# Use an official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the requirements.txt first (for better caching)
COPY requirements.txt .

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY . .

# Expose the port the app will run on
EXPOSE 8001

# Command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

