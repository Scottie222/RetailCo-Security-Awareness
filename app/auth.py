import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_users():
    return pd.read_csv(BASE_DIR / "data" / "users.csv")

def authenticate(username, password):
    users = load_users()
    user = users[(users["username"] == username) & (users["password"] == password)]
    
    if not user.empty:
        return user.iloc[0]["role"]
    return None