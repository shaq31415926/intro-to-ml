import os
import pandas as pd
import librosa 
import scipy


def create_audio_features_df(list_of_audio_files):
    """Method which loads a list of audio data files and returns a DataFrame with features extracted. 
    """

    audio_features = []

    for audio_file in list_of_audio_files:
        audio_file_name = os.path.basename(audio_file)

        # load the file into an array
        x , sr = librosa.load(audio_file)

        # extract features from the audio dictionry
        # zero crossing rate
        zcr = librosa.zero_crossings(x).sum()

        # energy
        energy = scipy.linalg.norm(x)

        # duration
        S = librosa.stft(x)
        duration = librosa.get_duration(S=S, sr=sr)

        # store as a dict
        audio_features.append({"audio_file_name": audio_file_name,
                                 "zero_crossing_rate": zcr,
                                 "energy": energy,
                               "duration":duration
                                 })
        
    audio_features_df = pd.DataFrame(audio_features)
    audio_features_df = audio_features_df.set_index("audio_file_name")

        
    return audio_features_df