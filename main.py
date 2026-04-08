from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

def smart_url_repair(url):
    """AI logic to fix broken URLs"""
    url = url.replace('%20', '').replace(' ', '').strip().lower()
    if not url: return ""
    
    # Agar dot nahi hai toh .com lagao
    if "." not in url:
        url += ".com"
    
    # Protocol fix (https add karna)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    return url

@app.route('/', methods=['GET', 'POST'])
def proxy():
    raw_url = request.args.get('url', '')
    target_url = smart_url_repair(raw_url) if raw_url else ""

    if target_url:
        # 20 Seconds Background Wait
        time.sleep(20)

        try:
            if request.method == 'POST':
                res = requests.post(target_url, data=request.form, headers=HEADERS, timeout=15)
            else:
                res = requests.get(target_url, headers=HEADERS, timeout=15)

            soup = BeautifulSoup(res.text, 'html.parser')

            # --- SMART COMPRESSION ---
            for s in soup(["script", "iframe", "ins", "style", "video"]):
                s.decompose()

            # Fix Links, Forms, and Images
            for tag in soup.find_all(['a', 'form', 'img']):
                if tag.name == 'a' and tag.get('href'):
                    tag['href'] = f"/?url={urljoin(target_url, tag['href'])}"
                    tag['style'] = "display:block; padding:8px; color:#d32f2f; text-decoration:none;"
                elif tag.name == 'form' and tag.get('action'):
                    tag['action'] = f"/?url={urljoin(target_url, tag['action'])}"
                    tag['method'] = 'POST'
                elif tag.name == 'img' and tag.get('src'):
                    # Images ko chhota aur lite banana
                    tag['src'] = urljoin(target_url, tag['src'])
                    tag['style'] = "max-width:100px; height:auto; display:block;"

            return f'''
            <div style="background:#d32f2f; color:white; padding:10px; text-align:center; font-family:sans-serif;">
                <b>AI Optimized View</b> | <a href="/" style="color:yellow;">[ NEW URL ]</a>
            </div>
            <div style="padding:10px; font-family:sans-serif;">
                {soup.body.decode_contents() if soup.body else "Error: Empty Content"}
            </div>
            '''
        except Exception as e:
            return f"Error connecting to <b>{target_url}</b>. <a href='/'>Try again</a>"

    return '''
    <div style="text-align:center; padding:40px 10px; font-family:sans-serif;">
        <h2 style="color:#d32f2f;">Smart <span style="color:#333;">JioProxy</span></h2>
        <p style="font-size:12px; color:#666;">Enter any site name (AI will fix it)</p>
        <form action="/" method="GET">
            <input type="text" name="url" placeholder="facebook or y2mate.is" 
                   style="width:90%; padding:15px; border:2px solid #d32f2f; border-radius:10px;">
            <br><br>
            <button type="submit" style="width:95%; padding:15px; background:#d32f2f; color:white; border:none; border-radius:10px; font-weight:bold;">
                OPEN SECURELY
            </button>
        </form>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
