import pandas as pd
import bcrypt
from pathlib import Path

FILE = Path(__file__).resolve().parent / "users.csv"

users = [
    {"username": "admin", "password": "alice/password123", "role": "admin"},
]

df = pd.DataFrame(users)

df["password"] = df["password"].apply(
    lambda x: bcrypt.hashpw(x.encode(), bcrypt.gensalt()).decode()
)

df.to_csv(FILE, index=False)

print("✅ Users ready")