FROM python:3.12-slim

WORKDIR /app

# Copy dependency files first for better caching
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
