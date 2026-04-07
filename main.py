from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

@app.route('/')
def home():
    target_url = request.args.get('url', 'https://www.google.com')
    if not target_url.startswith('http'):
        target_url = "https://" + target_url

    try:
        # y2mate ya kisi bhi site ko fetch karna
        res = requests.get(target_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Conversion buttons ke liye zaroori scripts ko rehne dena
        # Sirf Ads aur Tracker scripts ko hatana
        for s in soup.find_all("script"):
            if "ads" in str(s) or "analytics" in str(s):
                s.decompose()

        # Relative links ko absolute banana taaki buttons kaam karein
        for a in soup.find_all('a', href=True):
            if a['href'].startswith('/'):
                a['href'] = target_url.rstrip('/') + a['href']

        search_ui = f"""
        <div style="background:#000; padding:10px; color:#fff; text-align:center;">
            <form action="/" method="get">
                <input type="text" name="url" placeholder="Paste URL or Site" style="width:65%;">
                <button type="submit">GO</button>
            </form>
        </div>
        <div id="proxy-content" style="padding:5px;">
            {soup.body.decode_contents() if soup.body else "Loading..."}
        </div>
        """
        return render_template_string(search_ui)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
