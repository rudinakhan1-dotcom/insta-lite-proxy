from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# Real Chrome Browser ki tarah dikhne ke liye headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

@app.route('/')
def proxy():
    # 1. Search ya URL nikalna
    query = request.args.get('q', '')
    target_url = request.args.get('url', '')

    # Agar user search kare toh Google Search fetch karo
    if query:
        target_url = f"https://www.google.com/search?q={query}"

    # Default Home Page
    if not target_url and not query:
        return '''
        <div style="text-align:center; padding:20px; font-family:sans-serif; background:#f0f2f5; min-height:100vh;">
            <h1 style="color:#007bff;">Jio<span style="color:#333;">Proxy</span></h1>
            <form action="/" method="get">
                <input type="text" name="q" placeholder="Google Search..." style="width:80%; padding:12px; border-radius:20px; border:1px solid #ccc;">
                <br><br>
                <button type="submit" style="padding:10px 25px; background:#007bff; color:white; border:none; border-radius:15px;">Search</button>
            </form>
            <div style="margin-top:25px; display:grid; gap:10px;">
                <a href="/?url=https://m.facebook.com" style="padding:10px; background:#3b5998; color:white; text-decoration:none; border-radius:5px;">Facebook Lite</a>
                <a href="/?url=https://www.instagram.com/accounts/login/" style="padding:10px; background:#e1306c; color:white; text-decoration:none; border-radius:5px;">Instagram Login</a>
                <a href="/?url=https://y2mate.is" style="padding:10px; background:#ff0000; color:white; text-decoration:none; border-radius:5px;">Video Downloader</a>
            </div>
        </div>
        '''

    # 2. Site ko Fetch karna (Proxy Logic)
    try:
        if not target_url.startswith('http'):
            target_url = 'https://' + target_url

        response = requests.get(target_url, headers=HEADERS, timeout=15, allow_redirects=True)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Link Rewriting (Sari links ko aapki site ke through bhejna)
        for tag in soup.find_all(['a', 'form'], href=True, action=True):
            if tag.name == 'a':
                original_href = tag['href']
                full_url = urljoin(target_url, original_href)
                tag['href'] = f"/?url={full_url}"
            elif tag.name == 'form':
                original_action = tag['action']
                full_url = urljoin(target_url, original_action)
                tag['action'] = f"/?url={full_url}"

        # 4. Compression (Ads aur bhari scripts hatana)
        for script in soup(["script", "style", "iframe", "ins"]):
            script.decompose()

        # Header bar taaki user wapas home ja sake
        proxy_header = f'''
        <div style="background:#333; color:white; padding:10px; text-align:center; font-family:sans-serif;">
            <a href="/" style="color:yellow; text-decoration:none;">[ New Search ]</a> | 
            <span style="font-size:12px;">Browsing: {urlparse(target_url).netloc}</span>
        </div>
        '''
        
        return proxy_header + soup.prettify()

    except Exception as e:
        return f'<div style="padding:20px;"><h3>Error: Link nahi khul raha.</h3><p>{str(e)}</p><a href="/">Back to Home</a></div>'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
