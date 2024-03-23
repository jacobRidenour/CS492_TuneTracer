import librosa
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models

def compute_spectrogram(audio_data, sr=44100):
    # Compute the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr)

    # Convert to decibels (log scale)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    return spectrogram_db

def process_wav_instrument(filepath):
  audio_data, _ = librosa.load(filepath, sr=None)
  spectrogram = compute_spectrogram(audio_data[:132299])
  #Calculated during model build based on training dataset
  DATASET_MEAN = -47.48947
  DATASET_STD = 19.5177

  spectrogram = (spectrogram - DATASET_MEAN) / DATASET_STD
  spectrogram = np.expand_dims(spectrogram, axis=-1)
  print(spectrogram.shape)
  spectrogram = spectrogram.reshape(-1, 128, 259, 1)

  model = models.load_model("../instrument_recognition/model_3_11_24.h5")
  print("Model Loaded!")
  prediction = model.predict(spectrogram)
  prediction = np.argmax(prediction)
  return prediction

def enumerate_prediction(prediction):
  if prediction == -1:
     return "None"
  
  mapping = ['Cello', 'Clarinet', 'Flute', 'Acoustic Guitar', 'Electric Guitar', 
             'Organ', 'Piano', 'Saxophone', 'Trumpet', 'Violin', 'Voice']
  return mapping[prediction]