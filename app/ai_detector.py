# ── ai_detector.py ──

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# ── Sample Email Data ──
emails = [
    # Phishing (label = 1)
    "Your account is suspended verify now",
    "Reset your password immediately",
    "Invoice attached please review urgently",
    "Click here to claim your prize",
    "Verify your identity or your account will be closed",
    "Urgent action required your payment failed",
    "Your package could not be delivered click to reschedule",
    "Login attempt detected confirm your details now",
    "You have been selected for a reward enter your details",
    "Security alert unusual sign-in activity detected",
    "Your Netflix subscription has expired update billing",
    "SARS tax refund available click to claim now",
    # Safe (label = 0)
    "Lunch tomorrow at 12 the usual spot",
    "Meeting reminder quarterly review Friday 10am",
    "Please find the agenda for next week attached",
    "Happy birthday hope you have a great day",
    "Team outing this Saturday optional but fun",
    "The report has been updated on SharePoint",
    "Can we reschedule our call to Thursday",
    "Thanks for your help on the project yesterday",
]

labels = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          0, 0, 0, 0, 0, 0, 0, 0]

# ── Train TF-IDF Vectorizer and RandomForest ──
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, labels)

# ── Phishing Keywords List ──
PHISHING_KEYWORDS = [
    "account", "verify", "password", "invoice", "click", "prize",
    "identity", "urgent", "payment", "login", "reward", "security",
    "subscription", "tax", "refund", "claim", "update", "failed",
    "suspended", "detect"
]

# ── Basic Prediction Function ──
def predict_email(text):
    """
    Predict if an email is phishing (1) or safe (0).
    """
    X_new = vectorizer.transform([text])
    return model.predict(X_new)[0]

# ── Detailed Prediction Function ──
def predict_email_detail(text):
    """
    Returns detailed phishing prediction:
    - is_phishing: 0 or 1
    - confidence: probability
    - reason: explanation including triggered keywords
    - triggered_keywords: list of matched keywords
    """
    # Prediction
    is_phishing = predict_email(text)
    
    # Confidence using predict_proba
    X_new = vectorizer.transform([text])
    confidence_score = model.predict_proba(X_new)[0][is_phishing]
    
    # Detect triggered phishing keywords (case-insensitive)
    triggered_keywords = [kw for kw in PHISHING_KEYWORDS if kw.lower() in text.lower()]
    
    # Build reason
    if is_phishing:
        if triggered_keywords:
            reason = f"Suspicious keywords detected: {', '.join(triggered_keywords)}"
        else:
            reason = "Phishing indicators detected, but no specific keywords matched."
    else:
        reason = "No phishing indicators detected."
    
    # Return detailed result
    return {
        "is_phishing": int(is_phishing),
        "confidence": float(confidence_score),
        "reason": reason,
        "triggered_keywords": triggered_keywords
    }

# ── Example Usage ──
if __name__ == "__main__":
    test_email = "Please verify your account immediately to avoid suspension."
    detail = predict_email_detail(test_email)
    print(detail)