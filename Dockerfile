FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --break-system-packages

add src /app/src

COPY cheerlights_bot.py .

RUN chmod +x cheerlights_bot.py

CMD ./cheerlights_bot.py