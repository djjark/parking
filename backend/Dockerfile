# Use an official Python runtime as a parent image
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --upgrade pip  # Upgrade pip to avoid issues
RUN pip install -r requirements.txt  # Install the dependencies

# Expose port 5000 to the world outside the container
EXPOSE 5000

# Run the Flask app with Gunicorn (a production-ready web server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
