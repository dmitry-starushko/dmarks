FROM python:3.12.6
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN pip install -r addons/requirements.txt

