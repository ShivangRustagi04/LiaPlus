FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m nltk.downloader -d /usr/local/share/nltk_data vader_lexicon
EXPOSE 8000
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn_conf.py"]
