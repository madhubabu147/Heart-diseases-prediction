FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (needed for XGBoost/CatBoost)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["python", "app.py"]