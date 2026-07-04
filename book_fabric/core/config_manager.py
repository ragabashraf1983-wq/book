import os
from pathlib import Path
from dotenv import load_dotenv, set_key

ENV_PATH = Path(".env")

def get_setting(key: str, default: str = None) -> str:
    load_dotenv(ENV_PATH)
    return os.getenv(key, default)

def save_setting(key: str, value: str):
    # Ensure .env exists
    if not ENV_PATH.exists():
        ENV_PATH.touch()
    set_key(str(ENV_PATH), key, value)

def is_configured() -> bool:
    load_dotenv(ENV_PATH)
    return os.getenv("NINEROUTER_API_KEY") is not None
