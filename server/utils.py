import os
import sys
from pathlib import Path
from music21 import midi, stream

# Convert MIDI to PDF with lilypond
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

# Clean out files from temp directory when there's more than the threshold
def cleanup_old_files(directory, max_files=30):
    delete = False
  
    # Get list of files in temp dir
    files = sorted(
        [
          os.path.join(directory, filename)
          for filename in os.listdir(directory)
          if not filename.endswith('.pdf')
        ]
    )

    # If we've got more than max_files, clear out the folder
    if len(files) > max_files:
      delete = True
    
    if delete:
        for i in range(len(files)):
          os.remove(files[i])
          print(f"Deleted old file: {files[i]}")

