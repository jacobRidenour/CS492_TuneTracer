from music21 import midi, stream, environment
import os
import librosa
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models

environment.set('lilypondPath', 'C:/Users/Austin/Downloads/lilypond-2.24.3-mingw-x86_64/lilypond-2.24.3/bin/lilypond.exe')
# stuff with basic pitch

# stuff with instrument classifier

# misc helper functions and stuff

# convert midi to pdf
def midi_to_pdf(midi_path):
  #read midi file
  midi_file = midi.translate.midiFilePathToStream(midi_path)

  score = stream.Score()
  part = stream.Part()

  #add each midi event (note) to the score
  for event in midi_file.flatten().notes:
    part.append(event)
  score.append(part)

  #temporarily store pdf
  score.write("lily.pdf", fp="./temp")

  #read pdf
  with open("./temp.pdf", "rb") as pdf_file:
    pdf_content = pdf_file.read()

  #remove temp pdf
  os.remove("./temp.pdf")
  os.remove("./temp")

  return pdf_content

def compute_spectrogram(audio_data, sr=44100):
    # Compute the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr)

    # Convert to decibels (log scale)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    return spectrogram_db

def process_wav_instrument(filepath):
  audio_data, _ = librosa.load(filepath, sr=None)
  spectrogram = compute_spectrogram(audio_data[:132299])
  DATASET_MEAN = -47.48947
  DATASET_STD = 19.5177

  spectrogram = (spectrogram - DATASET_MEAN) / DATASET_STD
  spectrogram = np.expand_dims(spectrogram, axis=-1)
  spectrogram = spectrogram.reshape(-1, 128, 259, 1)

  model = models.load_model("../instrument_recognition/best_model_1.keras")
  prediction = model.predict(spectrogram)
  
  return prediction