# Use official Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg2 && \
    apt-get install -y libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libgbm1 libxshmfence1 libxcomposite1 libxdamage1 libxrandr2 libxinerama1 libpango-1.0-0 libcairo2 libatspi2.0-0 libdrm2 libxkbcommon0 && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install --with-deps

# Copy app code
COPY . .

# Expose port
EXPOSE 8082

# Run the app
CMD ["python", "app.py"] 