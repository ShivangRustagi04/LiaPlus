from flask import Blueprint, jsonify, request, current_app, session, render_template
from ..services.sentiment import get_sentiment_service, SentimentService
from typing import Dict, List

bp = Blueprint("chat", __name__, url_prefix="")

_sentiment: SentimentService = None

def _ensure_sentiment():
    global _sentiment
    if _sentiment is None:
        kind = current_app.config.get("SENTIMENT_PROVIDER", "vader")
        _sentiment = get_sentiment_service(kind)

def ensure_history():
    session.setdefault("history", [])  # list of dicts: {speaker, text, sentiment}

@bp.route("/")
def index():
    ensure_history()
    return render_template("index.html")

@bp.route("/api/send", methods=["POST"])
def send():
    _ensure_sentiment()
    ensure_history()
    if not request.is_json:
        return jsonify({"error":"JSON body required"}), 400
    payload = request.get_json()
    text = payload.get("text", "")
    if not isinstance(text, str) or not text.strip():
        return jsonify({"error":"`text` must be a non-empty string"}), 400
    text = text.strip()
    scores = _sentiment.analyze(text)
    label = _sentiment.label_from_compound(scores["compound"])
    user_entry = {"speaker":"User", "text": text, "sentiment": {"compound": scores["compound"], "label": label}}
    history = session["history"]
    history.append(user_entry)
    # Simple bot reply logic (replaceable)
    if label == "Negative":
        bot_text = "I'm sorry to hear that. Could you tell me more?"
    elif label == "Positive":
        bot_text = "That's wonderful — I'm glad to hear it. Anything else?"
    else:
        bot_text = "Thanks for sharing. How can I help further?"
    bot_entry = {"speaker":"Bot", "text": bot_text}
    history.append(bot_entry)
    session["history"] = history
    return jsonify({"status":"ok", "user_sentiment": user_entry["sentiment"], "bot_reply": bot_text}), 201

@bp.route("/api/history", methods=["GET"])
def history():
    ensure_history()
    return jsonify({"history": session["history"]})

@bp.route("/api/summary", methods=["GET"])
def summary():
    ensure_history()
    user_entries = [m for m in session["history"] if m.get("speaker") == "User" and m.get("sentiment")]
    compounds = [m["sentiment"]["compound"] for m in user_entries]
    if not compounds:
        return jsonify({"avg_compound": 0.0, "count": 0, "overall_label": "Neutral", "distribution": {"Positive":0,"Neutral":0,"Negative":0}, "trend":"Stable"})
    avg = sum(compounds)/len(compounds)
    dist = {"Positive":0,"Neutral":0,"Negative":0}
    for c in compounds:
        dist[_sentiment.label_from_compound(c)] += 1
    half = len(compounds)//2
    first = sum(compounds[:half])/(half or 1)
    second = sum(compounds[half:])/(len(compounds)-half or 1)
    if second - first > 0.05:
        trend = "Improving"
    elif first - second > 0.05:
        trend = "Worsening"
    else:
        trend = "Stable"
    overall_label = _sentiment.label_from_compound(avg)
    return jsonify({"avg_compound": avg, "count": len(compounds), "overall_label": overall_label, "distribution": dist, "trend": trend})
