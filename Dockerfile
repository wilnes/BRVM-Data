# Base image
FROM python:3.12-alpine

# Buffering stdout
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies (important for pyscopg2)

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY src/ ./src

# Set PYTHONPATH so imports work
ENV PYTHONPATH=/app

# Default command
CMD ["python", "-m", "src" ]
