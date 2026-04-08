import os
from flask import Flask, render_template_string, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- CONFIGURATION ---
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE" 
)

# --- UI (JioBharat Optimized) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jio Video Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 5px; }
        .box { background: #222; border: 1px dotted #555; padding: 10px; margin-bottom: 15px; }
        .v-card { border-bottom: 2px solid #333; margin-bottom: 20px; padding-bottom: 10px; }
        .thumb { width: 100%; max-width: 200px; border: 1px solid #444; }
        .btn-up { background: green; color: white; padding: 10px; width: 90%; border: none; font-weight: bold; }
        .btn-dl { background: #007bff; color: white; text-decoration: none; padding: 12px; display: block; margin: 10px auto; width: 80%; border-radius: 4px; font-size: 14px; }
        .nav-btn { background: #444; color: white; padding: 8px 20px; text-decoration: none; margin: 10px; display: inline-block; border-radius: 4px; }
    </style>
</head>
<body>
    <h3>Video Manager</h3>
    
    <div class="box">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="text" name="title" placeholder="Video Name" required style="width:85%; margin-bottom:5px;"><br>
            <input type="file" name="file" required style="color:white; font-size:12px;"><br>
            <button type="submit" class="btn-up">UPLOAD</button>
        </form>
    </div>

    {% for v in videos %}
    <div class="v-card">
        <b style="color: #ffc107; font-size: 14px;">{{ v.public_id }}</b><br>
        <img src="{{ v.secure_url | replace('.mp4', '.jpg') }}" class="thumb" alt="Thumbnail"><br>
        <a href="{{ v.secure_url }}" class="btn-dl">DOWNLOAD NOW</a>
    </div>
    {% endfor %}

    <div style="margin-top: 20px; padding-bottom: 30px;">
        {% if next_cursor %}
            <a href="{{ url_for('index', cursor=next_cursor) }}" class="nav-btn">NEXT >></a>
        {% endif %}
        <a href="/" class="nav-btn">HOME</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    cursor = request.args.get('cursor')
    try:
        # max_results=10 rakha hai taaki 10 hi dikhein
        result = cloudinary.api.resources(
            resource_type="video", 
            type="upload", 
            max_results=10, 
            next_cursor=cursor
        )
        videos = result.get('resources', [])
        next_cursor = result.get('next_cursor')
    except:
        videos = []
        next_cursor = None
    return render_template_string(HTML_TEMPLATE, videos=videos, next_cursor=next_cursor)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    title = request.form.get('title')
    if file:
        try:
            cloudinary.uploader.upload(file, resource_type="video", public_id=title)
        except:
            pass
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
