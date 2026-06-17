FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-api.txt .

RUN pip install --no-cache-dir -r requirements-api.txt

COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8000

WORKDIR /app/src/api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]