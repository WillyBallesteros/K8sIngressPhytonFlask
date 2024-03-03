FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

EXPOSE 3006

ENV FLASK_APP=src/main.py
ENV POST_SERVICE_URL=http://localhost:3001
ENV ROUTE_SERVICE_URL=http://localhost:3002
ENV OFFER_SERVICE_URL=http://localhost:3003
ENV SCORE_SERVICE_URL=http://localhost:3020

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0", "--port=3006"]
