
FROM python:3.11-slim

# Install Tesseract OCR engine
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Streamlit port
EXPOSE 8501

# Start the application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
