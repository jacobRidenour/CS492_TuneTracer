from flask import Flask, request, jsonify, send_from_directory, send_file, current_app
import os
import io
from utils import *
from model.instrument_recognizer import *
import uuid
import tensorflow as tf
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH
from music21 import environment

app = Flask(__name__, static_folder='../Application/client/src')

TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'temp')

temp_store = {}

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400
    
    # If temp dir gets too full...
    cleanup_old_files(TEMP_DIR)
    
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    audio_path = os.path.join(TEMP_DIR, unique_filename)
    file.save(audio_path)
    
    # Process audio file into MIDI with basic-pitch
    output_directory = TEMP_DIR
    predict_and_save(
        audio_path_list=[audio_path],
        output_directory=output_directory,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=True
    )
    
    # Classify instrument from original audio file
    try:
        prediction = -1
        prediction = process_wav_instrument(audio_path)
        prediction = enumerate_prediction(prediction)
    except Exception as e:
        current_app.logger.error(f"Error in instrument recognition: {str(e)}")
        return {"error": "Internal server error"}, 500
    
    midi_filename = os.path.splitext(unique_filename)[0] + '_basic_pitch.mid'
    
    try: 
        midi_path = os.path.join(output_directory, midi_filename)
        
        # Open/Edit midi here (maybe use a function in utils.py?)
        # try:
        #     with open(midi_path) as file:
        #         change instrument of midi file based on prediction
        #         other changes
        # except Exception as e:
        #     current_app.logger.error(f"Error in editing MIDI: {str(e)}")
        #     return {"error": "Internal server error"}, 500
        
        if os.path.exists(midi_path):
            print('MIDI file exists:', midi_path)
            id = str(uuid.uuid4())
            temp_store[id] = midi_path
            return jsonify({
                "midiId": id,
                "midiFilename": midi_filename,
                # "pdfId": "soon"
                "instrumentPrediction": prediction,
            })
        else:
            print('MIDI file does not exist:', midi_path)
            return {"error": "Failed to generate MIDI file"}, 500
    except Exception as e:
        current_app.logger.error(f"Error in handle_upload: {str(e)}")
        return {"error": "Internal server error"}, 500

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    if file_id in temp_store:
        file_path = temp_store[file_id]
        print(f"Attempting to serve file from path: {file_path}")
        try:
            return send_from_directory(directory=TEMP_DIR, path=os.path.basename(file_path), as_attachment=True)
        except Exception as e:
            print(f"Error serving file: {e}")
            return {"error": "Internal server error"}, 500
    return {"error": "File not found"}, 404

@app.route('/getPdf/<file_id>', methods=['GET'])
def send_pdf(file_id):
    if file_id in temp_store:
        file_path = temp_store[file_id]
        print(f'Attempting to convert midi file {file_path} to pdf')
        try:
            midi_pdf = midi_to_pdf(file_path)
            return send_file(
                io.BytesIO(midi_pdf),
                mimetype='application/pdf',
                as_attachment=True,
                download_name="output.pdf"
            )
        except Exception as e:
            print(f"error serving pdf {e}")
            return {"error": "Internal server error"}, 501
    return {"error": "File not found"}, 404

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
        
    # Set appropriate location for lilypond for Windows users
    if sys.platform.startswith('win'):
        project_root = Path(__file__).parent.parent
        include_folder_path = project_root / "include" / "lilypond-2.24.3" / "bin" / "lilypond.exe"
        lilypond_path = str(include_folder_path.resolve())
        environment.set('lilypondPath', lilypond_path)
        print(f"Lilypond path set to {lilypond_path}")
        
    app.logger.setLevel('DEBUG')
    app.run(debug=True)
