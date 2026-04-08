import os
from flask import Flask, render_template_string, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --- CLOUDINARY CONFIGURATION ---
# Note: Details wahi hain jo tumne di thi
cloudinary.config( 
  cloud_name = "dntmgunma", 
  api_key = "247386995162694", 
  api_secret = "Z4NDEGSgXqA5eUdNlRbjL6V-FoE" 
)

# --- HTML TEMPLATE ---
# Isme loop aur image handling fix kar di hai
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jio Video Cloud</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 5px; }
        .box { border: 2px dashed #444; padding: 10px; margin-bottom: 20px; background: #111; }
        .v-card { border-bottom: 1px solid #333; padding: 15px 0; margin-bottom: 10px; }
        .thumb { width: 160px; height: 120px; object-fit: cover; border: 1px solid #555; background: #222; }
        .btn-up { background: #28a745; color: white; padding: 10px; width: 100%; border: none; margin-top: 10px; font-weight: bold; }
        .btn-dl { background: #007bff; color: white; text-decoration: none; padding: 10px; display: block; margin: 10px auto; width: 80%; border-radius: 5px; font-size: 14px; }
        input[type="file"] { color: #ccc; margin: 10px 0; }
    </style>
</head>
<body>
    <h3>Jio Video Manager</h3>
    
    <div class="box">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="video/*" required><br>
            <button type="submit" class="btn-up">UPLOAD VIDEO</button>
        </form>
    </div>

    <h4 style="text-align: left; border-left: 3px solid #ffc107; padding-left: 10px;">Videos List:</h4>

    {% if videos %}
        {% for v in videos %}
        <div class="v-card">
            <b style="color: #ffc107; font-size: 12px;">{{ v.public_id }}</b><br>
            <img src="{{ v.secure_url.rsplit('.', 1)[0] + '.jpg' }}" class="thumb" alt="Thumbnail"><br>
            <a href="{{ v.secure_url }}" class="btn-dl">WATCH / DOWNLOAD</a>
        </div>
        {% endfor %}
    {% else %}
        <p style="color: #666;">No videos found. Upload one!</p>
    {% endif %}

</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def index():
    try:
        # Cloudinary API se videos ki list nikalna
        res = cloudinary.api.resources(resource_type="video")
        video_list = res.get('resources', [])
    except Exception as e:
        print(f"Error fetching: {e}")
        video_list = []
    
    return render_template_string(HTML_TEMPLATE, videos=video_list)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
        
    if file:
        try:
            # Video upload logic
            cloudinary.uploader.upload_video(file, resource_type="video")
        except Exception as e:
            print(f"Upload failed: {e}")
            
    return redirect(url_for('index'))

# --- START SERVER ---
if __name__ == "__main__":
    # Port 5000 par run hoga (Termux/Netlify friendly)
    app.run(host='0.0.0.0', port=5000, debug=True)
