# start by pulling the python image
FROM python:3.14.2-alpine

WORKDIR /app

COPY flaskr/requirements.txt requirements.txt

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY . .

ENV FLASK_APP=flaskr
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--debug"]