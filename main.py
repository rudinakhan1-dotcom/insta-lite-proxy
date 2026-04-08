from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time  # 20 second rukne ke liye

app = Flask(__name__)

# Opera Mini Headers
HEADERS = {"User-Agent": "Opera/9.80 (Android; Opera Mini/36.1.2254/120.184; U; en) Presto/2.12.423 Version/12.16"}

@app.route('/')
def proxy():
    target_url = request.args.get('url', '')

    if target_url:
        # --- STEP 1: SERVER-SIDE WAIT (20 SECONDS) ---
        # Opera Mini ko sirf "Connecting..." dikhega kyunki server response hold pe hai
        time.sleep(20) 

        # --- STEP 2: FETCH & COMPRESS ---
        try:
            if not target_url.startswith('http'):
                target_url = 'https://' + target_url
            
            res = requests.get(target_url, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Sabse bhari cheezein hatana (Ultra Compression)
            for s in soup(["script", "style", "iframe", "video", "link", "svg", "img"]):
                s.decompose()

            # Links ko proxy link mein badalna
            for a in soup.find_all('a', href=True):
                a['href'] = f"/?url={urljoin(target_url, a['href'])}"

            # Simple HTML Output (No CSS/JS)
            content = soup.body.decode_contents() if soup.body else "Page empty hai."
            
            return f'''
            <div style="background:#000; color:#fff; padding:10px; text-align:center;">
                <b>JioLite Proxy</b> | <a href="/" style="color:yellow;">[ HOME ]</a>
            </div>
            <div style="padding:10px;">{content}</div>
            '''
        except:
            return "Error: Site khul nahi rahi. <a href='/'>Wapas jayein</a>"

    # --- HOME UI (Simple Input Box) ---
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif;">
        <h2 style="color:red;">JioLite Browser</h2>
        <p>Website ka address niche dalein:</p>
        <form action="/" method="get">
            <input type="text" name="url" placeholder="example.com" style="width:90%; padding:10px; margin-bottom:10px;">
            <br>
            <button type="submit" style="width:90%; padding:12px; background:red; color:white; border:none; font-weight:bold;">
                OPEN (20s Loading)
            </button>
        </form>
        <p style="font-size:12px; color:#888; margin-top:20px;">Note: Button dabane ke baad browser ki loading bar dekhte rahein.</p>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
