# Use official Python base image
FROM python:3.11

# Set working directory in container
WORKDIR /app

# Copy and install dependencies
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt

# Copy the full project into the container
COPY . .

# Set Python path to make "app" package discoverable
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

