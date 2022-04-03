# Harmony_Grader_full_2022

Harmony Grader Version April, 2022.

The script, which inspects the XML files of harmony (figured bass realizations) tasks, chorals for basic errors:
  1. Parallelisms - fifths, octaves
  2. Voice Crossing
  3. All voices moving to one direction

How to install and to use?

1. Python 3.9 installation is obligatory.
2. Clone this repository.
3. Activate virtual environment, install dependencies with command "pip install -r requirements.txt".
4. Keep MuseScore3 music editor already installed.
5. Setup environment for music21 - path to MuseScore folder in order to get music images in Jupyter Notebook, 
more information: https://stackoverflow.com/questions/43060669/python-how-to-rename-musescore-path-in-package-music21
6. Launch Grader with command "jupyter notebook Grader.ipynb" 
7. Run the script, copy and paste into the input box the path your .xml music file.

What is new?

1. Now the Grader is able to scan music for any number of voices (from 2 to any). 
2. New function: scanning for all voices moving the same direction (up or down).
