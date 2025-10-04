import os
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer
from utils import env_db_config
from verify import compute_mfcc, dtw_score

THRESHOLD = float(os.environ.get("VERIFICATION_THRESHOLD", 0.6))

def recognize_and_verify(query_path):
    djv = Dejavu(env_db_config())
    # First-stage: Dejavu recognition (coarse)
    result = djv.recognize(FileRecognizer, query_path)
    if not result:
        return []

    # result keys: 'song_name', 'confidence', 'offset_seconds'
    matches = []
    song_name = result.get('song_name')
    dejavu_conf = result.get('confidence', 0)

    # You must map song_name -> file path / asset metadata in your DB
    # For this prototype we assume song_name is the filename in /app/indexes/
    candidate_path = os.path.join("/app/indexes", song_name)
    if not os.path.exists(candidate_path):
        # fallback: Full DB lookup or S3 fetch - left for integration
        print("Candidate file not found locally:", candidate_path)
        candidate_path = None

    if candidate_path:
        q_mfcc = compute_mfcc(query_path)
        c_mfcc = compute_mfcc(candidate_path)
        score, wp = dtw_score(q_mfcc, c_mfcc)
        if score >= THRESHOLD:
            matches.append({
                "song_name": song_name,
                "dejavu_confidence": dejavu_conf,
                "dtw_score": score
            })
    return matches

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python recognizer.py /path/to/query.wav")
        sys.exit(1)
    q = sys.argv[1]
    print(recognize_and_verify(q))
