FROM alpine:latest

# Install Python 3 and required dependencies
RUN apk add --no-cache bash git python3 python3-dev py3-pip build-base tzdata

# Set the timezone
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime && \
    echo "America/New_York" > /etc/timezone

# Install Pandoc
RUN apk add --no-cache pandoc

# Set the working directory
WORKDIR /app
RUN mkdir -p output

# Create a Python virtual env
ENV VIRTUAL_ENV=/app/venv
RUN pip3 install virtualenv && python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy files
COPY copier/ template/
COPY entrypoint.py .

# Set the entrypoint command
ENTRYPOINT ["/app/entrypoint.py"]
