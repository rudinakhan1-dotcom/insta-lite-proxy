from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Sabse compatible header jo block nahi hota
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def fix_url(text):
    text = text.strip()
    if "." in text and " " not in text:
        return 'https://' + text if not text.startswith('http') else text
    return f"https://www.google.com/search?q={text.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def proxy():
    url_param = request.args.get('url') or request.args.get('q', '')
    
    if url_param:
        target = fix_url(url_param)
        time.sleep(20) # 20s Background Wait

        try:
            # Facebook aur Google bypass ke liye cookies handle karna
            session = requests.Session()
            res = session.get(target, headers=HEADERS, timeout=20, allow_redirects=True)
            soup = BeautifulSoup(res.text, 'html.parser')

            # --- SMART COMPRESSION (Not Deletion) ---
            # Hum sirf Scripts hatayenge, Styles nahi taaki layout na bigde
            for s in soup(["script", "iframe", "ins"]):
                s.decompose()

            # Links Rewrite
            for tag in soup.find_all(['a', 'form', 'img']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target, tag['href'])}"
                elif tag.name == 'form':
                    tag['action'] = '/'
                    tag['method'] = 'GET'
                    for inp in form.find_all('input'):
                        if inp.get('name') in ['q', 'query']: inp['name'] = 'url'
                elif tag.name == 'img' and tag.get('src'):
                    tag['src'] = urljoin(target, tag['src'])
                    tag['style'] = "max-width:100%; height:auto;"

            # Layout Patch (Buttons ko sahi jagah rakhne ke liye)
            layout_patch = """
            <style>
                body { font-family: sans-serif; margin: 0; padding: 0; background: #fff; }
                .top-bar { background: #333; color: yellow; padding: 10px; text-align: center; position: sticky; top: 0; z-index: 100; }
                input[type='text'], input[type='search'] { width: 90% !important; padding: 12px !important; margin: 5px auto !important; display: block !important; border: 2px solid #333 !important; }
                button, input[type='submit'] { width: 95% !important; padding: 15px !important; background: #333 !important; color: #fff !important; border: none !important; display: block !important; margin: 10px auto !important; font-weight: bold !important; }
            </style>
            """

            content = soup.body.decode_contents() if soup.body else "Page Error"
            return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{layout_patch}</head><body>" \
                   f"<div class='top-bar'><a href='/' style='color:yellow; text-decoration:none;'>[ NEW SEARCH ]</a></div>" \
                   f"<div style='padding:5px;'>{content}</div></body></html>"
        except Exception as e:
            return f"Error: {str(e)}. <a href='/'>Wapas jayein</a>"

    return '''
    <div style="text-align:center; padding:50px 10px; font-family:sans-serif;">
        <h2 style="color:#333;">Universal <span style="color:#f44336;">Gateway</span></h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="Search Google, FB, or URL" style="width:90%; padding:15px; border:2px solid #333; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#333; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN SECURELY (20s)</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
