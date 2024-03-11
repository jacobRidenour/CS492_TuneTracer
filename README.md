# Project Background

Developed by Treyton Perkins, Jacob Ridenour, and Austin Shutt for Purdue Fort Wayne course CS 49200 Machine Learning.

# Tune Tracer

This project uses Spotify's automatic music transcription (AMT) machine learning model, [Basic Pitch](https://github.com/spotify/basic-pitch).

Then with a locally trained model, we intend to modify the output of the Basic Pitch midi file to produce a more accurate representation of sheet music depending on the identified instrument.

# Setup

This project uses the open source command line music tool lilypond. Visit http://lilypond.org/download.html for information on 
downloading and installing lilypond

<strong>If utilizing Windows:</strong> <br>
Place this program with directory structure `$(ProjectRoot)\include\lilypond-2.24.3\bin\lilypond.exe`

# Running the server
```
. .venv/scripts/activate
cd server
python server.py
```
This will currently produce a basic site at port 5000 on localhost. .wav files are the currently only known supported file for instrument prediction.