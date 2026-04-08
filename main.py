import os
from flask import Flask, render_template_string, request, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- AAPKI CLOUDINARY DETAILS (FIXED) ---
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE" 
)

# --- HTML (JioBharat aur Render ke liye optimized) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My Video Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #111; color: white; font-family: sans-serif; text-align: center; padding: 10px; }
        .v-card { border: 1px solid #444; margin-bottom: 20px; padding: 10px; border-radius: 10px; background: #222; }
        video { width: 100%; border-radius: 5px; }
        .upload-section { background: #333; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .btn { background: #28a745; color: white; padding: 12px; border: none; width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
</head>
<body>
    <h3>Video Cloud Manager</h3>
    
    <div class="upload-section">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required style="margin-bottom: 10px;">
            <button type="submit" class="btn">Click to Upload Video</button>
        </form>
    </div>

    <hr style="border: 0.5px solid #444;">

    {% for v in videos %}
    <div class="v-card">
        <p style="font-size: 12px; color: #aaa;">ID: {{ v.public_id }}</p>
        <video controls preload="none">
            <source src="{{ v.secure_url }}" type="video/mp4">
            Browser not supported.
        </video>
    </div>
    {% else %}
        <p>No videos found. Upload your first one!</p>
    {% endfor %}
</body>
</html>
"""

@app.route('/')
def index():
    try:
        # Cloudinary se 50 latest videos fetch karna
        result = cloudinary.api.resources(resource_type="video", type="upload", max_results=50)
        videos = result.get('resources', [])
    except Exception as e:
        print(f"Log Error: {e}")
        videos = []
    return render_template_string(HTML_TEMPLATE, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        try:
            cloudinary.uploader.upload(file, resource_type="video")
        except Exception as e:
            print(f"Upload Fail: {e}")
    return redirect('/')

if __name__ == "__main__":
    # Render Port Binding (Port 10000 fix)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
