from verify import compute_mfcc, dtw_score
import os

def test_dtw_score_small():
    # Using the same file yields a high score
    p = "sample_audio/example1.wav"
    if not os.path.exists(p):
        # skip if samples are missing
        return
    a = compute_mfcc(p)
    b = compute_mfcc(p)
    score, _ = dtw_score(a, b)
    assert score > 0.8
