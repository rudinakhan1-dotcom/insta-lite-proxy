from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

app = Flask(__name__)

# Nokia 206 User-Agent is best for Lite sites
HEADERS = {"User-Agent": "Mozilla/5.0 (Nokia206/2.0) AppleWebKit/534.46 (KHTML, like Gecko) Safari/534.46"}

def smart_url(text):
    text = text.strip()
    if "." in text and " " not in text:
        return 'https://' + text if not text.startswith('http') else text
    return f"https://www.google.com/search?q={text.replace(' ', '+')}&gbv=1"

@app.route('/', methods=['GET', 'POST'])
def proxy():
    query = request.args.get('url', '')
    if query:
        target = smart_url(query)
        time.sleep(20) # 20 Sec Wait

        try:
            res = requests.get(target, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')

            # Clean heavy stuff
            for s in soup(["script", "style", "iframe", "ins", "header", "footer", "nav"]):
                s.decompose()

            # --- CSS AI Fix: Har button ko line mein lane ke liye ---
            custom_style = """
            <style>
                * { box-sizing: border-box; }
                body { font-family: sans-serif; background: #fff; margin: 0; padding: 5px; color: #000; }
                /* Har link ko button jaisa banao */
                a { display: block !important; width: 100% !important; padding: 12px !important; margin: 5px 0 !important; 
                    background: #f9f9f9 !important; border: 1px solid #ddd !important; border-radius: 4px !important; 
                    text-decoration: none !important; color: #333 !important; font-size: 14px !important; text-align: left; }
                /* Inputs ko fix karo */
                input[type="text"], input[type="search"] { width: 100% !important; padding: 12px !important; 
                    margin: 8px 0 !important; border: 2px solid #333 !important; border-radius: 5px !important; display: block; }
                /* Buttons ko fix karo */
                button, input[type="submit"] { width: 100% !important; background: #333 !important; color: #fff !important; 
                    padding: 15px !important; border: none !important; border-radius: 5px !important; 
                    font-weight: bold !important; display: block !important; margin: 10px 0 !important; }
                img { max-width: 100px; height: auto; }
                table, tr, td { display: block !important; width: 100% !important; } /* Tables ko todna */
            </style>
            """

            for tag in soup.find_all(['a', 'form']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target, tag['href'])}"
                elif tag.name == 'form':
                    tag['action'] = f"/?url={urljoin(target, tag.get('action', ''))}"
                    tag['method'] = 'GET'

            content = soup.body.decode_contents() if soup.body else "Empty content"
            
            return f"<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0'>{custom_style}</head><body>" \
                   f"<div style='background:#000;color:#fff;padding:10px;text-align:center;'><b>SMART GATEWAY</b> | <a href='/' style='display:inline;color:yellow;background:none;border:none;padding:0;'>[HOME]</a></div>" \
                   f"{content}</body></html>"
        except:
            return "Connection Error. <a href='/'>Retry</a>"

    return '''
    <div style="text-align:center; padding:40px 10px; font-family:sans-serif;">
        <h2 style="color:#333;">Jio<span style="color:#f44336;">Lite</span> Gateway</h2>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="Search or URL" style="width:90%; padding:15px; border:2px solid #333; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#333; color:white; border:none; border-radius:10px; font-weight:bold;">OPEN (20s WAIT)</button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
