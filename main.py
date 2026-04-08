from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124"}

def smart_url_repair(url):
    url = url.replace('%20', '').replace(' ', '').strip().lower()
    if not url: return ""
    if "." not in url: url += ".is" # Y2mate ke liye default .is
    if not url.startswith(('http://', 'https://')): url = 'https://' + url
    return url

@app.route('/', methods=['GET', 'POST'])
def proxy():
    raw_url = request.args.get('url', '')
    target_url = smart_url_repair(raw_url) if raw_url else ""

    if target_url:
        # 20 Seconds Background Wait
        time.sleep(20)

        try:
            # Y2mate Search handling
            if request.method == 'POST' or 'search' in target_url:
                res = requests.post(target_url, data=request.form, headers=HEADERS, timeout=15)
            else:
                res = requests.get(target_url, headers=HEADERS, timeout=15)

            soup = BeautifulSoup(res.text, 'html.parser')

            # --- SMART COMPRESSION ---
            for s in soup(["script", "iframe", "ins", "style", "video"]):
                s.decompose()

            # Fix Links & Forms for No-JS Browsers
            for tag in soup.find_all(['a', 'form']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target_url, tag['href'])}"
                elif tag.name == 'form':
                    # Y2mate ke search form ko force karna
                    tag['action'] = f"/?url={urljoin(target_url, tag.get('action', ''))}"
                    tag['method'] = 'POST'

            return f'''
            <div style="background:#000; color:white; padding:10px; text-align:center;">
                <b>AI Smart View</b> | <a href="/" style="color:yellow;">[ HOME ]</a>
            </div>
            <div style="padding:10px; font-family:sans-serif;">
                {soup.body.decode_contents() if soup.body else "No Results Found."}
            </div>
            '''
        except Exception as e:
            return f"Error: {str(e)}. <a href='/'>Back</a>"

    return '''
    <div style="text-align:center; padding:40px 10px; font-family:sans-serif;">
        <h2 style="color:#f44336;">Smart JioProxy</h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="y2mate.is" style="width:90%; padding:15px; border:2px solid #f44336; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#f44336; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN SITE</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
