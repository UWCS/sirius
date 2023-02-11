FROM python:3.11

WORKDIR /app

RUN pip install pipenv

COPY Pipfile Pipfile.lock /app

# system deps
RUN apt-get update && apt-get install -y libxmlsec1 libxmlsec1-dev

RUN pipenv install --system

COPY sirius /app/sirius


CMD ["uvicorn", "sirius:app", "--host", "0.0.0.0", "--port", "8080"]