import pandas as pd
import bcrypt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "data" / "users.csv"

def load_users():
    return pd.read_csv(USERS_FILE)

def authenticate(username, password):
    users = load_users()
    user = users[users["username"] == username]

    if not user.empty:
        stored_hash = user.iloc[0]["password"]
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return user.iloc[0]["role"]

    return None