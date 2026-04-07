from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

app = Flask(__name__)

# User-Agent taaki sites ko lage ki hum browser hain
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

@app.route('/')
def home():
    query = request.args.get('q', '')
    url_to_open = request.args.get('url', '')

    # AGAR USER KUCH SEARCH KARE (Google Search Logic)
    if query:
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&hl=hi" # hl=hi se Hindi/English mix aayega
        try:
            res = requests.get(search_url, headers=HEADERS)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Google ke faltu headers hatana
            for s in soup(["script", "style"]): s.decompose()
            
            results = ""
            for g in soup.find_all('div', class_='tF2Cxc') or soup.find_all('div', class_='kCrYT'):
                link = g.find('a')['href']
                title = g.find('h3').text if g.find('h3') else "Link"
                # Proxy ke zariye link kholne ke liye
                results += f'<div style="margin-bottom:15px;"><a href="/?url={link}" style="color:blue; font-size:18px; font-weight:bold;">{title}</a><br><small>{link[:50]}...</small></div>'

            return f"""
            <div style="background:#f2f2f2; padding:10px; border-bottom:2px solid red;">
                <form action="/" method="get">
                    <input type="text" name="q" value="{query}" style="width:70%; padding:8px;">
                    <button type="submit">Search</button>
                </form>
            </div>
            <div style="padding:15px;">{results if results else "No results found. Try again."}</div>
            """
        except:
            return "Search fail ho gaya. Internet check karein."

    # AGAR USER KOI SITE KHOLNA CHAHE (Proxy Logic)
    if url_to_open:
        try:
            # Facebook/Insta ke liye language and session handling
            res = requests.get(url_to_open, headers=HEADERS, timeout=20)
            time.sleep(2) # Chhota wait taaki logo se aage badhe
            
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Instagram/Facebook fix: Heavy JS hatana par links rakhna
            for s in soup(["script", "style", "iframe"]): s.decompose()

            # Sabhi relative links ko hamare proxy link mein badalna
            for a in soup.find_all('a', href=True):
                original = a['href']
                if original.startswith('/'):
                    base = "/".join(url_to_open.split('/')[:3])
                    a['href'] = f"/?url={base}{original}"
                else:
                    a['href'] = f"/?url={original}"

            return f"""
            <div style="background:black; color:white; padding:5px; text-align:center;">
                <a href="/" style="color:yellow;">[ Naya Search ]</a> | Browsing: {url_to_open[:20]}
            </div>
            <div style="padding:10px;">{soup.body.decode_contents() if soup.body else "Content load nahi hua."}</div>
            """
        except:
            return "Site khulne mein problem ho rahi hai."

    # DEFAULT HOME PAGE (Google Look-alike)
    return '''
    <div style="text-align:center; padding-top:50px; font-family: sans-serif;">
        <h1 style="color:red; font-size:40px;">Jio<span style="color:black;">Search</span></h1>
        <form action="/" method="get">
            <input type="text" name="q" placeholder="Kuch bhi search karein..." style="width:80%; padding:15px; border-radius:25px; border:1px solid #ccc;">
            <br><br>
            <button type="submit" style="padding:10px 20px; background:#f8f9fa; border:1px solid #ccc; cursor:pointer;">Google Search</button>
        </form>
        <div style="margin-top:30px;">
            <a href="/?url=https://www.facebook.com" style="margin:10px; text-decoration:none; color:blue;">Facebook</a> |
            <a href="/?url=https://www.instagram.com" style="margin:10px; text-decoration:none; color:purple;">Instagram</a>
        </div>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
