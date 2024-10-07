# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Fibonacci Server will listen on
EXPOSE 9090

# Run the Fibonacci Server
CMD ["python", "fibonacci_server.py"]
