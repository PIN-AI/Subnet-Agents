# Build Stage
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install Python dependencies (assuming you have a requirements.txt)
# The SDK package lists required packages like grpcio, protobuf, aiohttp, etc.
#
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Final Stage
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages and code from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/agent1.py /app/agent1.py

# This command runs your agent application
CMD ["python", "agent1.py"]
