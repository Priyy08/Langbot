# Stage 1: Use the same base image as the backend for consistency.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Set Python environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file and install dependencies first to leverage caching.
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend application source code into the container.
# This includes the main app, pages, components, services, utils, and styles.
COPY ./app /app/app

# Expose the default Streamlit port.
EXPOSE 8501

# Define the command to run the Streamlit application.
# --server.port specifies the port to run on.
# --server.address 0.0.0.0 makes it accessible from outside the container.
# --server.enableCORS=false is a good practice when running behind a proxy,
# though Streamlit's defaults are generally fine.
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]