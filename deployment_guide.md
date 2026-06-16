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
   # Map host port 5000 to the container port 7860 (exposed by the Dockerfile)
   docker run -p 5000:7860 --env FLASK_DEBUG=false traffic-analytics
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
Hugging Face Spaces offers a free CPU basic tier with **16GB RAM**, which is more than enough to host the Faster R-CNN PyTorch model. Because this is a custom Flask app with PyTorch and OpenCV dependencies, we deploy it using the **Docker SDK**.

#### Why our configuration is optimized for Hugging Face Spaces:
* **Non-Root User (UID 1000):** Hugging Face Spaces runs containers under user ID `1000` for security. Our updated `Dockerfile` automatically switches to a non-root `user` to avoid file write and cache permissions issues.
* **Port 7860 default:** Hugging Face requires web apps to listen on port `7860`. Our `Dockerfile` configures `PORT=7860` and `EXPOSE 7860` dynamically.
* **Pre-baked Weights:** PyTorch model weights are downloaded during the Docker build stage. This ensures instant app startup on Hugging Face Spaces and avoids runtime download timeouts.

#### Step-by-Step Deployment Instructions:

1. **Create a Space on Hugging Face:**
   * Sign up or log in at [Hugging Face](https://huggingface.co/).
   * Click your profile icon at the top right and select **New Space** (or go directly to [huggingface.co/new-space](https://huggingface.co/new-space)).
   * Set a name for your Space (e.g., `traffic-analytics`).
   * Select **Docker** as the SDK.
   * Under "Choose a Docker template", select **Blank**.
   * Choose the **CPU basic (16GB RAM, Free)** hardware tier.
   * Set the Space visibility (**Public** or **Private**).
   * Click **Create Space**.

2. **Upload/Push Your Code:**
   *Hugging Face Spaces are Git repositories. You can upload files directly through the web UI, or use git CLI.*
   
   **Using Git CLI:**
   * Clone your Space repository locally:
     ```bash
     git clone https://huggingface.co/spaces/your-username/your-space-name
     ```
   * Copy all project files (including `app.py`, `Dockerfile`, `requirements.txt`, the `templates/` directory, and the `static/` directory) into the cloned directory.
   * Commit and push your files:
     ```bash
     git add .
     git commit -m "Deploy traffic detection dashboard"
     git push
     ```

3. **Build and View:**
   * Navigate to your Space page.
   * Under the **App** tab, you will see the logs as Hugging Face builds your Docker container.
   * Once the build is complete, the Space status will change to **Running**, and your dashboard will be interactive directly on the web page!

### Option C: Railway
Railway is another quick way to deploy:
1. Connect your GitHub repository to [Railway](https://railway.app/).
2. Railway will automatically detect the `Dockerfile` and build it.
3. Add a custom domain or use the provided Railway domain to access your application.
