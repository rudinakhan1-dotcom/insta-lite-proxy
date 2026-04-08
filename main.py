from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# User-Agent optimized for compatibility, not too old
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def smart_url_repair(url):
    url = url.strip().lower()
    if not url: return ""
    # Agar search hai toh.com na lagayein, direct search ho.
    if "." in url and " " not in url:
        return 'https://' + url if not url.startswith('http') else url
    # Google Search URL with gbv=1 for basic view
    return f"https://www.google.com/search?q={url.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def simple_lite_proxy():
    q = request.args.get('url') or request.args.get('q', '')
    if not q:
        # HOME UI (Centered & Big Buttons)
        return '''
        <center style="padding-top:40px; font-family:sans-serif;">
            <h2 style="color:#222;">Smart <span style="color:#d32f2f;">Gateway</span></h2>
            <form action="/" method="GET">
                <input type="text" name="url" placeholder="google or facebook.com" style="width:90%; padding:15px; border:1px solid #d32f2f; border-radius:10px; font-size:16px;">
                <br><br>
                <button type="submit" style="width:95%; padding:15px; background:#d32f2f; color:white; border:none; border-radius:10px; font-weight:bold; font-size:16px;">
                    Open (20s Wait)
                </button>
            </form>
            <p style="color:#666; font-size:12px;">Image & Form Support Enabled</p>
        </center>
        '''

    target_url = smart_url_repair(q)
    
    # --- 20 SECONDS BACKGROUND WAIT ---
    time.sleep(20)

    try:
        # Universal session to handle cookies/redirects
        session = requests.Session()
        res = session.get(target_url, headers=HEADERS, timeout=25, allow_redirects=True)
        soup = BeautifulSoup(res.text, 'html.parser')

        # --- HEAVY COMPRESSION (Not Deletion) ---
        # Sirf Scripts aur Faltu Ads hatao, Stylesheet ko mat chhero layout na bigde
        for tag in soup(["script", "iframe", "ins", "embed"]):
            tag.decompose()

        # --- SMART REWRITE (Links, Forms, & Images) ---
        for tag in soup.find_all(['a', 'form', 'img']):
            # Link Rewrite for Proxy
            if tag.name == 'a' and tag.get('href'):
                tag['href'] = f"/?url={urljoin(target_url, tag['href'])}"
            
            # Form Rewrite for Search to work
            elif tag.name == 'form':
                tag['action'] = '/' # Redirect forms back to our proxy
                tag['method'] = 'GET'
                for i in tag.find_all('input'):
                    # Check forms if they have search input names like 'q', 'query', 'p'
                    if i.get('name') in ['q', 'query', 'p']: i['name'] = 'url'
            
            # Image Resize for JioBharat
            elif tag.name == 'img' and tag.get('src'):
                # Original Image ko humne block nahi kiya, bas use chota (Lite) bana diya.
                tag['src'] = urljoin(target_url, tag['src'])
                tag['style'] = "max-width:150px; height:auto; display:block; margin:5px 0; border:1px solid #ccc; border-radius:5px;"

        # --- DESIGN PATCH (Simple & Vertical) ---
        design_fix = """
        <style>
            body { font-family: sans-serif; background: #fff; margin: 0; padding: 5px; color: #000; }
            .top-gateway { background: #d32f2f; color: white; padding: 12px; text-align: center; font-weight: bold; position: sticky; top: 0; z-index: 999; }
            .content-area { padding: 5px; }
            /* Links ko bade button jaisa banana */
            a { display: block !important; width: 100% !important; padding: 12px !important; margin: 5px 0 !important; 
                background: #f4f4f4 !important; color: #333 !important; text-decoration: none !important; border: 1px solid #ddd !important; border-radius: 5px !important; font-size: 14px !important; text-align: left; }
            /* Inputs & Buttons ko fix karna */
            input[type='text'], input[type='search'] { width: 100% !important; padding: 12px !important; margin: 10px 0 !important; border: 2px solid #333 !important; border-radius: 8px !important; display: block; }
            button, input[type='submit'] { width: 100% !important; background: #d32f2f !important; color: #fff !important; 
                padding: 15px !important; border: none !important; border-radius: 8px !important; font-weight: bold !important; display: block; margin: 10px 0 !important; font-size: 16px; }
            table, tr, td { display: block !important; width: 100% !important; } /* Responsive Tables */
        </style>
        """

        content = soup.body.decode_contents() if soup.body else "Page content is missing or load failed."
        
        return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{design_fix}</head><body>" \
               f"<div class='top-gateway'><a href='/' style='background:none; border:none; color:yellow; display:inline; padding:0; font-size:16px;'>[ NEW SEARCH ]</a></div>" \
               f"<div class='content-area'>{content}</div></body></html>"
    except Exception as e:
        return f"Error: {str(e)}. <a href='/'>Wapas jayein</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
