# Traffic Detection and Classification Dashboard

An interactive, deep learning-powered traffic scene analysis system featuring a premium monochrome dashboard, real-time object detection (using Faster R-CNN), and dynamic visualization modes.

---

## Key Features

1. **Monochrome Dark UI Dashboard**: A state-of-the-art dark-themed web user interface featuring modern typography, glassmorphism card panels, smooth progress bar animations, and side-by-side comparison tabs.
2. **Deep Learning Model (Faster R-CNN)**: Detects and classifies various objects in traffic scenes (cars, trucks, buses, motorcycles, pedestrians) using a pre-trained PyTorch model.
3. **Black & White Detection Mode**: Toggle grayscale processing to transform the background scene into black and white while retaining full-color bounding boxes, making detections visually stand out.
4. **Local Command Line Interface (CLI)**: A command-line script (`detect.py`) to run inferences directly on images in your terminal.
5. **Cross-Platform & Deployment Ready**: Fully compatible with Linux, macOS, and Windows. Ready for deployment on cloud services (Render, Railway, Docker) with environment-aware configurations.

---

## Installation

Ensure you have Python 3.8+ installed, then run:

```bash
pip install -r requirements.txt
```

*This will install PyTorch, Torchvision, OpenCV, Matplotlib, Pillow, and Flask.*

---

## Running the Web Dashboard

Start the local Flask server:

```bash
python app.py
```

Then, open your web browser and navigate to:
```text
http://127.0.0.1:5000
```

*Click **"try with a demo image"** to immediately test the system, or upload your own traffic scene.*

---

## Running the CLI Tool

To perform inference directly via terminal command line:

```bash
# General usage
python detect.py --image <path_to_image>

# Toggle display window output
python detect.py --image traffic.jpg --show

# Specify custom output path
python detect.py --image traffic.jpg --output results/my_output.jpg
```

---

## Project Structure

- `app.py`: Flask application server with API inference endpoints.
- `detect.py`: CLI script for command-line inference.
- `Ex5.ipynb`: Pre-configured Jupyter Notebook optimized to run locally and in Google Colab.
- `templates/index.html`: Web dashboard page styling and logic.
- `static/`: Stores uploaded images, output results, and demo image configurations.
- `requirements.txt`: Python package dependency listings.
- `.gitignore` & `.gitkeep`: Git workspace configurations ignoring raw media cache.

---

## Deployment

Refer to the complete [Deployment Guide](./deployment_guide.md) file inside the repository for details on setting up cloud servers, Docker containers, or local network sharing.
