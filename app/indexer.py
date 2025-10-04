import os
from dejavu import Dejavu
from utils import env_db_config

AUDIO_DIR = os.environ.get("AUDIO_DIR", "/app/sample_audio")

def main():
    config = env_db_config()
    djv = Dejavu(config)
    print("Fingerprinting files in", AUDIO_DIR)
    djv.fingerprint_directory(AUDIO_DIR, [".wav", ".mp3", ".m4a"], n_processes=4)
    print("Done.")

if __name__ == "__main__":
    main()
