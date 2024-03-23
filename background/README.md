Original requirements found in `Requirements.pptx`. Updated/clarified requirements in `Review.pptx`.

# Functional Requirements

## Must-Have

* ~~Upload audio files~~
  * ~~Generate MIDIs from audio files using Spotify's Basic Pitch model~~
  * ~~Generate & display PDFs from above MIDI files~~
  * ~~Ability to visualize sheet music based on user-provided audio files as PDF~~
* Upload a MIDI file
  * Generate and display PDF from the MIDI file (e.g. user corrected the MIDI file)
* Use instrument classifier model to set appropriate instrument in MIDI output

## Nice to Have

* Play Basic Pitch MIDI output directly in browser
  * Visualization of the output
* Key changes
  * Ability to change/set the key for MIDI file
  * Ability to change/set the key for sheet music PDF
* Add instrument name to PDF somewhere
* Record audio directly in browser (add functionality to file chooser)
* Use YouTube video link as input
  * Visualization of the output alongside input video

# Nonfunctional Requirements

* Simple and intuitive UI
* Processing reliability (appropriate error handling)
* Responsive interface
* Acceptable performance (indicate to user if something takes more than a few seconds)
* Maintainable project infrastructure