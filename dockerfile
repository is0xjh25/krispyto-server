# Use a base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . . 

ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL True

# Install MPICH
RUN apt-get update && apt-get install -y mpich
RUN pip install --upgrade pip

# Install dependencies from a list
RUN pip install -r requirements.txt

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["flask", "run","--host","0.0.0.0","--port","8000"]