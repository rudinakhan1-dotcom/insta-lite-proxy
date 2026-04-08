import os
import time
from flask import Flask, render_template_string, request, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- CLOUDINARY CONFIG (Aapki Details Fixed) ---
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE",
  secure = True
)

# --- JIO-OPTIMIZED UI (YouTube Style) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JioCloud Tube</title>
    <style>
        body { font-family: sans-serif; background: #000; color: #fff; margin: 0; padding: 10px; }
        .brand { color: #f00; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 15px; }
        .upload-box { background: #222; padding: 15px; border-radius: 10px; border: 1px dashed #f00; margin-bottom: 20px; }
        .video-card { background: #111; margin-bottom: 30px; border-radius: 8px; overflow: hidden; border: 1px solid #333; }
        video { width: 100%; display: block; background: #000; height: 200px; }
        .video-title { padding: 10px; font-size: 14px; color: #eee; border-top: 1px solid #222; }
        .btn-download { display: block; width: 100%; padding: 15px; background: #28a745; color: #fff; 
                        text-decoration: none; text-align: center; font-weight: bold; border-radius: 0 0 8px 8px; }
        .btn-upload { width: 100%; padding: 12px; background: #f00; color: #fff; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; }
        input[type="file"] { margin: 10px 0; color: #ccc; width: 100%; }
    </style>
</head>
<body>
    <div class="brand">JioCloud Tube</div>

    <div class="upload-box">
        <strong>Upload New Video</strong>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="video/*" required>
            <button type="submit" class="btn-upload">START UPLOAD</button>
        </form>
    </div>

    <h3 style="border-left: 4px solid #f00; padding-left: 10px;">Your Video Feed</h3>
    {% for v in videos %}
    <div class="video-card">
        <video controls preload="metadata">
            <source src="{{ v.url }}" type="video/mp4">
            Your browser does not support video.
        </video>
        <div class="video-title">{{ v.name }}</div>
        <a href="{{ v.url }}" download class="btn-download">DOWNLOAD VIDEO</a>
    </div>
    {% endfor %}

    {% if not videos %}
    <p style="text-align:center; color:#666; margin-top:30px;">No videos found. Upload your first video!</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    try:
        # Latest videos mangwane ka logic
        res = cloudinary.api.resources(resource_type="video", max_results=50)
        vids = []
        for r in res.get('resources', []):
            vids.append({
                'url': r['secure_url'],
                'name': r['public_id'].split('/')[-1]
            })
        return render_template_string(HTML_TEMPLATE, videos=vids)
    except Exception as e:
        return f"System Error: {str(e)}"

@app.route('/upload', methods=['POST'])
def do_upload():
    if 'file' not in request.files: return redirect('/')
    f = request.files['file']
    if f.filename == '': return redirect('/')
    
    try:
        # Video upload process
        cloudinary.uploader.upload_video(f, resource_type="video")
        # Chota sa wait taaki cloud register kar le
        time.sleep(3) 
    except Exception as e:
        print(f"Upload failed: {e}")
    
    return redirect('/')

if __name__ == "__main__":
    # Render Port Fix
    p = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=p)
