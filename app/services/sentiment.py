from typing import Dict, Optional
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    _VADER_AVAILABLE = True
except Exception:
    _VADER_AVAILABLE = False

class SentimentService(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Dict[str, float]:
        ...

    @abstractmethod
    def label_from_compound(self, compound: float) -> str:
        ...

class VaderSentimentService(SentimentService):
    def __init__(self):
        if not _VADER_AVAILABLE:
            logger.error("VADER not available. Ensure 'nltk' and 'vader_lexicon' are installed.")
            raise RuntimeError("VADER unavailable")
        self._sia = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> Dict[str, float]:
        text = text or ""
        return self._sia.polarity_scores(text)

    def label_from_compound(self, compound: float) -> str:
        if compound <= -0.05:
            return "Negative"
        if compound >= 0.05:
            return "Positive"
        return "Neutral"

def get_sentiment_service(kind: Optional[str] = None) -> SentimentService:
    kind = kind or "vader"
    if kind == "vader":
        return VaderSentimentService()
    raise ValueError(f"Unknown sentiment service: {kind}")
