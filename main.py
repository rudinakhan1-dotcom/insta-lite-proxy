from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def fix_url(text):
    text = text.strip().lower()
    if not text: return ""
    if "facebook.com" in text: return "https://mbasic.facebook.com"
    if "duckduckgo" in text: return "https://html.duckduckgo.com/html/"
    if "." in text and " " not in text:
        return 'https://' + text if not text.startswith('http') else text
    return f"https://www.google.com/search?q={text.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def proxy():
    url_param = request.args.get('url') or request.args.get('q') or ""
    
    if url_param:
        target = fix_url(url_param)
        time.sleep(20) # Background Delay

        try:
            res = requests.get(target, headers=HEADERS, timeout=25, allow_redirects=True)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Clean Scripts & Styles
            for s in soup(["script", "style", "iframe", "ins"]):
                s.decompose()

            # Fix Links & Forms
            for tag in soup.find_all(['a', 'form', 'img']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target, tag['href'])}"
                elif tag.name == 'form':
                    tag['action'] = '/'
                    tag['method'] = 'GET'
                    for inp in tag.find_all('input'):
                        if inp.get('name') in ['q', 'query']: inp['name'] = 'url'
                elif tag.name == 'img' and tag.get('src'):
                    tag['src'] = urljoin(target, tag['src'])

            style = "<style>body{font-family:sans-serif;margin:0;padding:5px;} a{display:block;padding:12px;margin:5px 0;background:#eee;border-radius:5px;text-decoration:none;color:#000;} input[type='text']{width:90%;padding:12px;margin:10px 0;border:2px solid #000;} button{width:95%;padding:15px;background:#000;color:#fff;font-weight:bold;border-radius:5px;}</style>"

            content = soup.body.decode_contents() if soup.body else "Error Loading Content"
            return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{style}</head><body><div style='background:#000;padding:10px;text-align:center;'><a href='/' style='background:none;color:yellow;display:inline;'>[ HOME ]</a></div>{content}</body></html>"
        except Exception as e:
            return f"Error: {str(e)}. <a href='/'>Retry</a>"

    return '''
    <div style="text-align:center; padding:50px 10px; font-family:sans-serif;">
        <h2>Smart Proxy</h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="Search or URL">
            <button type="submit">OPEN (20s WAIT)</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
