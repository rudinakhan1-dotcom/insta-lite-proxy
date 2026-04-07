from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

@app.route('/')
def home():
    target_url = request.args.get('url', '')
    
    if not target_url:
        return '''
        <div style="background:#111; color:#fff; padding:20px; text-align:center; font-family:sans-serif;">
            <h2>JioBharat Lite Proxy (15s Deep Scan)</h2>
            <p>Paste Link & Wait for Conversion...</p>
            <form action="/" method="get">
                <input type="text" name="url" placeholder="https://..." style="width:85%; padding:12px; border:1px solid #444;">
                <br><br>
                <button type="submit" style="padding:15px 30px; background:#28a745; color:white; border:none; font-weight:bold; border-radius:5px;">START CONVERSION</button>
            </form>
        </div>
        '''

    if not target_url.startswith('http'):
        target_url = "https://" + target_url

    try:
        # Step 1: Initial Request
        session = requests.Session()
        res = session.get(target_url, headers=HEADERS, timeout=30)
        
        # Step 2: 15 SECONDS WAIT (Deep Scan Mode)
        # Itne waqt mein y2mate piche se conversion buttons generate kar lega
        time.sleep(15) 
        
        # Step 3: Extracting Final Data
        soup = BeautifulSoup(res.text, 'html.parser')

        # Heavy scripts aur ads ko delete karna
        for s in soup(["script", "style", "iframe", "ins"]):
            s.decompose()

        # Saare Links ko clickable aur "Lite" banana
        for a in soup.find_all('a', href=True):
            a['style'] = "display:block; color:blue; margin:10px 0; font-weight:bold;"

        content = soup.find('body')
        
        final_ui = f"""
        <div style="background:#007bff; padding:10px; text-align:center; color:white;">
            <b>Conversion Finished (15s Wait Complete)</b>
        </div>
        <div style="padding:15px; background:#fff; font-family:sans-serif;">
            {content.decode_contents() if content else "Page load nahi ho saka. Dobara try karein."}
        </div>
        """
        return render_template_string(final_ui)

    except Exception as e:
        return f"Timeout Error: Site ne response nahi diya. (Error: {str(e)})"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
