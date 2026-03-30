import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from auth import authenticate
from simulator import simulate_phishing

# ---------------- PATH SETUP ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "data" / "phishing_results.csv"
reports_dir = BASE_DIR / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

# ---------------- UI STYLE ----------------
st.set_page_config(page_title="RetailCo Cyber Dashboard", layout="wide")

st.markdown("""
<style>
body {background-color: #0E1117; color: white;}
[data-testid="metric-container"] {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "role" not in st.session_state:
    st.session_state.role = None

if st.session_state.role is None:
    st.title("🔐 RetailCo Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- LOAD DATA ----------------
df = pd.read_csv(data_path)

# ---------------- SIMULATION ----------------
if st.session_state.role == "admin":
    if st.button("🎯 Run Ransomware Simulation"):
        df = simulate_phishing()
        st.success("Simulation updated")

# ---------------- RISK ----------------
def calculate_risk(row):
    score = 0
    if row["Email_Clicked"] == "Yes":
        score += 2
    if row["Credentials_Submitted"] == "Yes":
        score += 5
    if row["Reported_Phish"] == "Yes":
        score -= 3
    score += 5
    return score

df["Risk_Score"] = df.apply(calculate_risk, axis=1)

def risk_label(score):
    if score <= 3:
        return "Low"
    elif score <= 6:
        return "Medium"
    else:
        return "High"

df["Risk_Level"] = df["Risk_Score"].apply(risk_label)

# ---------------- HEADER ----------------
st.title("🚢 RetailCo Cyber Incident Dashboard")

st.error("""
🚨 INCIDENT: Ransomware Attack Detected

• Entry: Phishing Email  
• Impact: Logistics Disruption  
• Risk: HIGH  
""")

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Employees", len(df))
col2.metric("Avg Risk", round(df["Risk_Score"].mean(), 2))
col3.metric("Reports", (df["Reported_Phish"] == "Yes").sum())

# ---------------- CHARTS ----------------
st.subheader("📊 Risk by Department")

dept = df.groupby("Department")["Risk_Score"].mean()
fig, ax = plt.subplots()
dept.plot(kind="bar", ax=ax)
st.pyplot(fig)

# Risk Levels
st.subheader("🔥 Risk Levels")
risk_counts = df["Risk_Level"].value_counts()
fig2, ax2 = plt.subplots()
risk_counts.plot(kind="bar", ax=ax2)
st.pyplot(fig2)

# ---------------- INSIGHTS ----------------
st.subheader("🧠 Insights")

high_risk = len(df[df["Risk_Level"] == "High"])
click_rate = (df["Email_Clicked"] == "Yes").mean() * 100

st.write(f"⚠️ {high_risk} employees are HIGH RISK")
st.write(f"📧 {round(click_rate,1)}% clicked phishing emails")

# ---------------- TIMELINE ----------------
st.subheader("⏳ Attack Timeline")

st.markdown("""
Day 1: Phishing emails sent  
Day 2: Credentials stolen  
Day 3: Ransomware deployed  
Day 4: Systems disrupted  
Day 5: Incident response  
""")

# ---------------- EXPORT ----------------
if st.button("📄 Export Report"):
    file_path = reports_dir / "report.csv"
    df.to_csv(file_path, index=False)
    st.success("Report exported!")

# ---------------- DOWNLOAD ----------------
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Report", csv, "RetailCo_Report.csv", "text/csv")

# ---------------- POPIA ----------------
st.warning("Failure to report phishing may lead to POPIA violations.")