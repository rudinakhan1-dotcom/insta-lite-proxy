from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Basic Header
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0"}

@app.route('/', methods=['GET'])
def simple_proxy():
    u = request.args.get('url', '')
    if not u:
        return '''
        <center>
            <h2>Saada Proxy</h2>
            <form action="/" method="GET">
                <input type="text" name="url" placeholder="Search or URL" style="width:80%;padding:10px;"><br><br>
                <button type="submit" style="padding:10px 20px;">Open (Wait 20s)</button>
            </form>
        </center>
        '''

    # Google/URL Fix logic
    if "." not in u or " " in u:
        target = f"https://www.google.com/search?q={u.replace(' ', '+')}&gbv=1"
    else:
        target = u if u.startswith('http') else 'https://' + u

    time.sleep(20) # Aapka 20s wait logic

    try:
        r = requests.get(target, headers=HEADERS, timeout=20)
        s = BeautifulSoup(r.text, 'html.parser')

        # Sab kuch saaf kardo (Saada Mode)
        for tag in s(["script", "style", "iframe", "ins"]):
            tag.decompose()

        # Saare links ko proxy banao
        for a in s.find_all('a', href=True):
            a['href'] = f"/?url={urljoin(target, a['href'])}"

        return f"<html><body style='font-family:sans-serif;'><a href='/'>[ HOME ]</a><hr>{s.body.decode_contents()}</body></html>"
    except:
        return "Nahi khul raha. <a href='/'>Wapas jayein</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
