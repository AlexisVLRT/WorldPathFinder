FROM python:3.8

RUN mkdir /app
ENV PYTHONPATH /app
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bin/main.py"]