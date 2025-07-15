# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# This should include your app.py, requirements.txt, and any other app files
COPY . /app

# Install any needed packages specified in requirements.txt
# Added --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the FLASK_APP environment variable to tell Flask which file to run
ENV FLASK_APP=app.py

# Command to run the Flask application using its built-in development server
# --host=0.0.0.0 makes the app accessible from outside the container
# --port=5000 specifies the port Flask listens on
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]