FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set up user with UID 1000 (standard for Hugging Face Spaces)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy requirements and install dependencies
# We use --chown=user to ensure the new user owns the files
COPY --chown=user requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Pre-download the PyTorch Faster R-CNN model weights during image build.
# This ensures the container starts up instantly on Hugging Face Spaces and avoids runtime download issues.
RUN python -c "from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights; fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)"

# Copy the application code
COPY --chown=user . .

# Expose port 7860 (Hugging Face Spaces default port)
EXPOSE 7860

# Set production environment flags and default port
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
ENV PORT=7860

# Run the application
CMD ["python", "app.py"]
