# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the working directory
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt 
# Copy the rest of the application code to the working directory
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Command to run the application (without running migrations in the build process)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
