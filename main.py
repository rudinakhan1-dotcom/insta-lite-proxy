import os
from flask import Flask, render_template_string, request, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- CONFIGURATION (Fixed Details) ---
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE" 
)

# --- UI (Download + Title Support) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Pro Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 10px; }
        .v-card { border: 1px solid #444; margin-bottom: 25px; padding: 10px; border-radius: 10px; background: #1a1a1a; }
        video { width: 100%; border-radius: 5px; background: #000; }
        .box { background: #333; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        input, button { width: 90%; padding: 12px; margin: 5px 0; border-radius: 5px; border: none; }
        .up-btn { background: #28a745; color: white; font-weight: bold; }
        .dl-btn { background: #007bff; color: white; display: block; text-decoration: none; padding: 10px; margin-top: 10px; border-radius: 5px; font-size: 14px; }
    </style>
</head>
<body>
    <h3>Video Cloud Manager</h3>
    <div class="box">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="text" name="title" placeholder="Video ka naam..." required>
            <input type="file" name="file" required>
            <button type="submit" class="up-btn">Upload Video</button>
        </form>
    </div>
    <hr style="border: 0.5px solid #444;">
    {% for v in videos %}
    <div class="v-card">
        <h4 style="margin: 5px 0; color: #ffc107;">{{ v.public_id }}</h4>
        <video controls preload="none">
            <source src="{{ v.secure_url }}" type="video/mp4">
        </video>
        <a href="{{ v.secure_url }}" download="{{ v.public_id }}.mp4" class="dl-btn">Download Video</a>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    try:
        result = cloudinary.api.resources(resource_type="video", type="upload", max_results=50)
        videos = result.get('resources', [])
    except:
        videos = []
    return render_template_string(HTML_TEMPLATE, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    title = request.form.get('title')
    if file:
        try:
            cloudinary.uploader.upload(file, resource_type="video", public_id=title)
        except Exception as e:
            print(f"Error: {e}")
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
