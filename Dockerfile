FROM python:3.11-alpine

WORKDIR /app

ENV DJANGO_SUPERUSER_NAME=${DJANGO_SUPERUSER_NAME:-admin}
ENV DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@example.com}
ENV DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-admin}

COPY requirements.txt .
RUN pip install -U --require-hashes --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py createsuperuser --noinput --username ${DJANGO_SUPERUSER_NAME} --email ${DJANGO_SUPERUSER_EMAIL}

EXPOSE 8182
CMD ["granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "8182", "piepi.wsgi_docker:application"]
