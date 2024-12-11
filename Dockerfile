FROM python:3.10-slim

WORKDIR /pythonProject10

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]