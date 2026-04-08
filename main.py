from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Ultra-Lite User Agent for Feature Phones
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def smart_url_repair(url):
    url = url.replace('%20', '').replace(' ', '').strip().lower()
    if not url: return ""
    if "." not in url: url += ".is"
    if not url.startswith(('http://', 'https://')): url = 'https://' + url
    return url

@app.route('/', methods=['GET', 'POST'])
def proxy():
    raw_url = request.args.get('url', '')
    target_url = smart_url_repair(raw_url) if raw_url else ""

    if target_url:
        # --- PHASE 1: BACKGROUND CONVERSATION WAIT (20 SEC) ---
        time.sleep(20)

        try:
            # --- PHASE 2: BACKGROUND SEARCH LOADING ---
            # Hum server-side par hi Y2mate ko result nikalne par majboor karenge
            if request.method == 'POST':
                res = requests.post(target_url, data=request.form, headers=HEADERS, timeout=20)
            else:
                res = requests.get(target_url, headers=HEADERS, timeout=20)

            soup = BeautifulSoup(res.text, 'html.parser')

            # Sabhi loading wheels aur scripts ko pehle hi khatam karo
            for s in soup(["script", "style", "iframe", "ins", "link"]):
                s.decompose()

            # Y2mate ke result table ko fix karna
            for tag in soup.find_all(['a', 'form']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target_url, tag['href'])}"
                elif tag.name == 'form':
                    tag['action'] = f"/?url={urljoin(target_url, tag.get('action', ''))}"
                    tag['method'] = 'POST'

            # Result page return karna
            return f'''
            <div style="background:#cc0000; color:white; padding:10px; text-align:center; font-family:sans-serif;">
                <b>AI Results Loaded</b> | <a href="/" style="color:yellow; text-decoration:none;">[ NEW SEARCH ]</a>
            </div>
            <div style="padding:15px; font-family:sans-serif; background:#fff;">
                {soup.body.decode_contents() if soup.body else "Result load nahi hua. Wapas try karein."}
            </div>
            '''
        except Exception as e:
            return f"Error: {str(e)}. <a href='/'>Back</a>"

    return '''
    <div style="text-align:center; padding:50px 10px; font-family:sans-serif;">
        <h2 style="color:#cc0000;">Smart Downloader</h2>
        <p style="font-size:12px;">URL dalein aur 20 sec wait karein.</p>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="y2mate.is" style="width:85%; padding:15px; border:1px solid #cc0000; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:90%; padding:15px; background:#cc0000; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN & COMPRESS</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
