
ENTRYPOINT ["top", "-b"]

# Dockerfile
FROM python:3.11

LABEL authors="maxfriebertshauser"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./backend /code
