FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y awscli

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]