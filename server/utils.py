from music21 import *
import os
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
