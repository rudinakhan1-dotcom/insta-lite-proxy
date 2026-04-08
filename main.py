from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

# Opera Mini ko pasand aane wala headers
HEADERS = {"User-Agent": "Opera/9.80 (Android; Opera Mini/36.1.2254/120.184; U; en) Presto/2.12.423 Version/12.16"}

@app.route('/')
def home():
    url_to_open = request.args.get('url', '')

    # STEP 1: Timer Page (Har Link se pehle 20 Seconds wait)
    # Isme koi animation nahi hai, sirf simple text taaki Opera Mini support kare
    wait = request.args.get('wait', '0')
    if url_to_open and wait == '0':
        return f'''
        <html><head><meta http-equiv="refresh" content="20; url=/?url={url_to_open}&wait=1"></head>
        <body style="text-align:center; padding-top:100px; font-family:sans-serif;">
            <h2>Processing...</h2>
            <p>Please wait <b>20 seconds</b> for compression.</p>
            <p style="color:red;">Do not go back.</p>
        </body></html>
        '''

    # STEP 2: Compression Logic (20 Sec baad yahan aayega)
    if url_to_open and wait == '1':
        try:
            if not url_to_open.startswith('http'):
                url_to_open = 'https://' + url_to_open
            
            res = requests.get(url_to_open, headers=HEADERS, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Sabse bada compression: Scripts aur Styles ko khatam karna
            for s in soup(["script", "style", "iframe", "video", "link", "svg"]):
                s.decompose()

            # Links ko proxy link mein badalna
            for a in soup.find_all('a', href=True):
                a['href'] = f"/?url={urljoin(url_to_open, a['href'])}"

            # Page ko bahut halka (Lite) banana
            return f'''
            <div style="background:#000; color:#fff; padding:10px; text-align:center;">
                <a href="/" style="color:yellow;">[ BACK TO HOME ]</a>
            </div>
            <div style="padding:10px; font-family:serif;">{soup.body.decode_contents()}</div>
            '''
        except:
            return "Site block hai ya address galat hai. <a href='/'>Wapas jayein</a>"

    # STEP 3: Simple Home UI (Opera Mini Best Support)
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif;">
        <h1 style="color:red;">Jio<span style="color:black;">Lite</span></h1>
        <form action="/" method="get">
            <input type="text" name="url" placeholder="Enter Website Address" style="width:90%; padding:10px;">
            <br><br>
            <button type="submit" style="width:90%; padding:12px; background:red; color:white; border:none;">OPEN LITE VERSION</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
