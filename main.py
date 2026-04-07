from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# Desktop User-Agent taaki y2mate ko lage ki computer se request aa rahi hai
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

@app.route('/')
def home():
    target_url = request.args.get('url', '')
    
    # Agar user ne kuch search nahi kiya toh Home Page dikhao
    if not target_url:
        return '''
        <div style="background:#f00; color:#fff; padding:20px; text-align:center; font-family:sans-serif;">
            <h1>JioBharat Video Downloader</h1>
            <form action="/" method="get">
                <input type="text" name="url" placeholder="Video URL ya Site likhein..." style="width:80%; padding:10px;">
                <br><br>
                <button type="submit" style="padding:10px 20px; background:#000; color:#fff; border:none;">GO / CONVERT</button>
            </form>
        </div>
        '''

    if not target_url.startswith('http'):
        target_url = "https://" + target_url

    try:
        # Step 1: Site ko fetch karna
        res = requests.get(target_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Step 2: Live Conversion logic (Ads hatana aur Buttons nikaalna)
        # Hum saari Scripts ko allow karenge lekin Ads ko block karenge
        for s in soup.find_all("script"):
            if "google" in str(s) or "ads" in str(s) or "pop" in str(s):
                s.decompose()

        # Step 3: Page ko "Jio-Ready" (Compress) karna
        # Hum sirf Main Content area ko rakhenge
        content = soup.find('body')
        
        final_html = f"""
        <div style="background:#222; padding:10px; text-align:center;">
            <a href="/" style="color:#fff; text-decoration:none;">[ Home ]</a>
            <span style="color:#0f0;"> | Site: {target_url[:20]}...</span>
        </div>
        <div style="padding:10px; font-size:14px; background:#fff;">
            {content.decode_contents() if content else "Page Load Nahi Hua"}
        </div>
        """
        return render_template_string(final_html)

    except Exception as e:
        return f"Error: Site busy hai ya khul nahi rahi. ({str(e)})"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
