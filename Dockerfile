FROM python:latest

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY config.py .

RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "main.py"]