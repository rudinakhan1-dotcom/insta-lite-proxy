from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {"User-Agent": "Mozilla/5.0 (NokiaS40; AppleWebkit/534.13) Gecko/20110303"}

@app.route('/')
def home():
    # User agar koi URL search kare toh wo 'url' parameter mein aayega
    target_url = request.args.get('url', 'https://www.google.com')
    
    if not target_url.startswith('http'):
        target_url = "https://" + target_url

    try:
        res = requests.get(target_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Clean-up: Heavy files hatana
        for s in soup(["script", "style", "video"]):
            s.decompose()

        # Simple Search Bar Design (JioBharat ke liye optimized)
        search_html = f"""
        <div style="background:#222; padding:10px; color:white; text-align:center;">
            <form action="/" method="get">
                <input type="text" name="url" placeholder="Site ka naam likhein (e.g. instagram.com)" style="width:70%; padding:5px;">
                <button type="submit" style="padding:5px;">GO</button>
            </form>
            <div style="margin-top:5px; font-size:12px;">
                Quick: <a href="/?url=instagram.com" style="color:yellow;">Insta</a> | 
                <a href="/?url=facebook.com" style="color:yellow;">FB</a> | 
                <a href="/?url=google.com" style="color:yellow;">Google</a>
            </div>
        </div>
        <hr>
        <div style="padding:10px; font-family:sans-serif;">
            {soup.body.decode_contents() if soup.body else "Page load nahi ho saka."}
        </div>
        """
        return render_template_string(search_html)
    except Exception as e:
        return f"Error: Site khul nahi rahi. Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
