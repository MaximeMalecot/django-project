FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./docker/requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./code/ /code/