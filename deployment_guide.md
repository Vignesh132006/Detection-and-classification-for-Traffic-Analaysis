# Deployment Guide - Traffic Detection Dashboard

This guide provides instructions for deploying and hosting the Traffic Detection and Classification Flask web application in different environments.

---

## 🚀 1. Local Network Sharing (Easiest)

To access the dashboard from other devices (like smartphones, tablets, or other computers) connected to the same Wi-Fi/local network:

1. Connect the host computer to the network.
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Locate the host computer's local IP address (printed in the terminal output as `Running on http://<host-ip-address>:5000`, e.g., `http://192.168.1.15:5000`).
4. On any other device on the same local network, open a web browser and navigate to:
   ```text
   http://<host-ip-address>:5000
   ```

---

## 🐳 2. Containerized Deployment (Docker)

Docker is the recommended approach for deploying this application to cloud platforms, virtual machines, or local environments, as it bundles Python packages (like PyTorch and OpenCV) along with their required system dependencies.

### Local Docker Build & Run
1. Make sure you have Docker installed.
2. Build the Docker image:
   ```bash
   docker build -t traffic-analytics .
   ```
3. Run the container:
   ```bash
   docker run -p 5000:5000 --env FLASK_DEBUG=false traffic-analytics
   ```
4. Access the web app at `http://localhost:5000`.

---

## ☁️ 3. Cloud Deployment

> [!IMPORTANT]
> **Resource Requirements:**
> Because this application runs a deep learning model (**Faster R-CNN** using **PyTorch**), it has a heavy memory footprint (~1GB+). Ensure your cloud hosting plan has **at least 2GB of RAM** to prevent Out-Of-Memory (OOM) build or runtime errors.

### Option A: Render (Docker-based, Recommended)
Render allows you to deploy containerized applications directly:
1. Push your code (including the `Dockerfile`) to a GitHub repository.
2. Log in to [Render](https://render.com/) and click **New** -> **Web Service**.
3. Connect your GitHub repository.
4. Set the **Language** to `Docker` (Render will automatically detect your `Dockerfile`).
5. Choose a tier with at least 2GB of RAM (e.g., Starter tier).
6. Click **Deploy Web Service**.

### Option B: Hugging Face Spaces (Docker-based, Free Tier Available)
Hugging Face Spaces offers a free Docker SDK space with 16GB CPU RAM:
1. Create a Hugging Face account and create a new **Space**.
2. Select **Docker** as the SDK (instead of Streamlit or Gradio).
3. Select the **Blank** template.
4. Clone the space repository locally or upload your project files directly through the HF web interface.
5. Hugging Face will automatically read the `Dockerfile`, build it, and expose the app.
   > [!NOTE]
   > Hugging Face Spaces expose port `7860` by default. You can configure Flask to run on port `7860` by setting the environment variable `PORT=7860` in the Space settings, or let the Dockerfile handle it dynamically.

### Option C: Railway
Railway is another quick way to deploy:
1. Connect your GitHub repository to [Railway](https://railway.app/).
2. Railway will automatically detect the `Dockerfile` and build it.
3. Add a custom domain or use the provided Railway domain to access your application.
