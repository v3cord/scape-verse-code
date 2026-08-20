FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by LightGBM (libgomp1 for OpenMP thread management)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code including app/ml/lgbm_model.txt
COPY . .

# Expose FastAPI backend port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start FastAPI server using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
