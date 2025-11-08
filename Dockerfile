FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run potrzebuje portu 8080
ENV PORT=8080

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8080"]
