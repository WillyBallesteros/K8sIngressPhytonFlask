FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE 3020

ENV FLASK_APP=src/main.py

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=3020"]
