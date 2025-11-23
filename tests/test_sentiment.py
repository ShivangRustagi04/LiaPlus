from app.services.sentiment import get_sentiment_service

def test_vader_basic():
    svc = get_sentiment_service("vader")
    pos = svc.analyze("I love this!")
    neg = svc.analyze("This is terrible.")
    assert pos["compound"] > 0
    assert neg["compound"] < 0
    assert svc.label_from_compound(pos["compound"]) == "Positive"
