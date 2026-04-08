from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Nokia206/2.0) AppleWebKit/534.46 (KHTML, like Gecko) Safari/534.46"}

def smart_url(text):
    text = text.strip()
    if "." in text and " " not in text:
        return 'https://' + text if not text.startswith('http') else text
    # gbv=1 Google ka basic version hai jo bina JS ke chalta hai
    return f"https://www.google.com/search?q={text.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def proxy():
    # 'q' Google ka standard search parameter hai, 'url' hamara hai
    query = request.args.get('url') or request.args.get('q', '')
    
    if query:
        target = smart_url(query)
        time.sleep(20) # Background Process Wait

        try:
            res = requests.get(target, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Clean heavy stuff
            for s in soup(["script", "style", "iframe", "ins"]):
                s.decompose()

            # --- SEARCH BUTTON FIX ---
            for form in soup.find_all('form'):
                form['action'] = '/' # Saara data hamare proxy par aaye
                form['method'] = 'GET'
                # Input ka naam 'url' kar do taaki hamara proxy samajh sake
                for inp in form.find_all('input', attrs={'name': True}):
                    if inp['name'] in ['q', 'query', 'p']: 
                        inp['name'] = 'url'

            # Links rewrite
            for a in soup.find_all('a', href=True):
                a['href'] = f"/?url={urljoin(target, a['href'])}"

            # Layout CSS
            custom_style = "<style>body{font-family:sans-serif;padding:10px;} a, button, input[type='submit']{display:block;width:95%;padding:12px;margin:10px 0;background:#f0f0f0;border:1px solid #ccc;text-decoration:none;color:#000;border-radius:5px;} input[type='text']{width:90%;padding:12px;border:1px solid #333;}</style>"

            content = soup.body.decode_contents() if soup.body else "No Content"
            return f"<html><head>{custom_style}</head><body>" \
                   f"<div style='background:#333;color:#fff;padding:10px;text-align:center;'><a href='/' style='background:none;border:none;color:yellow;display:inline;'>[ NEW SEARCH ]</a></div>" \
                   f"{content}</body></html>"
        except:
            return "Error loading results. <a href='/'>Retry</a>"

    return '''
    <div style="text-align:center; padding:50px 10px; font-family:sans-serif;">
        <h2 style="color:#4285F4;">Smart <span style="color:#34A853;">JioProxy</span></h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="Search Google or URL" style="width:90%; padding:15px; border:2px solid #4285F4; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#4285F4; color:white; border:none; border-radius:10px; font-weight:bold;">SEARCH / OPEN</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
