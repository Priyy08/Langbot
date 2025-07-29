# Stage 1: Use the official Python slim image for a smaller footprint.
# Using a specific version ensures a reproducible build.
FROM python:3.11-slim

# Set the working directory inside the container. All subsequent commands
# will be run from this directory.
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files to disk
# and to run in unbuffered mode, which is better for logging.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the container.
# This is done as a separate step to leverage Docker's layer caching.
# If the requirements don't change, this layer will be cached, speeding up
# future builds.
COPY ./requirements.txt .

# Install the Python dependencies.
# --no-cache-dir reduces the image size by not storing the pip cache.
# --upgrade pip ensures we have the latest version of the package installer.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's source code into the container.
# This includes the `app` directory with all your Python modules.
# The .dockerignore file (usually the same as .gitignore) will prevent
# unnecessary files like .env or __pycache__ from being copied.
COPY ./app /app/app

# Expose the port the app runs on.
# This is documentation for the user and allows for easier inter-container
# communication. The FastAPI app is configured to run on port 8000.
EXPOSE 8000

# Define the command to run the application when the container starts.
# We use uvicorn to run the FastAPI application.
# --host 0.0.0.0 makes the server accessible from outside the container.
# The exec form (JSON array) is the preferred syntax for CMD.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]