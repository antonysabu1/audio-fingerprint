import os
import json

def load_config():
    cfg_path = os.environ.get("DJV_CONFIG_PATH", "dejavu_config.example.json")
    with open(cfg_path, "r") as f:
        return json.load(f)

def env_db_config():
    return {
        "database": {
            "host": os.environ.get("DJV_DB_HOST", "db"),
            "user": os.environ.get("DJV_DB_USER", "dejavu"),
            "passwd": os.environ.get("DJV_DB_PASS", "dejavu_pass"),
            "db": os.environ.get("DJV_DB_NAME", "dejavu_db")
        }
    }
