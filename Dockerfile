FROM python:3.14.3-slim AS builder

WORKDIR /build

COPY pyproject.toml .
COPY app/ app/

RUN pip install --no-cache-dir .

FROM python:3.14.3-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY app/ app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
