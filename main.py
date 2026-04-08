import os
from flask import Flask, render_template_string, request, redirect
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- AAPKI CLOUDINARY DETAILS ---
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE",
  secure = True
)

# --- JIO-OPTIMIZED UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Cloud Tube</title>
    <style>
        body { font-family: Arial, sans-serif; background: #000; color: #fff; margin: 0; padding: 10px; }
        .brand { color: #f00; font-size: 24px; font-weight: bold; text-align: center; margin-bottom: 20px; }
        .upload-box { background: #222; padding: 15px; border-radius: 10px; border: 1px dashed #f00; margin-bottom: 20px; }
        .video-item { background: #111; margin-bottom: 25px; border-radius: 8px; overflow: hidden; border: 1px solid #333; }
        video { width: 100%; display: block; background: #000; }
        .video-info { padding: 10px; }
        .download-btn { display: block; width: 100%; padding: 12px; background: #28a745; color: #fff; 
                        text-decoration: none; text-align: center; font-weight: bold; border-radius: 5px; margin-top: 5px; }
        .upload-btn { width: 100%; padding: 12px; background: #f00; color: #fff; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; }
        input[type="file"] { margin: 10px 0; display: block; width: 100%; color: #ccc; }
    </style>
</head>
<body>
    <div class="brand">MY CLOUD TUBE</div>

    <div class="upload-box">
        <strong>Upload Video</strong>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="video/*" required>
            <button type="submit" class="upload-btn">UPLOAD NOW</button>
        </form>
    </div>

    <hr style="border: 0; border-top: 1px solid #333;">

    <h3>Video Feed</h3>
    {% for v in videos %}
    <div class="video-item">
        <video controls>
            <source src="{{ v.url }}" type="video/mp4">
            JioBharat doesn't support this player.
        </video>
        <div class="video-info">
            <div style="margin-bottom:10px;">{{ v.name }}</div>
            <a href="{{ v.url }}" download class="download-btn">DOWNLOAD MP4</a>
        </div>
    </div>
    {% endfor %}

    {% if not videos %}
    <p style="text-align:center; color:#666;">No videos yet. Upload something!</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    try:
        res = cloudinary.api.resources(resource_type="video")
        vids = []
        for r in res.get('resources', []):
            vids.append({
                'url': r['secure_url'],
                'name': r['public_id'].split('/')[-1]
            })
        return render_template_string(HTML_TEMPLATE, videos=vids)
    except Exception as e:
        return f"Cloud Error: {e}"

@app.route('/upload', methods=['POST'])
def do_upload():
    if 'file' not in request.files: return redirect('/')
    f = request.files['file']
    if f.filename == '': return redirect('/')
    
    try:
        cloudinary.uploader.upload_video(f, resource_type="video")
    except Exception as e:
        print(f"Upload Error: {e}")
    
    return redirect('/')

if __name__ == "__main__":
    p = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=p)
