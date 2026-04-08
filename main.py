import os
from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

def fix_url(u):
    u = u.strip()
    if not u: return ""
    if "facebook.com" in u.lower(): return "https://mbasic.facebook.com"
    if "." not in u or " " in u:
        return f"https://www.google.com/search?q={u.replace(' ', '+')}&gbv=1"
    return u if u.startswith('http') else 'https://' + u

@app.route('/', methods=['GET', 'POST'])
def proxy():
    q = request.args.get('url') or request.args.get('q', '')
    if not q:
        return '<center style="padding:50px;"><h2>JioProxy v4</h2><form action="/" method="GET"><input type="text" name="url" placeholder="Search or URL" style="width:80%;padding:10px;"><br><br><button type="submit" style="padding:10px 20px;">Open Page</button></form></center>'

    target = fix_url(q)
    time.sleep(15) 

    try:
        session = requests.Session()
        res = session.get(target, headers=HEADERS, timeout=30, allow_redirects=True)
        soup = BeautifulSoup(res.text, 'html.parser')

        for s in soup(["script", "style", "iframe"]):
            s.decompose()

        for tag in soup.find_all(['a', 'form', 'img']):
            if tag.name == 'a' and tag.get('href'):
                tag['href'] = f"/?url={urljoin(target, tag['href'])}"
            elif tag.name == 'form':
                tag['action'] = '/'
                tag['method'] = 'GET'
                for i in tag.find_all('input'):
                    if i.get('name') in ['q', 'query']: i['name'] = 'url'
            elif tag.name == 'img' and tag.get('src'):
                tag['src'] = urljoin(target, tag['src'])
                tag['style'] = "max-width:150px; height:auto;"

        return f"<html><body style='font-family:sans-serif;'><a href='/'>[ HOME ]</a><hr>{soup.body.decode_contents() if soup.body else 'Error'}</body></html>"
    except Exception as e:
        return f"Error: {str(e)}. <a href='/'>Retry</a>"

if __name__ == "__main__":
    # Render ke liye port 10000 zaroori hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
