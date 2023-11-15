FROM python:3.11-slim

LABEL description="Cadastral number test case: external server" \
      version="1.0" \
      maintainer="TheSuncatcher222" \
      deployer="https://github.com/TheSuncatcher222/"

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

CMD python main.py
