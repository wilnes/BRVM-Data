# Base image
FROM python:3.12-alpine

# Buffering stdout
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt  .

# Install system dependencies (including Postgres client)
RUN apk add --no-cache gcc libpq-dev postgresql-client

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN adduser --disabled-password --no-create-home app-user


# Copy project source
COPY . .

# Scripts enable
RUN chmod +x /app/scripts/wait_for_db.sh

# Environment variables
ENV PYTHONPATH=/app
ENV PATH="/py/bin:$PATH"


# Switch to non-root user
USER app-user

