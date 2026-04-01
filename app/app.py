import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
from pathlib import Path
from datetime import date
from auth import authenticate
from ai_detector import predict_email, predict_email_detail

DEPARTMENTS = ["Logistics", "Finance", "HR", "IT", "Operations", "Marketing"]

EMPLOYEE_POOL = [
    ("John Mokoena","Logistics"), ("Sarah Dlamini","Finance"), ("Thabo Nkosi","HR"),
    ("Lerato Sithole","IT"), ("Mpho Zulu","Logistics"), ("Nomsa Khumalo","Finance"),
    ("David Pietersen","Operations"), ("Ayanda Molefe","HR"), ("Sipho Ndlovu","IT"),
    ("Zanele Mahlangu","Logistics"), ("Bongani Cele","Logistics"), ("Priya Naidoo","HR"),
    ("Tebogo Molete","Finance"), ("Heinrich Botha","IT"), ("Ntombifuthi Dube","Logistics"),
    ("Kagiso Sithole","Finance"), ("Lindiwe Mthembu","HR"), ("Sifiso Nxumalo","IT"),
    ("Rudo Moyo","Operations"), ("Carlos Ferreira","Marketing"), ("Nandi Dlamini","HR"),
    ("Wayne Jacobs","IT"), ("Precious Khumalo","Logistics"), ("Lungelo Mthethwa","Finance"),
    ("Thandi Zungu","HR"), ("Andre du Toit","IT"), ("Nomvula Shabalala","Operations"),
    ("Sibusiso Mhlongo","Finance"), ("Fatima Mahomed","Marketing"), ("Vusi Masondo","IT"),
]

PHISHING_TEMPLATES = [
    "Your account has been suspended. Verify your identity immediately to restore access.",
    "URGENT: Unusual login detected. Confirm your password now or your account will be locked.",
    "Your salary payment has been delayed. Please verify your banking details with HR.",
    "SARS Tax Refund: You are eligible for a R4,500 refund. Click here to submit your details.",
    "Your package could not be delivered. Pay R45 customs fee to release your shipment.",
    "IT Security Alert: Your Microsoft license has expired. Renew immediately to avoid disruption.",
    "Congratulations! You have been selected as our lucky winner. Claim your R10,000 prize now.",
    "Action Required: Your email storage is full. Click here to upgrade your account.",
    "HR Notice: Please review and sign the attached employment contract immediately.",
    "Your PayPal account has been limited. Verify your details to restore full access.",
]

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent
PHISHING_CSV = BASE_DIR.parent / "data" / "phishing_results.csv"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RetailCo Cyber Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #0a0e1a;
    color: #c9d1e0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; }

.cyber-header {
    background: linear-gradient(135deg, #0d1b2a 0%, #0a1628 50%, #060d1a 100%);
    border: 1px solid #1e3a5f;
    border-left: 4px solid #00d4ff;
    border-radius: 4px;
    padding: 1.2rem 1.8rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.cyber-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,0.015) 2px,rgba(0,212,255,0.015) 4px);
    pointer-events: none;
}
.cyber-header h1 {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.6rem;
    color: #00d4ff;
    margin: 0;
    letter-spacing: 2px;
    text-shadow: 0 0 20px rgba(0,212,255,0.4);
}
.cyber-header p {
    font-size: 0.85rem;
    color: #5a7a9a;
    margin: 0.3rem 0 0 0;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 1px;
}

