FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' myuser
USER myuser
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
