from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('q', '')
    url_to_open = request.args.get('url', '')

    # 1. SEARCH LOGIC (Google Web Light ke naye raste se)
    if query:
        # Hum Google Search ko directly bypass karke Web Light par bhejenge
        # Isse white screen nahi aayegi
        search_target = f"https://www.google.com/search?q={query}"
        gateway = f"https://googleweblight.com/i?u={search_target}"
        return render_template_string(f'<meta http-equiv="refresh" content="0; url={gateway}">')

    # 2. SITE OPEN LOGIC
    if url_to_open:
        # Instagram/Facebook ke liye force mobile optimization
        if "instagram.com" in url_to_open:
            url_to_open = "https://www.social-searcher.com/google-social-search/?q=instagram+login"
        
        gateway = f"https://googleweblight.com/i?u={url_to_open}"
        return render_template_string(f'<meta http-equiv="refresh" content="0; url={gateway}">')

    # 3. CLEAN HOME UI
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif; background:#fff; min-height:100vh;">
        <h1 style="color:#4285F4; font-size:40px;">Jio<span style="color:#34A853;">Lite</span></h1>
        
        <form action="/" method="get">
            <input type="text" name="q" placeholder="Search anything..." 
                   style="width:85%; padding:15px; border:1px solid #ddd; border-radius:25px; outline:none; font-size:16px;">
            <br><br>
            <button type="submit" style="padding:12px 30px; background:#4285F4; color:white; border:none; border-radius:20px; font-weight:bold;">Search Engine</button>
        </form>

        <div style="margin-top:40px; display:grid; gap:15px; justify-content:center;">
            <a href="/?url=https://m.facebook.com" style="width:200px; padding:12px; background:#3b5998; color:white; text-decoration:none; border-radius:10px;">Facebook</a>
            <a href="/?url=https://www.instagram.com" style="width:200px; padding:12px; background:#e1306c; color:white; text-decoration:none; border-radius:10px;">Instagram</a>
            <a href="/?url=https://y2mate.is" style="width:200px; padding:12px; background:#ff0000; color:white; text-decoration:none; border-radius:10px;">YouTube Downloader</a>
        </div>
        
        <p style="margin-top:30px; font-size:12px; color:#999;">Agar white screen aaye toh 5 second wait karein ya page refresh karein.</p>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
