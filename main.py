from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Ye header site ko batata hai ki hum ek asli browser hain
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Upgrade-Insecure-Requests": "1"
}

def fix_target(url):
    url = url.strip().lower()
    if not url: return ""
    if "facebook.com" in url: return "https://mbasic.facebook.com"
    if "youtube.com" in url or "youtu.be" in url:
        return f"https://www.google.com/search?q={url}+download+link&gbv=1"
    if "." not in url or " " in url:
        return f"https://www.google.com/search?q={url.replace(' ', '+')}&gbv=1"
    return 'https://' + url if not url.startswith('http') else url

@app.route('/', methods=['GET', 'POST'])
def smart_render():
    q = request.args.get('url') or request.args.get('q', '')
    
    if not q:
        return '''<center style="padding:50px 10px; font-family:sans-serif;">
            <h2 style="color:#0078D4;">Jio<span style="color:#333;">Smart</span> Proxy</h2>
            <form action="/" method="GET">
                <input type="text" name="url" placeholder="Search or Website Link" style="width:90%; padding:15px; border:2px solid #0078D4; border-radius:10px;">
                <br><br>
                <button type="submit" style="width:95%; padding:15px; background:#0078D4; color:white; border:none; border-radius:10px; font-weight:bold;">LOAD PAGE (20s)</button>
            </form>
            <p style="color:#666;">Images & Forms: ENABLED</p></center>'''

    target = fix_target(q)
    time.sleep(20) # Server processing wait

    try:
        # Session se cookies handle hongi taaki login/second page chale
        session = requests.Session()
        res = session.get(target, headers=HEADERS, timeout=30, allow_redirects=True)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Sabse bada kaam: Scripts ko hatau par unka kaam kiya hua data rehne do
        for s in soup(["script", "iframe", "ins", "embed"]):
            s.decompose()

        # Design Patch (Images ko resize karna)
        for img in soup.find_all('img', src=True):
            img['src'] = urljoin(target, img['src'])
            img['style'] = "max-width:160px; height:auto; display:block; margin:5px 0; border:1px solid #ddd;"

        # All Links & Forms rewrite (Absolute URLs)
        for tag in soup.find_all(['a', 'form']):
            if tag.name == 'a' and tag.get('href'):
                tag['href'] = f"/?url={urljoin(target, tag['href'])}"
            elif tag.name == 'form':
                tag['action'] = '/'
                tag['method'] = 'GET'
                for i in tag.find_all('input'):
                    if i.get('name') in ['q', 'query', 'p']: i['name'] = 'url'

        style = """<style>
            body { font-family: sans-serif; background: #fff; margin: 0; padding: 5px; }
            .header { background: #0078D4; color: white; padding: 12px; text-align: center; }
            a { display: block; padding: 15px; margin: 8px 0; background: #f4f4f4; border: 1px solid #ccc; text-decoration: none; color: #000; border-radius: 8px; font-weight: bold; }
            input[type='text'] { width: 95%; padding: 12px; border: 2px solid #333; }
        </style>"""

        content = soup.body.decode_contents() if soup.body else "Page content error."
        return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{style}</head><body>" \
               f"<div class='header'><a href='/' style='background:none; border:none; color:yellow; display:inline; padding:0;'>[ HOME ]</a></div>" \
               f"<div>{content}</div></body></html>"

    except Exception as e:
        return f"Loading Failed: {str(e)}. <a href='/'>Retry</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
