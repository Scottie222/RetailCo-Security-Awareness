# 🛡️ RetailCo Security Awareness & Phishing Simulation Framework

> Cybersecurity awareness platform inspired by the Transnet ransomware attack on South African infrastructure. Simulates phishing campaigns, scores employee risk, and provides an AI-powered email detector — all in a live dashboard.

---

## 📁 Project Structure

```
RetailCo-Security-Awareness/
│
├── app/
│   ├── app.py              ← Main Streamlit dashboard
│   ├── auth.py             ← Login & bcrypt authentication
│   └── ai_detector.py      ← ML phishing email classifier
│
├── data/
│   ├── users.csv           ← Hashed user credentials
│   └── phishing_results.csv← Simulation results data
│
├── reports/
│   └── report.csv          ← Exported reports (auto-generated)
│
├── assets/                 ← Logos, images
├── generate_users.py       ← One-time script to hash passwords
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Dashboard | Streamlit |
| Data | Pandas |
| Charts | Matplotlib |
| ML Classifier | Scikit-learn (TF-IDF + Random Forest) |
| Auth | bcrypt |

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Scottie222/RetailCo-Security-Awareness.git
cd RetailCo-Security-Awareness
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate user credentials (run once)

> ⚠️ This step is required. The `users.csv` file ships with placeholder hashes that will crash the login. Run this script to replace them with real bcrypt hashes.

```bash
python generate_users.py
```

This writes valid hashed passwords for `admin`, `alice`, and `bob` into `data/users.csv`.

### 5. Launch the dashboard

```bash
cd app
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Login Credentials

| Username | Password | Role |
|---|---|---|
| `admin` | `admin123` | Admin |
| `alice` | `analyst123` | Analyst |
| `bob` | `viewer123` | Analyst |

---

## 📊 Dashboard Features

| Tab | What it shows |
|---|---|
| **Overview** | Phishing donut chart, department risk bar chart, click vs report comparison |
| **Trends** | Weekly phishing rate line chart, monthly summary table |
| **Employees** | Per-employee risk table with 🔴/🟡/🟢 risk labels |
| **AI Detector** | Paste any email — ML model classifies it as phishing or safe |

### Risk Score Formula
```
Risk = (phishing_rate × 0.4) + (click_rate × 0.4) − (report_rate × 0.2)
```
Colour-coded: 🟢 < 30% · 🟡 30–60% · 🔴 > 60%

---

## 🛡️ POPIA Relevance

Phishing attacks can lead to unauthorised access to personal information, resulting in violations of the **Protection of Personal Information Act (POPIA)**. All suspicious emails must be reported within 24 hours of receipt.

---

## 🧪 Running Tests

```bash
# From repo root, with venv activated
chmod +x test.sh
./test.sh
```

Smoke tests cover: imports, auth (valid + invalid credentials), AI detector (phishing + safe), and CSV integrity.

---

## 🔄 Resetting Demo Data

```bash
chmod +x reset.sh
./reset.sh
```

Clears `phishing_results.csv` and regenerates `users.csv` — useful before presentations.

---

## 🚀 Future Enhancements

- [ ] AI phishing detection with larger training corpus
- [ ] Email simulation engine (send mock phishing emails)
- [ ] Real-time monitoring & alerting
- [ ] Cloud deployment (Streamlit Cloud / Azure)
- [ ] PDF report export

---

## 👤 Author

**Scott Ngcampalala**  
Cybersecurity Awareness Project · South Africa · 2024