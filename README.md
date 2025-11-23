# Chatbot with Sentiment Analysis
```
The chatbot uses NLTK VADER (Valence Aware Dictionary and sEntiment Reasoner) as its sentiment analysis engine.
VADER is a rule-based, lexicon-driven sentiment analyzer specifically designed for short, informal, conversational text such as chats, social media posts, and real-time messages.

⭐ Why VADER is suitable for chatbots

Built for social and conversational language

Understands slang, emojis, capitalization emphasis ("I LOVE this"), and punctuation ("!!!")

Fast and lightweight → ideal for real-time analysis

No model training needed

🔬 How VADER Works

VADER uses:

A sentiment lexicon – a dictionary where each word has a pre-assigned emotional intensity score
Example:

“terrible” → -2.5

“good” → +1.9

“amazing” → +3.2

Contextual rules, such as:

Degree modifiers (e.g., "very", "extremely")

Negation handling ("not happy")

Punctuation emphasis ("good!!!")

Capitalization ("AWESOME")

Emojis / emoticons 🙂

A polarity output, consisting of:

pos → ratio of positive sentiment

neu → ratio of neutral sentiment

neg → ratio of negative sentiment

compound → normalized overall score from -1 to 1
```
## Clone or download project
    ```bash
    git clone https://github.com/ShivangRustagi04/LiaPlus.git
    ```
    ```
    cd LiaPlus
    ```

## How to Run
1. Create virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   python -m nltk.downloader vader_lexicon
   ```
3. Run the application:
   ```
   flask run 
   ```
   or:
   ```
   python wsgi.py
   ```

## Chosen Technologies
- **Python 3**
- **Flask** (web framework)
- **NLTK VADER** (sentiment analysis)
- **Flask-Session** (session handling)
- **HTML, CSS, JavaScript** (frontend)
- **Gunicorn** (production server)
- **Docker** (containerization)

## Explanation of Sentiment Logic
- Each user message is analyzed using **VADER**.
- VADER produces four scores: pos, neu, neg, and compound.
- Final classification uses:
  - compound <= -0.05 → Negative  
  - compound >= 0.05 → Positive  
  - otherwise → Neutral  
- Conversation-level sentiment is computed using:
  - Average compound score  
  - Label distribution  
  - Trend detection (first half vs second half comparison)

## Status of Tier 2 Implementation
✔ **Tier 1 fully completed**  
✔ **Tier 2 implemented**, including:
- Per-message sentiment
- Frontend display of sentiment
- Trend analysis (bonus enhancement)

## File Structure

```
chatbot-sentiment/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   └── chat.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── sentiment.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/
│   ├── conftest.py
│   ├── test_sentiment.py
│   └── test_chat_routes.py
│
├── .env.example
├── requirements.txt
├── Dockerfile
├── gunicorn_conf.py
├── wsgi.py
└── README.md

```

## Tests
The project includes unit and integration tests using **pytest**.

### Run all tests
From the project root (where `tests/` lives), with your virtualenv activated:
```bash
# ensure project root on PYTHONPATH if needed (Windows PowerShell)
$env:PYTHONPATH = (Get-Location).Path

# then
pytest -q
```

### Run a single test file
```bash
pytest tests/test_sentiment.py -q
```

### Run a single test function
```bash
pytest tests/test_sentiment.py::test_vader_basic -q
```

### Notes & Debugging
- If Python cannot find the `app` package when running tests, ensure you're in the project root and set `PYTHONPATH` (see commands above).
- Ensure the virtualenv is activated and `nltk`'s `vader_lexicon` is downloaded:
```bash
python -m nltk.downloader vader_lexicon
```
