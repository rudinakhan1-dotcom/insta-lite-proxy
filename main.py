from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

@app.route('/', methods=['GET', 'POST'])
def proxy():
    target_url = request.args.get('url', '')

    # 1. URL CLEANING: Spaces aur %20 ko auto-remove karein
    if target_url:
        target_url = target_url.replace('%20', '').replace(' ', '').strip()
        if not target_url.startswith('http'):
            target_url = 'https://' + target_url

        # 2. SERVER-SIDE SLEEP: 20 seconds wait
        time.sleep(20)

        try:
            # POST handling (Y2mate Start button ke liye)
            if request.method == 'POST':
                res = requests.post(target_url, data=request.form, headers=HEADERS, timeout=15)
            else:
                res = requests.get(target_url, headers=HEADERS, timeout=15)

            soup = BeautifulSoup(res.text, 'html.parser')

            # 3. LITE COMPRESSION
            for s in soup(["script", "iframe", "ins", "style"]):
                s.decompose()

            # 4. FORM & LINK REWRITE: Taaki button click karne par hamari site khule
            for tag in soup.find_all(['a', 'form']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target_url, tag['href'])}"
                elif tag.name == 'form' and tag.get('action'):
                    tag['action'] = f"/?url={urljoin(target_url, tag['action'])}"
                    tag['method'] = 'POST' # Force POST for search buttons

            return f'''
            <div style="background:#333; color:white; padding:10px; text-align:center;">
                <b>JioLite Mode</b> | <a href="/" style="color:yellow;">[ HOME ]</a>
            </div>
            <div style="padding:10px;">{soup.body.decode_contents() if soup.body else "Error Loading Content"}</div>
            '''
        except Exception as e:
            return f"Connection Error: {str(e)}. <a href='/'>Wapas jayein</a>"

    # HOME PAGE
    return '''
    <div style="text-align:center; padding:30px; font-family:sans-serif;">
        <h2 style="color:red;">JioLite Gateway</h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="y2mate.is" style="width:85%; padding:15px; border:1px solid #333; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:90%; padding:15px; background:red; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN SITE</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
