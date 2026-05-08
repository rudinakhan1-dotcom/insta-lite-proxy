import os
from flask import Flask, render_template_string, request, redirect, jsonify
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

PASSWORD_PROTECT = "809047"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jio Video Cloud Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; text-align: center; padding: 0; margin: 0; }
        .header { background: #cc0000; padding: 15px; border-bottom: 3px solid #900; }
        .main-title { font-size: 20px; font-weight: bold; }
        .dev-name { font-size: 12px; color: #ffc107; display: block; margin-top: 4px; }
        
        .box { border: 2px dashed #444; padding: 15px; margin: 10px; background: #111; }
        input[type="text"], input[type="password"], input[type="file"] { width: 90%; padding: 10px; margin: 5px 0; background: #222; border: 1px solid #444; color: #fff; }
        
        .progress-container { width: 90%; background: #333; margin: 10px auto; display: none; height: 20px; border-radius: 10px; overflow: hidden; }
        .progress-bar { width: 0%; height: 100%; background: #28a745; transition: width 0.3s; }

        .v-card { border-bottom: 2px solid #222; padding: 15px 5px; margin: 10px; background: #0a0a0a; }
        .thumb { width: 180px; height: 110px; object-fit: cover; border: 1px solid #333; }
        
        .btn { padding: 10px; border: none; font-weight: bold; cursor: pointer; color: #fff; margin: 5px; width: 45%; font-size: 12px; border-radius: 4px; }
        .btn-up { background: #28a745; width: 95%; }
        .btn-dl { background: #007bff; }
        .btn-ren { background: #ffc107; color: #000; }
        .btn-del { background: #dc3545; width: 93%; }

        .search-box { background: #111; padding: 10px; border-bottom: 1px solid #cc0000; }
        .nav-btn { color: #ffc107; text-decoration: none; font-weight: bold; padding: 10px; border: 1px solid #444; margin: 5px; display: inline-block; }
    </style>
</head>
<body>
    <div class="header">
        <span class="main-title">Jio Video Cloud</span>
        <span class="dev-name">Developed by: ATIF KHAN</span>
    </div>

    <div class="search-box">
        <form action="/" method="GET">
            <input type="text" name="q" placeholder="Search videos..." value="{{ q }}" style="width:60%;">
            <button type="submit" style="padding:10px; background:#cc0000; color:#fff; border:none;">GO</button>
        </form>
    </div>

    <div class="box">
        <b>Upload Video (Chunking Enabled)</b><br>
        <input type="text" id="videoName" placeholder="Video ka naam...">
        <input type="password" id="upPass" placeholder="Upload Password">
        <input type="file" id="fileInput">
        <div class="progress-container" id="progCont"><div class="progress-bar" id="progBar"></div></div>
        <div id="status" style="font-size:12px; margin-top:5px;"></div>
        <button onclick="startUpload()" class="btn btn-up">UPLOAD NOW</button>
    </div>

    {% for v in videos %}
    <div class="v-card">
        <b style="color: #ffc107;">{{ v.public_id }}</b><br>
        <img src="{{ v.secure_url.replace('.mp4', '.jpg').replace('.mkv', '.jpg').replace('.3gp', '.jpg') }}" class="thumb"><br>
        
        <button onclick="actionCheck('dl', '{{ v.secure_url }}')" class="btn btn-dl">DOWNLOAD</button>
        <button onclick="actionCheck('ren', '{{ v.public_id }}')" class="btn btn-ren">RENAME</button>
        <button onclick="actionCheck('del', '{{ v.public_id }}')" class="btn btn-del">DELETE VIDEO</button>
    </div>
    {% endfor %}

    <div class="nav-box" style="padding: 20px;">
        {% if cursor_prev %} <a href="/?cursor={{ cursor_prev }}" class="nav-btn"><< PREV</a> {% endif %}
        {% if next_cursor %} <a href="/?cursor={{ next_cursor }}" class="nav-btn">NEXT >></a> {% endif %}
    </div>

<script src="https://upload-widget.cloudinary.com/global/all.js"></script>
<script>
const PASS = "809047";

function actionCheck(type, data) {
    let p = prompt("Enter Password:");
    if (p !== PASS) { alert("Wrong Password!"); return; }

    if (type === 'dl') { window.location.href = data; }
    if (type === 'del') { if(confirm("Delete karein?")) window.location.href = "/delete/" + data; }
    if (type === 'ren') { 
        let newName = prompt("Naya naam likho:");
        if(newName) window.location.href = "/rename/" + data + "/" + newName;
    }
}

async function startUpload() {
    const file = document.getElementById('fileInput').files[0];
    const vName = document.getElementById('videoName').value;
    const upPass = document.getElementById('upPass').value;

    if (!file || !vName || upPass !== PASS) { alert("Details check karein!"); return; }

    document.getElementById('progCont').style.display = 'block';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('upload_preset', 'ml_default'); // Cloudinary settings mein unsigned preset enable karein
    formData.append('public_id', vName);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://api.cloudinary.com/v1_1/dntmgunma/video/upload');

    xhr.upload.onprogress = (e) => {
        const percent = Math.round((e.loaded / e.total) * 100);
        document.getElementById('progBar').style.width = percent + '%';
        document.getElementById('status').innerText = "Uploading: " + percent + "% (" + Math.round(e.loaded/1024/1024) + "MB / " + Math.round(e.total/1024/1024) + "MB)";
    };

    xhr.onload = () => {
        if (xhr.status === 200) {
            alert("Upload Success!");
            window.location.reload();
        } else {
            alert("Upload Failed! Preset check karein.");
        }
    };

    xhr.send(formData);
}
</script>
</body>
</html>
"""

@app.route('/')
def index():
    query = request.args.get('q', '').strip()
    cursor = request.args.get('cursor')
    try:
        # Har page par 10 results
        res = cloudinary.api.resources(resource_type="video", type="upload", max_results=10, next_cursor=cursor)
        videos = res.get('resources', [])
        next_cursor = res.get('next_cursor')
        
        if query:
            videos = [v for v in videos if query.lower() in v['public_id'].lower()]
            
        return render_template_string(HTML_TEMPLATE, videos=videos, q=query, next_cursor=next_cursor)
    except:
        return "Server error. Cloudinary settings check karein."

@app.route('/delete/<public_id>')
def delete_video(public_id):
    cloudinary.uploader.destroy(public_id, resource_type="video")
    return redirect('/')

@app.route('/rename/<old_id>/<new_id>')
def rename_video(old_id, new_id):
    cloudinary.uploader.rename(old_id, new_id, resource_type="video")
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
