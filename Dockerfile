# A tiny production-ish image for the Workspaces API.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV HOST=0.0.0.0 \
    PORT=5000 \
    FLASK_DEBUG=false

EXPOSE 5000

CMD ["python", "app.py"]