.metric-card {
    background: linear-gradient(135deg, #0d1b2a, #0a1520);
    border: 1px solid #1e3a5f;
    border-top: 2px solid #00d4ff;
    border-radius: 4px;
    padding: 1.2rem;
    text-align: center;
}
.metric-card.danger  { border-top-color: #ff3860; }
.metric-card.warning { border-top-color: #ffb400; }
.metric-card.safe    { border-top-color: #00e676; }
.metric-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.4rem;
    font-weight: bold;
    color: #00d4ff;
    display: block;
    text-shadow: 0 0 15px rgba(0,212,255,0.5);
}
.metric-card.danger  .metric-value { color: #ff3860; text-shadow: 0 0 15px rgba(255,56,96,0.5); }
.metric-card.warning .metric-value { color: #ffb400; text-shadow: 0 0 15px rgba(255,180,0,0.5); }
.metric-card.safe    .metric-value { color: #00e676; text-shadow: 0 0 15px rgba(0,230,118,0.5); }
.metric-label {
    font-size: 0.75rem;
    color: #5a7a9a;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
}

.section-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: #00d4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
}

.popia-alert {
    background: rgba(255,56,96,0.08);
    border: 1px solid rgba(255,56,96,0.3);
    border-left: 3px solid #ff3860;
    border-radius: 3px;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    color: #ff3860;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 0.5px;
    margin: 1rem 0;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #060d1a;
    border-bottom: 1px solid #1e3a5f;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    color: #5a7a9a !important;
    padding: 0.7rem 1.5rem !important;
    background: transparent !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
}

.stButton > button {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 1px;
    background: transparent;
    border: 1px solid #1e3a5f;
    color: #5a7a9a;
    border-radius: 2px;
    transition: all 0.2s;
}
.stButton > button:hover {
    border-color: #00d4ff;
    color: #00d4ff;
    background: rgba(0,212,255,0.05);
}

.stTextArea textarea {
    background: #0d1b2a !important;
    border: 1px solid #1e3a5f !important;
    color: #c9d1e0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.85rem !important;
    border-radius: 3px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0a0e1a",
    "axes.facecolor":   "#0d1b2a",
    "axes.edgecolor":   "#1e3a5f",
    "axes.labelcolor":  "#5a7a9a",
    "xtick.color":      "#5a7a9a",
    "ytick.color":      "#5a7a9a",
    "text.color":       "#c9d1e0",
    "grid.color":       "#1e3a5f",
    "grid.linestyle":   "--",
    "grid.alpha":       0.5,
    "font.family":      "monospace",
})

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [("logged_in", False), ("role", None), ("username", None), ("df", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Data loader ───────────────────────────────────────────────────────────────
def load_data():
    if PHISHING_CSV.exists():
        df = pd.read_csv(PHISHING_CSV)
        # Ensure required columns exist
        for col, fill in [("is_phishing", 0), ("department", "General"),
                          ("clicked", 0), ("reported", 0), ("employee", "Unknown")]:
            if col not in df.columns:
                df[col] = fill
        # Fill NaN in numeric columns BEFORE any int conversion
        for col in ["is_phishing", "clicked", "reported"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        df["department"] = df["department"].fillna("General").astype(str)
        df["employee"]   = df["employee"].fillna("Unknown").astype(str)
        df["date"]       = pd.to_datetime(df["date"], errors="coerce").fillna(pd.Timestamp.now())
        # Drop any rows that are completely empty
        df = df.dropna(how="all")
        return df
    return pd.DataFrame(columns=["email","is_phishing","department","date","employee","clicked","reported"])

# ── Charts ────────────────────────────────────────────────────────────────────
def chart_dept_risk(df):
    df = df.copy()
    df["is_phishing"] = df["is_phishing"].fillna(0).astype(int)
    if df.empty:
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.text(0.5, 0.5, "NO DATA", ha="center", va="center",
                transform=ax.transAxes, color="#5a7a9a", fontsize=12)
        ax.axis("off"); fig.tight_layout(); return fig
    dept = df.groupby("department").agg(
        phishing_rate=("is_phishing", "mean"),
        total=("is_phishing", "count"),
    ).reset_index().sort_values("phishing_rate", ascending=True)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    colors = ["#ff3860" if r > 0.7 else "#ffb400" if r > 0.4 else "#00e676"
              for r in dept["phishing_rate"]]
    bars = ax.barh(dept["department"], dept["phishing_rate"] * 100,
                   color=colors, height=0.55, zorder=2)
    ax.set_xlabel("Phishing Rate (%)", fontsize=8)
    ax.set_xlim(0, 110)
    ax.grid(axis="x", zorder=1)
    ax.spines[["top","right","left"]].set_visible(False)
    for bar, val in zip(bars, dept["phishing_rate"]):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                f"{val*100:.0f}%", va="center", fontsize=8, color="#c9d1e0")
    fig.tight_layout()
    return fig

def chart_trend(df):
    df = df.copy()
    df["is_phishing"] = df["is_phishing"].fillna(0).astype(int)
    if df.empty or "date" not in df.columns:
        fig, ax = plt.subplots(figsize=(8, 3.2))
        ax.text(0.5, 0.5, "NO DATA", ha="center", va="center",
                transform=ax.transAxes, color="#5a7a9a", fontsize=12)
        ax.axis("off"); fig.tight_layout(); return fig
    trend = df.groupby(df["date"].dt.to_period("W").dt.start_time).agg(
        phishing=("is_phishing", "sum"),
        total=("is_phishing", "count"),
    ).reset_index()
    trend["rate"] = trend["phishing"] / trend["total"]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    ax.fill_between(trend["date"], trend["rate"] * 100, alpha=0.15, color="#00d4ff")
    ax.plot(trend["date"], trend["rate"] * 100,
            color="#00d4ff", linewidth=2, marker="o", markersize=5,
            markerfacecolor="#0a0e1a", markeredgecolor="#00d4ff", markeredgewidth=1.5)
    ax.set_ylabel("Phishing Rate (%)", fontsize=8)
    ax.grid(axis="y")
    ax.spines[["top","right","left"]].set_visible(False)
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def chart_click_vs_report(df):
    df = df.copy()
    for col in ["clicked", "reported"]:
        df[col] = df[col].fillna(0).astype(int)
    if df.empty:
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.text(0.5, 0.5, "NO DATA", ha="center", va="center",
                transform=ax.transAxes, color="#5a7a9a", fontsize=12)
        ax.axis("off"); fig.tight_layout(); return fig
    depts    = df["department"].unique()
    clicked  = [df[df["department"] == d]["clicked"].sum()  for d in depts]
    reported = [df[df["department"] == d]["reported"].sum() for d in depts]
    x = np.arange(len(depts))
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.bar(x - 0.22, clicked,  0.4, label="Clicked",  color="#ff3860", alpha=0.85, zorder=2)
    ax.bar(x + 0.22, reported, 0.4, label="Reported", color="#00e676", alpha=0.85, zorder=2)
    ax.set_xticks(x)
    ax.set_xticklabels(depts, fontsize=8)
    ax.grid(axis="y", zorder=1)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.legend(fontsize=8, facecolor="#0d1b2a", edgecolor="#1e3a5f",
              labelcolor="#c9d1e0", loc="upper right")
    fig.tight_layout()
    return fig

def chart_donut(df):
    # Guard: drop NaN, ensure ints
    clean = df["is_phishing"].fillna(0).astype(int)
    phishing = int(clean.sum())
    safe     = len(clean) - phishing
    total    = phishing + safe

    fig, ax = plt.subplots(figsize=(3.5, 3.5))

    if total == 0:
        ax.text(0, 0, "NO DATA", ha="center", va="center",
                fontsize=12, color="#5a7a9a", fontfamily="monospace")
        ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.axis("off")
        fig.tight_layout()
        return fig

    ax.pie([phishing, safe],
           colors=["#ff3860", "#00e676"],
           startangle=90,
           wedgeprops={"width": 0.5, "edgecolor": "#0a0e1a", "linewidth": 2})
    ax.text(0, 0, f"{phishing/total*100:.0f}%\nPHISHING",
            ha="center", va="center", fontsize=13, color="#ff3860",
            fontfamily="monospace", fontweight="bold")
    patches = [mpatches.Patch(color="#ff3860", label=f"Phishing ({phishing})"),
               mpatches.Patch(color="#00e676", label=f"Safe ({safe})")]
    ax.legend(handles=patches, loc="lower center", fontsize=8,
              facecolor="#0d1b2a", edgecolor="#1e3a5f", labelcolor="#c9d1e0",
              bbox_to_anchor=(0.5, -0.08), ncol=2)
    fig.tight_layout()
    return fig

# ── Risk score ────────────────────────────────────────────────────────────────
def compute_risk(df):
    if df.empty:
        return 0
    click_rate  = df["clicked"].sum()  / max(len(df), 1)
    report_rate = df["reported"].sum() / max(len(df), 1)
    phish_rate  = df["is_phishing"].mean()
    return round(max(0, min(100, (phish_rate * 0.4 + click_rate * 0.4 - report_rate * 0.2) * 100)), 1)

def run_simulation(dept_filter, n_employees, click_rate_pct, report_rate_pct, sim_date):
    """
    Generate new phishing simulation rows and append them to phishing_results.csv.
    Returns the newly created DataFrame slice.
    """
    pool = [(n, d) for n, d in EMPLOYEE_POOL if dept_filter == "All" or d == dept_filter]
    if len(pool) < n_employees:
        pool = pool * (n_employees // len(pool) + 1)
    selected = random.sample(pool, n_employees)

    rows = []
    for name, dept in selected:
        template   = random.choice(PHISHING_TEMPLATES)
        clicked    = 1 if random.random() < (click_rate_pct / 100) else 0
        reported   = 1 if (not clicked) and random.random() < (report_rate_pct / 100) else 0
        rows.append({
            "email":        f"phish_{random.randint(1000,9999)}@sim.retailco.com",
            "is_phishing":  1,
            "department":   dept,
            "date":         str(sim_date),
            "employee":     name,
            "clicked":      clicked,
            "reported":     reported,
            "template":     template,
        })

    new_df = pd.DataFrame(rows)

    # Append to CSV
    if PHISHING_CSV.exists():
        existing = pd.read_csv(PHISHING_CSV)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    combined.to_csv(PHISHING_CSV, index=False)
    return new_df


# ── Login ─────────────────────────────────────────────────────────────────────
def login():
    _, col, _ = st.columns([1.5, 1, 1.5])
    with col:
        st.markdown("""
        <div style='text-align:center; padding:2rem 0 1.5rem 0;'>
            <div style='font-size:2.5rem;'>🛡️</div>
            <div style='font-family:"Share Tech Mono",monospace; font-size:1.1rem;
                        color:#00d4ff; letter-spacing:4px;'>RETAILCO</div>
            <div style='font-family:"Share Tech Mono",monospace; font-size:0.65rem;
                        color:#5a7a9a; letter-spacing:4px;'>CYBER AWARENESS PLATFORM</div>
        </div>
        """, unsafe_allow_html=True)
        username = st.text_input("USERNAME", placeholder="enter username")
        password = st.text_input("PASSWORD", placeholder="••••••••", type="password")
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.button("AUTHENTICATE →", use_container_width=True):
            role = authenticate(username.strip(), password.strip())
            if role:
                st.session_state.logged_in = True
                st.session_state.role      = role
                st.session_state.username  = username.strip()
                st.rerun()
            else:
                st.error("ACCESS DENIED — invalid credentials")
        st.markdown("""
        <div style='text-align:center; margin-top:1.5rem; font-family:"Share Tech Mono",monospace;
                    font-size:0.65rem; color:#2a3a4a; letter-spacing:1px;'>
            admin / admin123 &nbsp;·&nbsp; analyst / analyst123
        </div>""", unsafe_allow_html=True)

# ── Dashboard ─────────────────────────────────────────────────────────────────
def dashboard():
    if st.session_state.df is None:
        st.session_state.df = load_data()
    df = st.session_state.df

    # Header
    col_h, col_btn = st.columns([5, 1])
    with col_h:
        st.markdown(f"""
        <div class="cyber-header">
            <h1>🛡️ RETAILCO CYBER DASHBOARD</h1>
            <p>OPERATOR: {st.session_state.username.upper()} &nbsp;·&nbsp;
               ROLE: {st.session_state.role.upper()} &nbsp;·&nbsp;
               INCIDENT MONITORING ACTIVE</p>
        </div>""", unsafe_allow_html=True)
    with col_btn:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 REFRESH"):
            st.session_state.df = load_data()
            st.rerun()
        if st.button("🚪 LOGOUT"):
            for k in ["logged_in","role","username","df"]:
                st.session_state[k] = False if k == "logged_in" else None
            st.rerun()

    # KPI cards
    risk_score   = compute_risk(df)
    click_count  = int(df["clicked"].sum())  if "clicked"  in df.columns else 0
    report_count = int(df["reported"].sum()) if "reported" in df.columns else 0
    phish_count  = int(df["is_phishing"].sum())
    total        = len(df)
    risk_class   = "danger" if risk_score > 60 else "warning" if risk_score > 30 else "safe"

    for col, label, val, cls in zip(
        st.columns(5),
        ["TOTAL EMAILS","PHISHING DETECTED","EMPLOYEES CLICKED","REPORTED","RISK SCORE"],
        [total, phish_count, click_count, report_count, f"{risk_score}%"],
        ["", "danger", "danger", "safe", risk_class],
    ):
        with col:
            st.markdown(f"""
            <div class="metric-card {cls}">
                <span class="metric-value">{val}</span>
                <span class="metric-label">{label}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="popia-alert">⚠ POPIA COMPLIANCE ALERT — Failure to report phishing incidents may constitute a breach of POPIA. All suspicious emails must be reported within 24 hours.</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊  OVERVIEW", "📈  TRENDS", "🧑‍💼  EMPLOYEES", "🎯  SIMULATE", "🤖  AI DETECTOR"])

    with tab1:
        if df.empty:
            st.markdown("""
            <div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);
                        border-left:4px solid #00d4ff;padding:1.2rem 1.5rem;border-radius:3px;
                        font-family:"Share Tech Mono",monospace;color:#00d4ff;font-size:0.85rem;
                        line-height:1.8;'>
                📂 NO DATA LOADED<br>
                <span style='color:#5a7a9a;font-size:0.75rem;'>
                Make sure <b style='color:#c9d1e0;'>data/phishing_results.csv</b> exists in your repo root
                and contains rows. Copy the <b style='color:#c9d1e0;'>phishing_results.csv</b> file provided
                into your <b style='color:#c9d1e0;'>data/</b> folder, then click 🔄 REFRESH above.
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            ca, cb = st.columns([1, 2])
            with ca:
                st.markdown('<div class="section-title">Distribution</div>', unsafe_allow_html=True)
                st.pyplot(chart_donut(df), use_container_width=True)
            with cb:
                st.markdown('<div class="section-title">Risk by Department</div>', unsafe_allow_html=True)
                st.pyplot(chart_dept_risk(df), use_container_width=True)
            st.markdown('<div class="section-title">Click vs Report by Department</div>', unsafe_allow_html=True)
            st.pyplot(chart_click_vs_report(df), use_container_width=True)

    with tab2:
        st.markdown('<div class="section-title">Weekly Phishing Trend</div>', unsafe_allow_html=True)
        st.pyplot(chart_trend(df), use_container_width=True)
        st.markdown('<div class="section-title">Monthly Summary</div>', unsafe_allow_html=True)
        monthly = df.groupby(df["date"].dt.to_period("M")).agg(
            Phishing=("is_phishing","sum"), Total=("is_phishing","count"),
            Clicked=("clicked","sum"), Reported=("reported","sum"),
        ).reset_index()
        monthly["Period"] = monthly["date"].astype(str)
        monthly["Rate"]   = (monthly["Phishing"] / monthly["Total"] * 100).round(1).astype(str) + "%"
        st.dataframe(monthly[["Period","Total","Phishing","Clicked","Reported","Rate"]],
                     use_container_width=True, hide_index=True)

    with tab3:
        st.markdown('<div class="section-title">Employee Risk Table</div>', unsafe_allow_html=True)
        if "employee" in df.columns:
            emp = df[["employee","department","is_phishing","clicked","reported","date"]].copy()
            emp["date"] = emp["date"].dt.strftime("%Y-%m-%d")
            emp.columns = ["Employee","Department","Phishing","Clicked","Reported","Date"]
            emp["Risk"] = emp.apply(
                lambda r: "🔴 HIGH" if r["Clicked"]==1 and r["Phishing"]==1
                          else ("🟡 MEDIUM" if r["Phishing"]==1 and r["Reported"]==1 else "🟢 LOW"), axis=1)
            st.dataframe(emp, use_container_width=True, hide_index=True)
        else:
            st.info("No employee data available.")

    with tab4:
        st.markdown('<div class="section-title">Run Phishing Simulation</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-family:\"Share Tech Mono\",monospace;font-size:0.78rem;color:#5a7a9a;margin-bottom:1rem;'>Configure and launch a simulated phishing campaign. Results are saved to the CSV and metrics update immediately.</p>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            dept_filter    = st.selectbox("TARGET DEPARTMENT", ["All"] + DEPARTMENTS)
            n_employees    = st.slider("NUMBER OF EMPLOYEES", min_value=5, max_value=30, value=10, step=1)
            sim_date       = st.date_input("SIMULATION DATE", value=date.today())
        with c2:
            click_rate_pct  = st.slider("SIMULATED CLICK RATE %",   min_value=0, max_value=100, value=40, step=5,
                                        help="Percentage of employees who will click the phishing link")
            report_rate_pct = st.slider("SIMULATED REPORT RATE %",  min_value=0, max_value=100, value=30, step=5,
                                        help="Percentage of non-clickers who will report the email")

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        if st.button("🚀 LAUNCH SIMULATION", use_container_width=False):
            with st.spinner("Running simulation..."):
                new_rows = run_simulation(dept_filter, n_employees, click_rate_pct, report_rate_pct, sim_date)
                st.session_state.df = load_data()   # reload full dataset

            clicked_n  = int(new_rows["clicked"].sum())
            reported_n = int(new_rows["reported"].sum())
            st.markdown(f"""
            <div style='background:rgba(0,212,255,0.07);border:1px solid rgba(0,212,255,0.25);
                        border-left:4px solid #00d4ff;padding:1rem 1.2rem;border-radius:3px;
                        font-family:"Share Tech Mono",monospace;color:#00d4ff;font-size:0.85rem;
                        line-height:2;'>
                ✓ SIMULATION COMPLETE<br>
                <span style='color:#c9d1e0;'>
                Emails sent: <b>{n_employees}</b> &nbsp;·&nbsp;
                Clicked: <b style='color:#ff3860;'>{clicked_n}</b> &nbsp;·&nbsp;
                Reported: <b style='color:#00e676;'>{reported_n}</b> &nbsp;·&nbsp;
                Department: <b>{dept_filter}</b>
                </span><br>
                <span style='color:#5a7a9a;font-size:0.72rem;'>
                Metrics and charts have been updated. Switch to Overview or Trends to see the changes.
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-title">New Simulation Results</div>', unsafe_allow_html=True)
            display = new_rows[["employee","department","clicked","reported","date"]].copy()
            display.columns = ["Employee","Department","Clicked","Reported","Date"]
            display["Result"] = display.apply(
                lambda r: "🔴 CLICKED" if r["Clicked"]==1 else ("🟢 REPORTED" if r["Reported"]==1 else "⚪ NO ACTION"), axis=1)
            st.dataframe(display[["Employee","Department","Result","Date"]], use_container_width=True, hide_index=True)

            st.rerun()

    with tab5:
        st.markdown('<div class="section-title">AI-Powered Email Analysis</div>', unsafe_allow_html=True)
        st.markdown("<p style='font-family:\"Share Tech Mono\",monospace;font-size:0.8rem;color:#5a7a9a;'>Paste the raw body of a suspicious email below.</p>", unsafe_allow_html=True)
        email_text = st.text_area("EMAIL BODY", height=160,
                                  placeholder="e.g. Your account has been suspended. Click here to verify immediately...")
        if st.button("⚡ ANALYZE EMAIL", use_container_width=False):
            if email_text.strip():
                # Support both old ai_detector (predict_email only) and new (predict_email_detail)
                try:
                    detail = predict_email_detail(email_text)
                    prediction = detail.get("prediction", predict_email(email_text))
                    confidence = detail.get("confidence", None)
                    triggers   = detail.get("triggers", [])
                except Exception:
                    prediction = int(predict_email(email_text))
                    confidence = None
                    triggers   = []

                conf_html = f"&nbsp;<span style='font-size:0.75rem;color:#aa2040;'>CONFIDENCE: {confidence}%</span>" if confidence else ""
                conf_safe = f"&nbsp;<span style='font-size:0.75rem;color:#2a6040;'>CONFIDENCE: {confidence}%</span>" if confidence else ""

                if prediction == 1:
                    triggers_html = ""
                    if triggers:
                        kws = ", ".join(f'<code style="color:#ffb400;background:rgba(255,180,0,0.1);padding:1px 5px;border-radius:2px;">{t}</code>' for t in triggers)
                        triggers_html = f"<div style='margin-top:0.6rem;font-size:0.72rem;color:#7a6030;'>Trigger keywords: {kws}</div>"
                    st.markdown(f"""
                    <div style='background:rgba(255,56,96,0.1);border:1px solid rgba(255,56,96,0.4);
                                border-left:4px solid #ff3860;padding:1rem;border-radius:3px;
                                font-family:"Share Tech Mono",monospace;color:#ff3860;font-size:0.9rem;'>
                        THREAT DETECTED{conf_html}<br>
                        <span style='font-size:0.75rem;color:#7a3040;display:block;margin-top:0.4rem;'>
                        Do not click any links. Report to IT Security immediately.</span>
                        {triggers_html}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background:rgba(0,230,118,0.08);border:1px solid rgba(0,230,118,0.3);
                                border-left:4px solid #00e676;padding:1rem;border-radius:3px;
                                font-family:"Share Tech Mono",monospace;color:#00e676;font-size:0.9rem;'>
                        EMAIL APPEARS SAFE{conf_safe}<br>
                        <span style='font-size:0.75rem;color:#2a6040;display:block;margin-top:0.4rem;'>
                        Remain vigilant. Always verify sender identity for sensitive requests.</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.warning("Please paste email content to analyse.")

# ── Entry ─────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    login()
else:
    dashboard()