FROM python:3.11 as python-base
RUN mkdir app
RUN apt-get update 
WORKDIR  /app
COPY pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

# Copy Application
COPY . /app/