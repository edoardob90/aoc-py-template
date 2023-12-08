# Use Debian slim as the base image
FROM debian:stable-slim

# Install Python 3 and required dependencies
RUN apt-get update && apt-get install -y \
    bash \
    git \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    build-essential \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime && \
    echo "America/New_York" > /etc/timezone

# Install Pandoc
RUN apt-get update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app
RUN mkdir -p output

# Copy the Python requirements file
COPY requirements.txt .

# Create a virtual environment and activate it
ENV VENV_PATH="/app/venv"
RUN python3 -m venv $VENV_PATH
ENV PATH="$VENV_PATH/bin:$PATH"

# Install Python dependencies inside the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy template files
COPY copier/ template/

COPY entrypoint.py .

# Set the entrypoint command
ENTRYPOINT ["/app/venv/bin/python", "/app/entrypoint.py"]
