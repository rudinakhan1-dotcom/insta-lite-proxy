from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('q', '')
    url_to_open = request.args.get('url', '')
    
    # 1. SEARCH LOGIC (Using Bing - Block Proof)
    if query:
        # Hum user ko Bing ke Mobile Lite version par bhej rahe hain
        bing_url = f"https://www.bing.com/search?q={query}"
        return render_template_string(f'<meta http-equiv="refresh" content="0; url={bing_url}">')

    # 2. PROXY LOGIC (Direct Mobile Redirect)
    if url_to_open:
        # Facebook/Insta ke liye Mobile-friendly URL ensure karna
        final_url = url_to_open
        if "facebook.com" in url_to_open:
            final_url = "https://m.facebook.com"
        elif "instagram.com" in url_to_open:
            final_url = "https://www.instagram.com/accounts/login/"
            
        return render_template_string(f'<meta http-equiv="refresh" content="0; url={final_url}">')

    # 3. CLEAN & STYLISH HOME PAGE (JioBharat Optimized)
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif; background:#ffffff; min-height:100vh;">
        <h1 style="color:#0078d4; font-size:35px;">Jio<span style="color:#333;">Lite</span></h1>
        
        <form action="/" method="get" style="margin-bottom:25px;">
            <input type="text" name="q" placeholder="Search anything..." 
                   style="width:85%; padding:12px; border:2px solid #0078d4; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:90%; padding:12px; background:#0078d4; color:white; border:none; border-radius:10px; font-weight:bold;">SEARCH NOW</button>
        </form>

        <div style="display: flex; flex-direction: column; gap: 12px; align-items: center;">
            <a href="/?url=https://m.facebook.com" style="width:85%; padding:12px; background:#3b5998; color:white; text-decoration:none; border-radius:8px;">Facebook Login</a>
            <a href="/?url=https://www.instagram.com/accounts/login/" style="width:85%; padding:12px; background:#e1306c; color:white; text-decoration:none; border-radius:8px;">Instagram Login</a>
            <a href="/?url=https://m.youtube.com" style="width:85%; padding:12px; background:#ff0000; color:white; text-decoration:none; border-radius:8px;">YouTube Mobile</a>
            <a href="/?url=https://y2mate.is" style="width:85%; padding:12px; background:#444; color:white; text-decoration:none; border-radius:8px;">Video Downloader</a>
        </div>
        
        <p style="margin-top:25px; font-size:11px; color:#888;">© 2026 JioLite Proxy Engine</p>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
