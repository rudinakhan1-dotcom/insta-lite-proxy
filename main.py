import os
from flask import Flask, render_template_string, request, redirect
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
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 5px; margin: 0; }
        .header { background: #cc0000; padding: 10px; font-weight: bold; margin-bottom: 5px; }
        .dev-name { font-size: 12px; color: #ffc107; display: block; margin-top: 3px; }
        .box { border: 2px dashed #444; padding: 10px; margin: 10px; background: #111; }
        .v-card { border-bottom: 1px solid #333; padding: 15px 0; margin: 0 10px; }
        .thumb { width: 160px; height: 120px; object-fit: cover; border: 1px solid #555; background: #222; }
        .btn-up { background: #28a745; color: white; padding: 10px; width: 100%; border: none; margin-top: 5px; font-weight: bold; }
        .btn-dl { background: #007bff; color: white; text-decoration: none; padding: 12px; display: block; margin: 10px auto; width: 80%; border-radius: 5px; font-weight: bold; }
        .search-box { background: #222; padding: 10px; border-bottom: 1px solid #cc0000; margin-bottom: 10px; }
        input[type="text"] { width: 65%; padding: 8px; background: #000; color: #fff; border: 1px solid #555; }
        .btn-search { padding: 8px 15px; background: #cc0000; color: #fff; border: none; font-weight: bold; }
        .nav-box { padding: 20px; }
        .nav-btn { color: #ffc107; text-decoration: none; font-weight: bold; padding: 10px; border: 1px solid #444; margin: 5px; display: inline-block; min-width: 80px; }
    </style>
</head>
<body>
    <div class="header">
        Jio Video Cloud
        <span class="dev-name">(ATIF-khan) developer</span>
    </div>

    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="Video search..." value="{{ q }}">
            <button type="submit" class="btn-search">GO</button>
        </form>
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
        <p style="color: #888; padding: 20px;">No videos found.</p>
    {% endif %}

    <div class="nav-box">
        {% if next_cursor %}
            <a href="/?cursor={{ next_cursor }}{% if q %}&q={{ q }}{% endif %}" class="nav-btn">NEXT >></a>
        {% endif %}
        <br><br>
        <a href="/" class="nav-btn" style="background: #333;">HOME</a>
    </div>
</body>
</html>
