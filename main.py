from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# High Compatibility Header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def repair_url(u):
    u = u.strip()
    if not u: return ""
    if "facebook.com" in u.lower(): return "https://mbasic.facebook.com"
    if "." not in u or " " in u:
        return f"https://www.google.com/search?q={u.replace(' ', '+')}&gbv=1"
    return u if u.startswith('http') else 'https://' + u

@app.route('/', methods=['GET', 'POST'])
def power_proxy():
    target = request.args.get('url') or request.args.get('q', '')
    
    if not target:
        return '''<center style="padding:50px 10px; font-family:sans-serif;">
            <h2 style="color:#d32f2f;">Super <span style="color:#333;">Gateway</span></h2>
            <form action="/" method="GET">
                <input type="text" name="url" placeholder="Search or URL" style="width:90%; padding:15px; border:2px solid #333; border-radius:10px;">
                <br><br><button type="submit" style="width:95%; padding:15px; background:#333; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN (20s)</button>
            </form></center>'''

    real_url = repair_url(target)
    time.sleep(20) # Server processing delay

    try:
        # Session use karna zaroori hai taaki second page ko cookies milein
        session = requests.Session()
        res = session.get(real_url, headers=HEADERS, timeout=30, allow_redirects=True)
        
        # Agar status code 200 nahi hai toh error dikhao
        if res.status_code != 200:
            return f"Site error {res.status_code}. <a href='/'>Retry</a>"

        soup = BeautifulSoup(res.text, 'html.parser')

        # Clean JS but keep structure
        for s in soup(["script", "iframe", "ins", "embed"]):
            s.decompose()

        # --- ABSOLUTE LINK REWRITE (Second Page Fix) ---
        for tag in soup.find_all(['a', 'form', 'img', 'link', 'area']):
            # Links fix
            if tag.name == 'a' and tag.get('href'):
                tag['href'] = f"/?url={urljoin(real_url, tag['href'])}"
            
            # Form fix (Zaruri for search/login)
            elif tag.name == 'form':
                tag['action'] = '/'
                tag['method'] = 'GET'
                for i in tag.find_all('input'):
                    if i.get('name') in ['q', 'query', 'p']: i['name'] = 'url'
            
            # Image fix
            elif tag.name == 'img' and tag.get('src'):
                tag['src'] = urljoin(real_url, tag['src'])
                tag['style'] = "max-width:140px; height:auto; display:block;"

        # CSS for Mobile
        style = "<style>body{font-family:sans-serif;margin:0;padding:5px;} a{display:block;padding:12px;margin:5px 0;background:#f1f1f1;border:1px solid #ccc;text-decoration:none;color:#000;border-radius:5px;} input[type='text']{width:95%;padding:12px;margin:10px 0;border:2px solid #333;}</style>"
        
        content = soup.body.decode_contents() if soup.body else "Blank content received."
        return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{style}</head><body><div style='background:#000;padding:10px;text-align:center;'><a href='/' style='background:none;color:yellow;display:inline;border:none;'>[ HOME ]</a></div>{content}</body></html>"

    except Exception as e:
        return f"Loading Error: {str(e)}. <a href='/'>Wapas jayein</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
