FROM python:latest

WORKDIR /app
RUN mkdir -p /log

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ./cheerlights_bot.py