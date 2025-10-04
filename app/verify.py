import librosa
import numpy as np

def compute_mfcc(path, sr=22050, n_mfcc=20):
    y, _ = librosa.load(path, sr=sr, mono=True)
    # trim silence quickly
    y, _ = librosa.effects.trim(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfcc

def dtw_score(query_mfcc, candidate_mfcc):
    # use cosine distance in DTW
    D, wp = librosa.sequence.dtw(X=query_mfcc, Y=candidate_mfcc, metric='cosine')
    cost = D[-1, -1] / D.shape[0]
    # map to 0..1 (simple)
    score = max(0.0, 1.0 - cost)
    return float(score), wp
