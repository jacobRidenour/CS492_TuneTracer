import os
import sys
from pathlib import Path
from music21 import midi, stream, environment

if sys.platform.startswith('win'):
    project_root = Path(__file__).parent.parent
    include_folder_path = project_root / "include" / "lilypond-2.24.3" / "bin" / "lilypond.exe"
    lilypond_path = str(include_folder_path.resolve())
    environment.set('lilypondPath', lilypond_path)
    print(f"Lilypond path set to {lilypond_path}")

# stuff with basic pitch

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