import os
import sys
from pathlib import Path
from music21 import *
import mido
from mido import MidiFile, MidiTrack, Message

def writePdf(score):
    # temporarily store pdf
    score.write("lily.pdf", fp="./temp")

    # read pdf
    with open("./temp.pdf", "rb") as pdf_file:
        pdf_content = pdf_file.read()

    # remove temp pdf 
    os.remove("./temp.pdf")
    os.remove("./temp")

    return pdf_content

def change_midi_instrument(midi_path, predicted_instrument):
    instrument_programs = {
        'Cello': 42,
        'Clarinet': 71,
        'Flute': 73,
        'Acoustic Guitar': 24,
        'Electric Guitar': 30,
        'Organ': 19,
        'Piano': 0,
        'Saxophone': 65,
        'Trumpet': 56,
        'Violin': 40,
        'Voice': 52,
        'None': None
    }

    new_program = instrument_programs.get(predicted_instrument, 0)  # Default to Piano

    mid = MidiFile(midi_path)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'program_change':
                msg.program = new_program

    mid.save(midi_path)


def score_to_grand_staff(part):
    treble_part = base.copy.deepcopy(part)
    bass_part = base.copy.deepcopy(part)
    
    break_val = note.Note(60).pitch.midi

    for event in treble_part.recurse().getElementsByClass(note.Note):
        if event.pitch.midi < break_val:
            r = note.Rest()
            treble_part.replace(event, r, recurse=True, allDerived=False)

    for event in bass_part.recurse().getElementsByClass(note.Note):
        if event.pitch.midi >= break_val:
            r = note.Rest()
            treble_part.replace(event, r, recurse=True, allDerived=False)

    for event in treble_part.recurse().getElementsByClass(chord.Chord):
        for chord_pitch in event.pitches:
            if chord_pitch.midi < break_val:
                event.remove(chord_pitch)
        if len(event.pitches) == 0:
            r = note.Rest()
            treble_part.replace(event, r, recurse=True, allDerived=False)

    for event in bass_part.recurse().getElementsByClass(chord.Chord):
        for chord_pitch in event.pitches:
            if chord_pitch.midi >= break_val:
                event.remove(chord_pitch)
        if len(event.pitches) == 0:
            r = note.Rest()
            treble_part.replace(event, r, recurse=True, allDerived=False)

    bass_clef = clef.BassClef()
    bass_part.insert(0, bass_clef)

    return treble_part, bass_part


def transpose_to_key(score, target_key):
    key = analysis.discrete.analyzeStream(score, 'key')
    i = interval.Interval(key.tonic, pitch.Pitch(target_key))
    transposed_score = score.transpose(i)
    return transposed_score


def getWritableStream(filePath):
    midi_file = midi.translate.midiFilePathToStream(filePath)
    score = stream.Score()
    part = stream.Part()

    for event in midi_file.flatten().notes:
        part.append(event)

    return part


# Convert MIDI to PDF with lilypond
def midi_to_pdf(midi_path, instrument):
    Bb_instruments = ['Clarinet', 'Saxophone', 'Trumpet']
    grand_staff = ['Piano', 'Organ']

    score = stream.Score()
    part = getWritableStream(midi_path)

    if instrument in Bb_instruments:
        score.append(part)
        score = transpose_to_key(score, target_key='Bb')
    elif instrument in grand_staff:
        treble, bass = score_to_grand_staff(part)
        score.append(treble)
        score.append(bass)
    elif instrument == 'Cello':
        part.insert(0, clef.BassClef())
        score.append(part)
    else:
        score.append(part)

    pdf_content = writePdf(score)
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
