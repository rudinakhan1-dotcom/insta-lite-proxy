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
        .btn-up { background: #28a745; color: white; padding: 10px; width: 100%; border: none; margin-top: 10px; }
        .btn-dl { background: #007bff; color: white; text-decoration: none; padding: 10px; display: block; margin: 10px auto; width: 70%; border-radius: 5px; }
        .nav-btn { background: #333; color: white; padding: 10px; text-decoration: none; margin: 5px; display: inline-block; }
    </style>
</head>
<body>
    <h3>Video Manager</h3>
    
    <div class="box">
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="text" name="title" placeholder="Video Name" required style="width:90%; padding:8px;"><br>
            <input type="file" name="file" required style="margin-top:10px;"><br>
            <button type="submit" class="btn-up">UPLOAD NOW</button>
        </form>
    </div>

    {% for v in videos %}
    <div class="v-card">
        <b style="color: #ffc107;">{{ v.public_id }}</b><br>
        <img src="{{ v.secure_url | replace('.mp4', '.jpg') }}" class="thumb" alt="Loading..."><br>
        <a href="{{ v.secure_url }}" class="btn-dl">DOWNLOAD</a>
