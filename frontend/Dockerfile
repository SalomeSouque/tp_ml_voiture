FROM python:3.11-slim

LABEL maintainer="salome.souque@email.com"
LABEL version="1.0.0"
LABEL description="API ML de prédiction de prix de voiture"
LABEL org.opencontainers.image.source="https://github.com/SalomeSouque/tp_ml_voiture"

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd -m -u 1000 dataeng && \
    chown -R dataeng:dataeng /app

USER dataeng

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
