import librosa
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models

def compute_spectrogram(audio_data, sr=44100):
  if audio_data.ndim == 2:  # Check if audio is stereo
      # Compute spectrogram for each channel
      spectrograms = [librosa.feature.melspectrogram(y=channel, sr=sr) for channel in audio_data]
      # Convert to decibels and stack along the third dimension to form (height, width, channels)
      spectrogram_db = np.stack([librosa.power_to_db(s, ref=np.max) for s in spectrograms], axis=-1)
  else:
      # Process as mono
      spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr)
      spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
      spectrogram_db = np.expand_dims(spectrogram_db, axis=-1)  # Add channel dimension for mono
  return spectrogram_db

def process_wav_instrument(filepath):
  audio_data, sr = librosa.load(filepath, sr=None, mono=False)
  if audio_data.shape[-1] > 132299:
      audio_data = audio_data[:, :132299]
  elif audio_data.shape[-1] < 132299:
      pad_width = 132299 - audio_data.shape[-1]
      audio_data = np.pad(audio_data, ((0, 0), (0, pad_width)), mode='constant')
  
  
  spectrogram = compute_spectrogram(audio_data, sr=sr)
  #Calculated during model build based on training dataset
  # 3/23/24 need to update these
  DATASET_MEAN = -47.48947
  DATASET_STD = 19.5177
  
  spectrogram = (spectrogram - DATASET_MEAN) / DATASET_STD
  spectrogram = np.expand_dims(spectrogram, axis=0)
  print(spectrogram.shape)
  #spectrogram = spectrogram.reshape(-1, 128, 259, 1)

  model = models.load_model("../instrument_recognition/model_3_23_24.h5")
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