"""
ai_detector.py — Phishing email classifier
Uses TF-IDF + Logistic Regression (better than Random Forest for small text corpora).
Returns prediction (0=safe, 1=phishing) and a confidence percentage.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re

# ── Training data ─────────────────────────────────────────────────────────────
# 50 phishing + 50 safe = 100 balanced samples
PHISHING = [
    # Account / credential theft
    "Your account has been suspended please verify your identity immediately",
    "We detected unusual login activity please confirm your password now",
    "Your password has expired click here to reset it before your account is locked",
    "Verify your email address or your account will be permanently deleted",
    "Your account has been compromised update your credentials immediately",
    "Someone tried to access your account from an unknown device click to review",
    "Your login credentials need to be updated please click the link below",
    "Confirm your identity to restore access to your account click here",
    "We have locked your account for security reasons verify now to unlock",
    "Action required your account will be closed in 24 hours if not verified",

    # Financial / payment fraud
    "Your payment failed update your billing information immediately",
    "Your credit card has been charged please verify this transaction",
    "Urgent your bank account requires immediate verification",
    "You have a pending refund click here to claim your money now",
    "SARS tax refund of R4500 is available click to submit your bank details",
    "Your invoice is overdue please make payment immediately to avoid penalties",
    "Transfer request pending please approve this international wire transfer",
    "Your PayPal account has been limited please verify your details",
    "Congratulations you have won R50000 provide your banking details to claim",
    "Your subscription payment could not be processed update your card now",

    # Delivery / package scams
    "Your package could not be delivered click here to reschedule delivery",
    "DHL your parcel is on hold please pay R45 customs fee to release",
    "Your Takealot order has been delayed confirm your address to proceed",
    "We attempted to deliver your package please click to arrange redelivery",
    "Your shipment has been held at customs pay the clearance fee now",

    # Prize / reward scams
    "You have been selected as our lucky winner claim your prize today",
    "Click here to claim your free gift card limited time offer expires soon",
    "You are our 1000th visitor claim your exclusive reward now",
    "Congratulations you qualify for a R10000 cashback reward click to claim",
    "You have won a brand new iPhone click here to collect your prize",

    # Urgency / fear tactics
    "URGENT your computer has been infected with a virus call us immediately",
    "Security breach detected on your account immediate action required",
    "Your files have been encrypted pay R2000 in Bitcoin to restore access",
    "Final warning your account will be suspended in 12 hours",
    "Immediate response required failure to act will result in legal action",
    "Your Google account will be deactivated unless you verify now",
    "Alert we have detected suspicious transactions on your account act now",
    "Your Microsoft license has expired renew immediately to avoid disruption",
    "CRITICAL your email storage is full click here to upgrade immediately",
    "Warning your device is at risk install this security update now",

    # HR / workplace phishing
    "HR your salary payment has been delayed please verify your bank details",
    "Please review and sign the attached employment contract immediately",
    "Your leave application has been rejected click here for details",
    "Payroll update required please submit your banking details by end of day",
    "Important policy change please click to acknowledge the new HR policy",

    # Generic
    "Click this link to verify your details and avoid account suspension",
    "Enter your username and password to continue to your secure portal",
    "Your session has expired please log in again to secure your account",
    "Download the attached document to view your latest account statement",
    "Please update your personal information to keep your account active",
]

SAFE = [
    # Casual / personal
    "Lunch tomorrow at 12 the usual spot near the office",
    "Happy birthday hope you have a wonderful day",
    "Thanks for your help with the presentation yesterday it went really well",
    "Are you coming to the team braai on Saturday it should be fun",
    "Just checking in hope everything is going well with you",
    "Can we reschedule our catch up to Thursday afternoon",
    "Great work on the report this week the client was very happy",
    "Hope you had a good long weekend see you tomorrow",
    "Quick question do you have the contact details for the supplier",
    "I left my laptop charger in the boardroom can someone check",

    # Work / professional
    "Please find the agenda for Friday's quarterly review meeting attached",
    "The project timeline has been updated on SharePoint please review",
    "Reminder team standup is at 9am tomorrow in the main conference room",
    "The budget spreadsheet has been shared with you on Google Drive",
    "Please submit your timesheets by end of day Friday",
    "The client meeting has been moved to 2pm on Wednesday",
    "Can you review the attached proposal and send feedback by Thursday",
    "FYI the office will be closed on Monday for the public holiday",
    "The new onboarding checklist is available on the intranet",
    "Please complete the mandatory training module by end of this month",

    # IT / system notices (legitimate)
    "Your scheduled system maintenance is this Sunday from 2am to 4am",
    "The shared drive has been reorganised please see the new folder structure",
    "IT reminder please restart your laptop after the automatic update tonight",
    "The VPN configuration guide has been updated please see the IT wiki",
    "Your ticket has been resolved please let us know if you need further help",
    "Planned network maintenance will occur on Saturday between 10pm and 12am",
    "Software update for Microsoft Office has been pushed to all devices",
    "Your IT support request has been received reference number IT20240312",
    "The printer on the 3rd floor is back online after servicing",
    "Please use the new Zoom link for all external meetings going forward",

    # HR / admin (legitimate)
    "Your leave request for 15 April has been approved",
    "The updated leave policy document is available on the HR portal",
    "Please complete the annual performance review form by 28 March",
    "Your payslip for March is now available on the payroll portal",
    "Reminder the staff wellness day is on 20 April attendance is encouraged",
    "The recruitment drive for junior analysts starts next month",
    "Please update your emergency contact details on the HR system",
    "The office catering order for Wednesday's workshop has been confirmed",
    "Your training certificate for the compliance module has been emailed",
    "The company picnic is confirmed for 5 May please RSVP by Friday",

    # Finance / accounting (legitimate)
    "Please find the attached purchase order for your approval",
    "The Q1 budget report has been finalised and shared on SharePoint",
    "Reminder expense claims for March must be submitted by 5 April",
    "The audit team will be on site from Monday please have reports ready",
    "Your reimbursement for the conference travel has been processed",
    "The supplier invoice has been received and is pending your approval",
    "Please review the attached cost centre reconciliation for February",
    "The finance team meeting is at 3pm on Thursday in room B4",
    "Your petty cash request of R350 has been approved",
    "The year end financial close schedule has been shared with all managers",
]

emails = PHISHING + SAFE
labels = [1] * len(PHISHING) + [0] * len(SAFE)

# ── Phishing keyword signals (used for explanation) ───────────────────────────
PHISHING_KEYWORDS = [
    "verify", "suspended", "click here", "urgent", "immediately", "confirm",
    "password", "credentials", "locked", "compromised", "winner", "claim",
    "prize", "refund", "banking details", "update billing", "unusual activity",
    "limited", "expires", "action required", "warning", "alert", "encrypted",
    "customs fee", "reschedule delivery", "account will be", "your account",
]

# ── Build pipeline ────────────────────────────────────────────────────────────
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),       # unigrams + bigrams catch "click here", "act now" etc.
        max_features=500,
        sublinear_tf=True,        # dampen high-frequency terms
        stop_words="english",
    )),
    ("clf", LogisticRegression(
        C=1.0,
        max_iter=1000,
        class_weight="balanced",  # prevents bias toward majority class
        random_state=42,
    )),
])

pipeline.fit(emails, labels)

# ── Public API ────────────────────────────────────────────────────────────────
def predict_email(text: str) -> int:
    """Return 1 if phishing, 0 if safe."""
    return int(pipeline.predict([text])[0])


def predict_email_detail(text: str) -> dict:
    """
    Returns a dict with:
      - prediction: int (0 or 1)
      - confidence: float 0–100
      - label: str
      - triggers: list of matched phishing keyword phrases found in text
    """
    prediction  = int(pipeline.predict([text])[0])
    proba       = pipeline.predict_proba([text])[0]
    confidence  = round(float(max(proba)) * 100, 1)
    text_lower  = text.lower()
    triggers    = [kw for kw in PHISHING_KEYWORDS if kw in text_lower]

    return {
        "prediction":  prediction,
        "confidence":  confidence,
        "label":       "PHISHING" if prediction == 1 else "SAFE",
        "triggers":    triggers,
    }