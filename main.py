from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    target_url = request.args.get('url', '')

    if target_url:
        # Server-Side Wait (Dono logic ke liye 20 sec)
        time.sleep(20)

        try:
            if not target_url.startswith('http'):
                target_url = 'https://' + target_url

            # GET aur POST dono handle karein (Y2mate search fix)
            if request.method == 'POST':
                res = requests.post(target_url, data=request.form, headers=HEADERS, timeout=15)
            else:
                res = requests.get(target_url, headers=HEADERS, timeout=15)

            soup = BeautifulSoup(res.text, 'html.parser')

            # Compression: Scripts aur Ads hatayein
            for s in soup(["script", "style", "iframe", "ins"]):
                s.decompose()

            # Links aur Forms ko Rewrite karein (Y2mate fix)
            for a in soup.find_all(['a', 'form'], href=True, action=True):
                if a.name == 'a':
                    a['href'] = f"/?url={urljoin(target_url, a['href'])}"
                else: # Forms (Search bars)
                    a['action'] = f"/?url={urljoin(target_url, a['action'])}"

            return f'''
            <div style="background:#333; color:white; padding:10px; text-align:center;">
                <b>JioLite Proxy</b> | <a href="/" style="color:yellow;">[ HOME ]</a>
            </div>
            {soup.body.decode_contents() if soup.body else "Page loading error."}
            '''
        except Exception as e:
            return f"Error: {str(e)}. <a href='/'>Wapas jayein</a>"

    # Home Page
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif;">
        <h2 style="color:red;">JioLite Browser</h2>
        <form action="/" method="get">
            <input type="text" name="url" placeholder="Enter Website (e.g. y2mate.is)" style="width:90%; padding:10px;">
            <br><br>
            <button type="submit" style="width:90%; padding:12px; background:red; color:white; border:none; font-weight:bold;">OPEN WEBSITE</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
