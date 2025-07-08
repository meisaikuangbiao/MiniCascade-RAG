# 1. Base Image
# Use a slim Python image matching the project's version
FROM python:3.11-slim

# 2. Set Environment Variables
# Prevents Python from writing pyc files and buffers stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Install uv
# Install the uv package manager
COPY --from=ghcr.io/astral-sh/uv:0.7.12 /uv /uvx /bin/


# 4. Set Working Directory
ADD . /app
WORKDIR /app

# 5. Copy and Install Dependencies
# Copy dependency definition files first to leverage Docker cache
COPY pyproject.toml uv.lock ./
# Install dependencies using uv sync for a reproducible environment
RUN uv sync --locked

# 6. Copy Application Code
# Copy the rest of the application code
COPY . .

# 7. Expose Port
# Expose the default port for Gradio applications
EXPOSE 7860

# 8. Set Default Command
# Run the Gradio application, binding to 0.0.0.0 to make it accessible outside the container
CMD ["uv", "run", "app/ui/chatbot_v1.py"]

