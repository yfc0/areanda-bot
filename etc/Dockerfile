FROM python:3.11


WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTONPATH}:/usr/src"
ENV TZ="Asya/Almaty"

COPY ./etc/logging_config.ini /etc/logging_config.ini

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./src ./


CMD ["python", "main.py"]
