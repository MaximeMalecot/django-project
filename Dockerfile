FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ./docker/requirements.txt /code/

RUN pip install -r requirements.txt

COPY ./code/ /code/

COPY docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]