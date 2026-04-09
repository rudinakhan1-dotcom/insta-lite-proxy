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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jio Video Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 5px; }
        .box { border: 2px dashed #444; padding: 10px; margin-bottom: 20px; background: #111; }
        .v-card { border-bottom: 1px solid #333; padding: 15px 0; }
        .thumb { width: 160px; height: 120px; object-fit: cover; border: 1px solid #555; background: #222; }
        .btn-up { background: #28a745; color: white; padding: 10px; width: 100%; border: none; margin-top: 5px; }
        .btn-dl { background: #007bff; color: white; text-decoration: none; padding: 10px; display: block; margin: 10px auto; width: 70%; border-radius: 5px; }
        .search-box { background: #222; padding: 10px; margin-bottom: 15px; border-bottom: 1px solid #cc0000; }
        input[type="text"] { width: 70%; padding: 8px; background: #000; color: #fff; border: 1px solid #555; }
        .btn-search { padding: 8px; background: #cc0000; color: #fff; border: none; font-weight: bold; }
    </style>
</head>
<body>
    <h3>Video Manager</h3>

    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="Video search karein..." value="{{ q }}">
            <button type="submit" class="btn-search">GO</button>
        </form>
        {% if q %}
            <div style="font-size: 12px; margin-top: 5px;">Showing results for: <b>{{ q }}</b> | <a href="/" style="color: #007bff;">Clear</a></div>
        {% endif %}
    </div>

    <div class="box">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <button type="submit" class="btn-up">UPLOAD NOW</button>
        </form>
    </div>

    {% if videos %}
        {% for v in videos %}
        <div class="v-card">
            <b style="color: #ffc107;">{{ v.public_id }}</b><br>
            <img src="{{ v.secure_url.replace('.mp4', '.jpg').replace('.mkv', '.jpg').replace('.3gp', '.jpg') }}" class="thumb"><br>
            <a href="{{ v.secure_url }}" class="btn-dl">DOWNLOAD / WATCH</a>
        </div>
        {% endfor %}
    {% else %}
        <p style="color: #888;">No videos found.</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    query = request.args.get('q', '')
    if query:
        # Search Logic: Cloudinary search API ka use karke
        # public_id mein query search karna
        search_res = cloudinary.Search() \
            .expression(f'resource_type:video AND public_id:*{query}*') \
            .execute()
        videos = search_res.get('resources', [])
    else:
        # Normal List
        res = cloudinary.api.resources(resource_type="video")
        videos = res.get('resources', [])
        
    return render_template_string(HTML_TEMPLATE, videos=videos, q=query)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        cloudinary.uploader.upload_video(file, resource_type="video")
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
