FROM python:3.11 as python-base
RUN mkdir app
WORKDIR  /app
COPY pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install 

# Copy Application
COPY . /app/microservices/api_gateway

# Run Application
EXPOSE 4500