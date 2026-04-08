from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Modern Desktop Header taaki Google block na kare
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def smart_url(text):
    text = text.strip()
    if "." in text and " " not in text:
        return 'https://' + text if not text.startswith('http') else text
    # gbv=1 bahut zaruri hai Google bypass ke liye
    return f"https://www.google.com/search?q={text.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def proxy():
    query = request.args.get('url') or request.args.get('q', '')
    
    if query:
        target = smart_url(query)
        time.sleep(20) # Server-side delay

        try:
            res = requests.get(target, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Clean Scripts & Ads
            for s in soup(["script", "style", "iframe", "ins"]):
                s.decompose()

            # --- FORM & BUTTON FIX ---
            for form in soup.find_all('form'):
                form['action'] = '/' 
                form['method'] = 'GET'
                for inp in form.find_all('input'):
                    if inp.get('name') in ['q', 'query']: 
                        inp['name'] = 'url'

            # Links Rewrite
            for a in soup.find_all('a', href=True):
                a['href'] = f"/?url={urljoin(target, a['href'])}"

            # Layout Design (JioBharat Optimized)
            custom_style = """
            <style>
                body { font-family: sans-serif; background: #fff; padding: 5px; }
                a, button, input[type='submit'] { display: block; width: 98%; padding: 15px; margin: 8px 0; 
                    background: #f1f1f1; border: 1px solid #ccc; text-decoration: none; color: #000; 
                    border-radius: 8px; font-weight: bold; text-align: left; }
                input[type='text'] { width: 95%; padding: 15px; border: 2px solid #333; border-radius: 8px; }
            </style>
            """

            content = soup.body.decode_contents() if soup.body else "No Content Available"
            return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{custom_style}</head><body>" \
                   f"<div style='background:#333;color:#fff;padding:12px;text-align:center;'><a href='/' style='background:none;border:none;color:yellow;display:inline;padding:0;'>[ SEARCH AGAIN ]</a></div>" \
                   f"{content}</body></html>"
        except:
            return "Connection Timeout. <a href='/'>Retry</a>"

    return '''
    <div style="text-align:center; padding:50px 10px; font-family:sans-serif;">
        <h2 style="color:#4285F4;">Smart <span style="color:#EA4335;">Proxy</span></h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="Search Google or Enter URL" style="width:90%; padding:15px; border:2px solid #333; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#333; color:white; border:none; border-radius:10px; font-weight:bold;">SEARCH / OPEN</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
