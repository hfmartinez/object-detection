FROM python:3.11 as python-base
RUN mkdir app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
WORKDIR  /app
COPY pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

# Copy Application
COPY . /app

# Run Application
EXPOSE 6000