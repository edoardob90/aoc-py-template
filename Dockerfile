FROM alpine:latest

# Install Python 3 and required dependencies
RUN apk add --no-cache bash git python3 python3-dev py3-pip build-base tzdata

# Set the timezone
RUN cp /usr/share/zoneinfo/America/New_York /etc/localtime && \
    echo "America/New_York" > /etc/timezone

# Install Pandoc
RUN apk add --no-cache pandoc

# Set the working directory
WORKDIR /
RUN mkdir -p output

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy template files
COPY copier/ template/

COPY entrypoint.py .

# Set the entrypoint command
ENTRYPOINT ["/entrypoint.py"]
