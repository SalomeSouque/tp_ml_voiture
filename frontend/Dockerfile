FROM python:3.14-slim

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
