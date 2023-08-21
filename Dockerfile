FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -U --require-hashes --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py migrate && \
    python manage.py collectstatic --noinput

EXPOSE 8182
CMD ["granian", "--interface", "wsgi", "--host", "0.0.0.0", "--port", "8182", "piepi.wsgi_docker:application"]
