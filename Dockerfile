# Base image
FROM python:3.12-slim

# Buffering stdout
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies (important for pyscopg2)

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt /tmp/requirements.txt
COPY requirements.dev.txt /tmp/requirements.dev.txt



# System dependencies (important for pyscopg2)
ARG DEV=false
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        libffi-dev \
        postgresql-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp 

# Create non-root user
RUN adduser --disabled-password --no-create-home app-user


# Copy project source
COPY src/ ./src

# Environment variables
ENV PYTHONPATH=/app
ENV PATH="/py/bin:$PATH"


# Switch to non-root user
USER app-user

