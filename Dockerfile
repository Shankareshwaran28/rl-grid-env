# Base Python image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git git-lfs ffmpeg libsm6 libxext6 cmake rsync libgl1 curl && \
    rm -rf /var/lib/apt/lists/* && git lfs install

# Install Node.js (if your project uses it)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies including Gradio 6.x and Spaces
RUN --mount=target=/tmp/requirements.txt,source=requirements.txt \
    pip install --no-cache-dir -r /tmp/requirements.txt \
    gradio[oauth,mcp]==6.10.0 \
    "uvicorn>=0.14.0" \
    "websockets>=10.4" \
    spaces>=0.48.1

# Expose Gradio port
EXPOSE 7860

# Run your app (change if your main file is different)
CMD ["python", "app.py"]