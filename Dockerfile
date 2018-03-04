FROM python:3.6

# Install required packages.
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    wget \
    gettext \
    libxmlsec1-dev \
  && rm -rf /var/lib/apt/lists/*

# Download and install dockerize.
# Needed so the web container will wait for PostgreSQL to start.
ENV DOCKERIZE_VERSION v0.4.0
RUN wget --no-verbose https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1
ENV STATIC_ROOT=/usr/src/app/static/

EXPOSE 8000
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application's code
COPY . /usr/src/app

# Run the app
CMD ["./scripts/run.sh"]
