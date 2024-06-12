#
FROM python:3.10

#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDUNBUFFERED 1

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
COPY ./run.sh /code/run.sh

#
RUN chmod +x /code/run.sh

#
ENTRYPOINT bash ./run.sh