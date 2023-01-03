FROM python:3.9
ENV PORT 8080
ENV HOST 0.0.0.0
RUN apt-get update -y && \
    apt-get install -y python3-pip
RUN pip install pipenv
WORKDIR /app
COPY . /app
RUN pipenv install flask flask-restful gunicorn requests maxminddb psycopg2-binary SQLAlchemy cloud-sql-python-connector pg8000 google-cloud-logging flask-cors
RUN pipenv install --deploy --system
EXPOSE 8080
CMD ["gunicorn", "app:app", "-b", ":8080", "--timeout", "300"]