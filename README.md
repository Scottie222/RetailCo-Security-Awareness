# RetailCo Security Awareness Platform

## Overview

RetailCo is a phishing simulation and security awareness platform built for retail organisations. It was developed in response to the growing threat of social engineering attacks targeting operational staff — particularly following the 2021 Transnet ransomware incident, which demonstrated how a single phishing email can bring a critical logistics operation to a halt.

The platform gives security teams a controlled environment to test how employees respond to phishing attempts, measure risk at a department level, and track whether awareness training is producing measurable improvement over time. It is not a theoretical exercise — every simulation run writes real results to the database, and every metric on the dashboard reflects the actual state of the organisation.

The problem it solves is straightforward: most organisations cannot answer the question "which of our employees would click a phishing link today?" This tool answers it, department by department, and gives you the data to do something about it.

---

## What the Platform Does

**Phishing Simulation** — Launch configurable campaigns targeting specific departments or the full organisation. Set the date, number of employees, and expected click and report rates. Results are written to the data store and reflected immediately across all metrics.

**Risk Scoring** — Each simulation produces a composite risk score based on click rate, phishing exposure, and reporting behaviour. The formula weights proactive reporting as a mitigating factor, which means organisations that train employees to report suspicious emails will see their score improve over time.

**Department Analysis** — Risk is broken down by department so that security teams can prioritise training where it is needed most. In most retail environments, Logistics and Finance carry the highest exposure.

**Employee Records** — Every simulated interaction is logged against an employee name and department, giving HR and security teams a clear view of who needs intervention.

**AI Email Classifier** — A machine learning model trained on phishing and legitimate email patterns. Paste the body of any suspicious email and the model will classify it, provide a confidence percentage, and highlight the specific language patterns that triggered the classification.

**POPIA Compliance Tracking** — The platform surfaces reporting behaviour as a first-class metric, which is directly relevant to POPIA obligations around the handling and protection of personal information.

---

## Tech Stack

| Component | Technology |
|---|---|
| Dashboard | Streamlit |
| Data processing | Pandas |
| Charts | Matplotlib |
| ML classifier | Scikit-learn — TF-IDF vectoriser with Logistic Regression |
| Authentication | bcrypt |

---

## Project Structure

```
RetailCo-Security-Awareness/
│
├── app/
│   ├── app.py                  Main dashboard and all UI logic
│   ├── auth.py                 Login authentication using bcrypt
│   └── ai_detector.py          Email classification model
│
├── data/
│   ├── users.csv               Hashed user credentials
│   └── phishing_results.csv    Simulation results and history
│
├── reports/                    Auto-generated report exports
├── assets/                     Static assets
├── generate_users.py           One-time credential setup script
├── setup.sh                    Full environment setup
├── run.sh                      Start the application
├── reset.sh                    Clear data for a fresh demo
├── test.sh                     Smoke test suite
└── requirements.txt
```

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/Scottie222/RetailCo-Security-Awareness.git
cd RetailCo-Security-Awareness
```

### 2. Create a virtual environment

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate user credentials

This step is required before first run. The repository ships with placeholder password hashes that will cause login to fail. Run the following script once to replace them with valid bcrypt hashes:

```bash
python generate_users.py
```

### 5. Start the application

```bash
cd app
streamlit run app.py
```

The dashboard will be available at http://localhost:8501.

---

## User Accounts

| Username | Password | Role |
|---|---|---|
| admin | admin123 | Admin — full access including simulation controls |
| alice | analyst123 | Analyst — read access to all dashboards |
| bob | viewer123 | Analyst — read access to all dashboards |

Passwords are stored as bcrypt hashes in `data/users.csv`. To add or change users, edit `generate_users.py` and re-run it.

---

## Dashboard Tabs

**Overview** — High-level metrics across all simulations. Shows the phishing/safe distribution, department risk ranked by exposure, and a side-by-side view of click rates versus report rates by department.

**Trends** — Weekly phishing rate plotted over time, and a month-by-month summary table. This is where you see whether the organisation is improving.

**Employees** — Full log of every simulated interaction, including employee name, department, whether they clicked, whether they reported, and a risk classification (High / Medium / Low).

**Simulate** — Configure and run a new phishing campaign. Choose the target department, number of employees, date, and the expected behavioural rates. On launch, the results are appended to the data store and all metrics refresh automatically.

**AI Detector** — Paste the body of any email. The model returns a classification, a confidence percentage, and the specific phrases that contributed to the result.

---

## Risk Score

The platform computes a composite risk score per simulation using the following formula:

```
Risk = (phishing_rate x 0.4) + (click_rate x 0.4) - (report_rate x 0.2)
```

A score above 60% is classified as high risk. Between 30% and 60% is moderate. Below 30% indicates the organisation is responding well. Reporting behaviour is treated as a mitigating factor — departments that actively flag suspicious emails will see a lower score even at the same phishing exposure level.

---

## POPIA Relevance

Under the Protection of Personal Information Act, organisations are required to take reasonable steps to prevent the compromise of personal information. Phishing is the most common initial vector for data breaches. This platform supports compliance by giving security teams measurable evidence of employee awareness levels, identifying high-risk departments before an incident occurs, and tracking improvement over time.

---

## Utility Scripts

```bash
# Run full test suite (imports, auth, AI classifier, CSV integrity)
chmod +x test.sh && ./test.sh

# Reset all simulation data before a demo
chmod +x reset.sh && ./reset.sh
```

---

## Planned Improvements

- Expand the AI classifier training corpus for improved accuracy on South African phishing patterns
- Add PDF report export for management presentations
- Build an email dispatch engine to send real simulated phishing emails
- Support cloud deployment on Streamlit Cloud or Azure App Service

---

## Author

Scott Ngcampalala  
South Africa, 2026
