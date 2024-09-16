FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER=1

WORKDIR /app

COPY requirements.txt /src/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /src/requirements.txt

COPY . .

RUN chmod +x runners/django-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["runners/django-entrypoint.sh"]
