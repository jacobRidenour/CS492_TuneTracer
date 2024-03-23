# Project Background

Developed by Treyton Perkins, Jacob Ridenour, and Austin Shutt for Purdue Fort Wayne course CS 49200 Machine Learning.

# Tune Tracer

This project takes input as a single-instrument (even polyphonic) audio file, converts it into [MIDI](https://en.wikipedia.org/wiki/MIDI) [format](http://midi.teragonaudio.com/tech/midispec.htm), and generates a PDF with the sheet music represented in the MIDI file. We modify Basic Pitch's MIDI output with the help of our deep learning model (included in this project) that detects and selects the proper instrument and updates the sheet music accordingly.

For audio to MIDI conversion we are using Spotify's automatic music transcription (AMT) machine learning model, [Basic Pitch](https://github.com/spotify/basic-pitch).

For MIDI to PDF conversion we are using [GNU lilypond](https://lilypond.org/).

# Setup

Clone this repository:
```bash
git clone https://github.com/jacobRidenour/CS492_TuneTracer.git
```

This project uses the open source command line music tool lilypond. Visit https://lilypond.org/download.html for information on downloading and installing lilypond.

<strong>If utilizing Windows:</strong> <br>
Place this program with the following directory structure:

`$(ProjectRoot)\include\lilypond-2.24.3\bin\lilypond.exe`.

Linux users do not need to do this.

```bash
cd TuneTracer
py -3 -m venv .venv
. .venv/scripts/activate
pip install -r requirements.txt
```

# Running the server
```bash
cd TuneTracer/server
python server.py
```
This will currently produce a basic site at port 5000 on localhost. .wav files are the currently only known supported file for instrument prediction.