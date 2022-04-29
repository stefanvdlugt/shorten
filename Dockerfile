FROM python:slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN python -m venv venv && . venv/bin/activate && pip install -r requirements.txt && pip install gunicorn

COPY shorten shorten/
COPY migrations migrations/
COPY config.py run.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENV FLASK_APP run.py
EXPOSE 5000

ENV BASEDIR /config/

ENTRYPOINT ["./entrypoint.sh"]
