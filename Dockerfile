# Use an official lightweight Python base image
FROM python:3.14-slim

# Install uv for high-performance dependency resolution and caching
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition files first for optimal Docker layer caching
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen --no-install-project

# Copy the rest of the application files to the container
COPY . .

# Expose port 8080 (standard for Cloud Run)
EXPOSE 8080

# Run the FastAPI app using uvicorn. It reads the PORT environment variable 
# set by the cloud provider, defaulting to 8080.
CMD ["sh", "-c", "uv run uvicorn chatbot.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
