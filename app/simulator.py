import pandas as pd
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def simulate_phishing():
    departments = ["Finance", "IT", "Sales", "HR", "Logistics"]

    data = []

    for i in range(1, 101):
        data.append({
            "Employee_ID": i,
            "Department": random.choice(departments),
            "Email_Clicked": random.choice(["Yes", "No"]),
            "Credentials_Submitted": random.choice(["Yes", "No"]),
            "Reported_Phish": random.choice(["Yes", "No"]),
            "Attack_Type": "Ransomware"
        })

    df = pd.DataFrame(data)

    file_path = BASE_DIR / "data" / "phishing_results.csv"
    df.to_csv(file_path, index=False)

    return df