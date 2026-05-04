FROM python:3.10-slim

RUN addgroup --system appuser && adduser --system --group appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
