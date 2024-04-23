import librosa
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models
import math

MAX_SAMPLES = 10
model = models.load_model("../instrument_recognition/model_4_22_24.h5")
print("Model Loaded!")

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
  #Calculated during model build based on training dataset
  # 3/23/24 need to update these
  DATASET_MEAN = -47.03523
  DATASET_STD = 18.62283

  audio_data, sr = librosa.load(filepath, sr=None, mono=False)
  prediction = np.zeros(11)

  if audio_data.shape[-1] > 132299:
      #audio_data = audio_data[:, :132299]
      audio_chunks = chunk_audio_fixed_segments(audio_data, 132299, MAX_SAMPLES) 
  elif audio_data.shape[-1] < 132299:
      pad_width = 132299 - audio_data.shape[-1]
      audio_chunks[0] = np.pad(audio_data, ((0, 0), (0, pad_width)), mode='constant')

  #print(audio_chunks)

  i = 1
  for chunk in audio_chunks:
      spectrogram = compute_spectrogram(chunk, sr=sr)
      spectrogram = (spectrogram - DATASET_MEAN) / DATASET_STD
      spectrogram = np.expand_dims(spectrogram, axis=0)
      result = model.predict(spectrogram)
      print(enumerate_prediction(np.argmax(result)))
      print(result)
      print(f'*****Winner of segment {i}/{len(audio_chunks)}: {enumerate_prediction(np.argmax(result))}*****')
      i += 1
      prediction = prediction + result

  
  print("Final Prediction:")
  prediction = np.argmax(prediction)
  
  return prediction

def enumerate_prediction(prediction):
  if prediction == -1:
     return "None"
  
  mapping = ['Cello', 'Clarinet', 'Flute', 'Acoustic Guitar', 'Electric Guitar', 'Organ',
              'Piano', 'Saxophone', 'Trumpet', 'Violin', 'Voice']
  return mapping[prediction]

def chunk_audio_fixed_segments(data, segment_length, num_segments):
    print(f'data.shape is {data.shape}')
    
    channels, total_length = data.shape
    desired_length = segment_length * num_segments
    
    # Calculate the minimal necessary overlap to fit the desired length
    if num_segments > 1:
        overlap = max(0, math.ceil((segment_length * num_segments - total_length) / (num_segments - 1)))
    else:
        overlap = 0  # No overlap needed if only one segment is requested

    chunk_data = np.zeros((num_segments, channels, segment_length), dtype=data.dtype)

    start = 0
    for i in range(num_segments):
        end = start + segment_length
        end = min(end, total_length)  # Ensure we do not go out of the bounds of the data
        actual_length = end - start
        if actual_length > 0:
            chunk_data[i, :, :actual_length] = data[:, start:end]
        start += segment_length - overlap  # Move start forward by segment length minus overlap

    return chunk_data
