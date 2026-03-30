# 🔐 RetailCo Security Awareness & Phishing Simulation Framework

## 🚢 Project Overview

This project simulates a cybersecurity incident within a fictional retail company, **RetailCo**, inspired by the Transnet cyberattack in South Africa.

The application demonstrates how phishing attacks can lead to ransomware infections, disrupting operations and increasing organizational risk.

---

## 🎯 Objectives

* Simulate phishing attacks
* Measure employee vulnerability
* Calculate department-level risk
* Visualize cybersecurity metrics
* Promote POPIA awareness

---

## 🧠 Scenario (Real-World Inspired)

RetailCo experienced a ransomware attack initiated through a phishing email.
The attack impacted logistics operations, similar to the Transnet cyberattack that disrupted South African ports.

---

## ⚙️ Features

* 🔐 Login system (Admin & Analyst roles)
* 🎯 Phishing simulation engine
* 📊 Risk scoring system
* 📈 Interactive dashboard (Streamlit)
* 📄 Exportable reports
* 🛡️ POPIA awareness module

---

## 🏗️ Tech Stack

* Python
* Streamlit
* Pandas
* Matplotlib

---

## 📁 Project Structure

```
RetailCo-Security-Awareness/
│
├── app/
│   ├── app.py
│   ├── auth.py
│   ├── simulator.py
│
├── data/
│   ├── phishing_results.csv
│   ├── users.csv
│
├── reports/
├── assets/
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1. Clone repo

```
git clone <your-repo-link>
cd RetailCo-Security-Awareness
```

### 2. Create virtual environment

```
python -m venv venv
```

### 3. Activate environment

```
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run app

```
cd app
streamlit run app.py
```

---

## 🔑 Login Credentials

Admin:

* username: admin
* password: admin123

User:

* username: analyst
* password: analyst123

---

## 📊 Key Insights

* Employees who submit credentials significantly increase risk
* Reporting phishing reduces overall organizational risk
* Logistics and Finance departments are highest risk in ransomware scenarios

---

## 🛡️ POPIA Relevance

Phishing attacks can lead to unauthorized access to personal information, resulting in potential POPIA violations.

---

## 🚀 Future Enhancements

* AI phishing detection
* Email simulation engine
* Real-time monitoring
* Cloud deployment

---

## 👤 Author

Scott Ngcampalala
