from textblob import TextBlob

# Agriculture issue keywords
issue_keywords = {
    "Irrigation": ["water", "irrigation", "rain", "drought"],
    "Fertilizer": ["fertilizer", "manure", "urea"],
    "Crop Disease": ["disease", "infection", "pest"],
    "Market Price": ["price", "market", "selling"],
    "Weather": ["weather", "storm", "heat", "flood"]
}


def detect_issue(text):

    text = text.lower()

    detected_issues = []

    for issue, keywords in issue_keywords.items():

        for word in keywords:

            if word in text:
                detected_issues.append(issue)
                break

    if len(detected_issues) == 0:
        detected_issues.append("General")

    return detected_issues


def analyze_sentiment(text):

    analysis = TextBlob(text)

    polarity = analysis.sentiment.polarity

    text_lower = text.lower()

    # Agriculture neutral keywords
    neutral_words = [
        "average",
        "normal",
        "okay",
        "fine",
        "moderate",
        "usual",
        "stable"
    ]

    # Check neutral words
    if any(word in text_lower for word in neutral_words):
        sentiment = "NEUTRAL"

    else:

        if polarity > 0.2:
            sentiment = "POSITIVE"

        elif polarity < -0.2:
            sentiment = "NEGATIVE"

        else:
            sentiment = "NEUTRAL"

    # Detect issues
    issues = detect_issue(text)

    return {
        "sentiment": sentiment,
        "confidence": round(abs(polarity) * 100, 2),
        "issues": issues
    }