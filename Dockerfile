FROM python:latest
LABEL maintainer="Genaro Vogelius <genagevo@gmail.com>"
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
# Run Django management commands to set up the database
RUN python manage.py makemigrations && python manage.py migrate
