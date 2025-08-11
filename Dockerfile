# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy the dependency files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv sync --system

# Copy the application code into the container
COPY ./vitra_ai /app/vitra_ai

# Copy the entrypoint script
COPY entrypoint.sh .

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

# Set the entrypoint for the container
ENTRYPOINT ["./entrypoint.sh"]

# Expose the port the app runs on
EXPOSE 8000
