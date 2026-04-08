# RetailCo Security Awareness & Phishing Simulation

**Bakithi Scott Ngcampalala** Cybersecurity & GRC Professional
[github.com/Scottie222](https://github.com/Scottie222) · [LinkedIn](https://www.linkedin.com/in/bakithi-scott-ngcampalala-0051a4105)

---

## What this project is

A full-stack Python security awareness and phishing simulation platform built for South African retail organisations, grounded in the real R200 million phishing losses reported across South African businesses in 2023. The platform simulates phishing campaigns across 6 departments, tracks employee click rates and reporting behaviour, scores departmental risk, and includes an AI-powered email threat detector all wrapped in a live interactive Streamlit dashboard.

This is not a static report. It is a running application with login, role-based access, live simulation, and real-time risk scoring.

---

## The real incident

In 2023, South African businesses lost over **R200 million** to phishing attacks, making it the most costly social engineering threat vector in the country. The Finance and Logistics sectors were disproportionately targeted the same departments this simulation tracks as highest risk.

The Transnet cyberattack of 2021 which crippled South African port operations for weeks began with a phishing email. This platform is modelled on that scenario, simulating how a single employee click in Logistics can cascade into a full ransomware incident.

### Why phishing matters under POPIA

| Risk | POPIA implication |
|---|---|
| Employee clicks phishing link | Potential unauthorised access to personal information |
| Credentials submitted | Account compromise Section 19 safeguard failure |
| Data exfiltrated | Mandatory breach notification under Section 22 |
| Failure to report | POPIA compliance violation — Section 55 duty |

---

## Live dashboard features

- Secure login with role-based access (Admin and Analyst roles)
- Overview tab: total emails, phishing detected, employees clicked, reported, risk score
- Trends tab: click rate trends over 3 campaigns
- Employees tab: per-employee risk scoring and behaviour
- Simulate tab: run new phishing campaigns across departments
- AI Detector tab: paste any email and get instant threat classification

---

## Dashboard screenshots

To view the live dashboard run the app locally (instructions below). Login with:

| Role | Username | Password |
|---|---|---|
| Admin | admin | admin123 |
| Analyst | alice | analyst123 |

---

## Key results from 3 simulated campaigns

| Department | Click rate | Risk level |
|---|---|---|
| Marketing | 100% | Critical |
| Logistics | 94% | Critical |
| Finance | 88% | Critical |
| HR | 76% | High |
| Operations | 71% | High |
| IT | 52% | Medium |

Overall risk score reduced from 72% (Campaign 1) to 59% (Campaign 3) reflecting the impact of awareness training between campaigns.

---

## Framework alignment

| Framework | Coverage |
|---|---|
| ISO 27001:2022 | A.6.3 Security awareness, A.6.1 Screening, A.5.25 Incident assessment |
| POPIA Act 4 of 2013 | Section 19 safeguards, Section 22 breach notification, Section 55 Information Officer duties |
| NIST CSF 2.0 | Protect (PR.AT — Awareness and training), Respond (RS.CO — Communications) |

---

## How to run

```bash
git clone https://github.com/Scottie222/RetailCo-Security-Awareness.git
cd RetailCo-Security-Awareness
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python data\create_users.py
python -m streamlit run app\app.py
```

The dashboard opens at `http://localhost:8501`

---

## Project structure
RetailCo-Security-Awareness/
├── app/
│   ├── app.py              # Main Streamlit dashboard
│   ├── auth.py             # Login and role-based access
│   └── ai_detector.py      # AI phishing email classifier
├── data/
│   ├── create_users.py     # Generates users.csv with real bcrypt hashes
│   ├── users.csv           # User credentials
│   └── phishing_results.csv
├── reports/
├── assets/
├── requirements.txt
└── README.md

---

## References

1. SABRIC phishing statistics 2023 https://www.sabric.co.za
2. Transnet cyberattack https://www.itweb.co.za/content/KA3WBqdvgXqbRXm8
3. POPIA Act 4 of 2013 https://www.justice.gov.za/inforeg/docs/InfoRegSA-POPIA-act4of2013.pdf
4. ISO/IEC 27001:2022 A.6.3 https://www.iso.org/standard/82875.html

---

## Related GRC portfolio projects

| Project | Domain | Real incident |
|---|---|---|
| [StandardBank-Risk-Assessment](https://github.com/Scottie222/StandardBank-Risk-Assessment) | Risk Assessment | Experian SA 2020 — 24M records. [Live demo](https://scottie222.github.io/StandardBank-Risk-Assessment/) |
| [CloudSec-Assessment-SA](https://github.com/Scottie222/CloudSec-Assessment-SA) | Cloud Security | Dis-Chem 2022, Experian SA 2020 |
| [GRC-Controls-Lab](https://github.com/Scottie222/GRC-Controls-Lab) | Controls Lab | Capital One 2019 |
| [VendorRisk-SA](https://github.com/Scottie222/VendorRisk-SA) | Third-Party Risk | Experian, Dis-Chem, MTN, TransUnion |
| [LifeHealthcare-BCP](https://github.com/Scottie222/LifeHealthcare-BCP) | BCP/DR | Life Healthcare ransomware 2020 |
| [MTN-ISMS-Audit](https://github.com/Scottie222/MTN-ISMS-Audit) | Internal Audit | MTN SA breach April 2025 |
| [POPIA-GDPR-Compliance-Tracker](https://github.com/Scottie222/POPIA-GDPR-Compliance-Tracker) | Data Privacy | WhatsApp 2024 enforcement |