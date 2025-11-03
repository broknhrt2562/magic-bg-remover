# Cloud Background Removal

A simple Flask-based web app and API for removing image backgrounds in the cloud using AI (rembg).

## Features
- Web page with image upload form
- REST API endpoint for programmatic access
- Returns processed image with background removed

## Setup

1. **Clone the repo and install dependencies:**
   ```bash
   cd app
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Access the web app:**
   - Open [http://localhost:5000](http://localhost:5000) in your browser

4. **API Usage:**
   - POST an image to `/api/remove-bg`
   - Example with cURL:
     ```bash
     curl -F "image=@yourfile.jpg" http://localhost:5000/api/remove-bg --output result.png
     ```

## Deploying to Cloud
- Upload the project to your cloud VM
- Make sure Python 3.8+ is installed
- Open port 5000 (or change in `main.py`)
- Run as above

## Notes
- Processed images are served from `/processed/<filename>`
- For production, use a WSGI server (e.g., gunicorn) and secure file handling 