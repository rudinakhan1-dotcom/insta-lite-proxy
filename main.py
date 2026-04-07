from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Ultra-Lite User Agent (Purane phones jaisa behavior)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (NokiaS40; AppleWebkit/534.13) Gecko/20110303"
}

@app.route('/')
def home():
    target_url = "https://www.instagram.com/"
    try:
        # Instagram se data lena
        response = requests.get(target_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Sabhi bhari cheezein (Scripts/Styles) ko delete karna
        for element in soup(["script", "style", "link", "video"]):
            element.decompose()

        # Sirf zaroori text aur links ko bachana
        clean_text = soup.get_text(separator=' ')
        
        # Simple HTML Template jo har browser par chale
        html_output = f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Insta Lite Access</title>
            </head>
            <body style="background-color:#fff; color:#000; font-family:monospace; padding:10px;">
                <h3 style="background:#d62976; color:white; padding:5px;">INSTAGRAM LITE MODE</h3>
                <hr>
                <div style="border:1px solid #000; padding:5px; margin-bottom:10px;">
                    {clean_text[:5000]}...
                </div>
                <hr>
                <p><i>System: Compressed for Low-End Browsers</i></p>
            </body>
        </html>
        """
        return render_template_string(html_output)
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
