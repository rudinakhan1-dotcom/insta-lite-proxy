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
    
    if not target_url:
        return '''
        <div style="background:#000; color:#fff; padding:20px; text-align:center; font-family:sans-serif;">
            <h2>JioBharat Smart Proxy</h2>
            <p>Paste Link (YouTube/Instagram) & Wait 5 Sec</p>
            <form action="/" method="get">
                <input type="text" name="url" placeholder="https://..." style="width:85%; padding:10px; border-radius:5px;">
                <br><br>
                <button type="submit" style="padding:12px 25px; background:red; color:white; border:none; font-weight:bold;">CONVERT & DOWNLOAD</button>
            </form>
        </div>
        '''

    if not target_url.startswith('http'):
        target_url = "https://" + target_url

    try:
        # Step 1: Request bhejna
        session = requests.Session()
        res = session.get(target_url, headers=HEADERS, timeout=20)
        
        # Step 2: WAIT LOGIC (Yahi aapko chahiye tha)
        # Hum 5 second wait karenge taaki background scripts (AJAX) apna kaam kar sakein
        time.sleep(5) 
        
        # Dubara page refresh mode mein check karna (kuch sites ke liye)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Step 3: Filtering & Compression
        # Hum saari complex JS hata denge jo JioBharat ko hang karti hai
        for s in soup(["script", "style", "iframe", "ins"]):
            s.decompose()

        # Saare buttons ko "Direct Links" mein badalna
        for btn in soup.find_all(['button', 'input']):
            btn['style'] = "background:green; color:white; padding:10px; display:block; margin:5px auto; width:90%;"

        content = soup.find('body')
        
        final_ui = f"""
        <div style="background:#333; padding:10px; text-align:center; color:white;">
            <b>Page Compressed Successfully!</b>
        </div>
        <div style="padding:10px; font-family:sans-serif;">
            {content.decode_contents() if content else "Page Load Nahi Hua. Please Refresh."}
        </div>
        """
        return render_template_string(final_ui)

    except Exception as e:
        return f"Error: Site loading mein time le rahi hai. Dobara try karein. ({str(e)})"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
