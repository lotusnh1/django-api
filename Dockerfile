# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

