FROM python:3.11-alpine
LABEL authors="Plamen Ivanov"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /app/
RUN pip install pip --upgrade
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]