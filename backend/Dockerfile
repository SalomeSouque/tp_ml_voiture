FROM python:3.11-slim

LABEL maintainer="salome.souque@email.com"
LABEL version="1.0.0"
LABEL description="API ML de prédiction de prix de voiture"
LABEL org.opencontainers.image.source="https://github.com/SalomeSouque/tp_ml_voiture"

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app \
    POSTGRES_HOST=db \
    POSTGRES_PORT=5432

RUN useradd -m -u 1000 dataeng && \
    chown -R dataeng:dataeng /app

USER dataeng

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
