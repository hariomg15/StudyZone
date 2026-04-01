FROM python:3.11-slim-bookworm

WORKDIR /app
# requirements file in repository is 'requirements.txt' (lowercase r)
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]