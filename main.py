from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('q', '')
    
    # 1. SEARCH LOGIC (Using DuckDuckGo Lite - No Blocks!)
    if query:
        # Hum user ko DuckDuckGo ke HTML version par bhej rahe hain jo best hai
        ddg_url = f"https://duckduckgo.com/html/?q={query}"
        return render_template_string(f'<meta http-equiv="refresh" content="0; url=https://googleweblight.com/i?u={ddg_url}">')

    # 2. PROXY LOGIC (Google Web Light Gateway)
    url_to_open = request.args.get('url', '')
    if url_to_open:
        # Kisi bhi site ko Google Web Light ke zariye kholna
        lite_gateway = f"https://googleweblight.com/i?u={url_to_open}"
        return render_template_string(f'<meta http-equiv="refresh" content="0; url={lite_gateway}">')

    # 3. ULTRA-LITE HOME PAGE
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif; background:#f4f4f4; min-height:100vh;">
        <h1 style="color:#4285F4;">Jio<span style="color:#EA4335;">Search</span> <small style="font-size:12px; color:green;">v3.0</small></h1>
        
        <form action="/" method="get" style="margin-bottom:30px;">
            <input type="text" name="q" placeholder="Kuch bhi search karein..." 
                   style="width:85%; padding:15px; border:2px solid #ddd; border-radius:30px; outline:none;">
            <br><br>
            <button type="submit" style="padding:10px 25px; background:#4285F4; color:white; border:none; border-radius:20px; font-weight:bold;">Google Search</button>
        </form>

        <div style="display: flex; flex-direction: column; gap: 10px; align-items: center;">
            <a href="/?url=https://m.facebook.com" style="width:80%; padding:15px; background:#3b5998; color:white; text-decoration:none; border-radius:10px; font-weight:bold;">Facebook (Fast)</a>
            <a href="/?url=https://www.instagram.com/accounts/login/" style="width:80%; padding:15px; background:#e1306c; color:white; text-decoration:none; border-radius:10px; font-weight:bold;">Instagram Login</a>
            <a href="/?url=https://y2mate.is" style="width:80%; padding:15px; background:#ff0000; color:white; text-decoration:none; border-radius:10px; font-weight:bold;">Video Downloader</a>
            <a href="/?url=https://www.google.com" style="width:80%; padding:15px; background:#34a853; color:white; text-decoration:none; border-radius:10px; font-weight:bold;">Google Lite</a>
        </div>
        
        <p style="margin-top:20px; font-size:12px; color:#666;">Note: Har site 5-10 second mein compress hokar khulegi.</p>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
