from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

# Advanced Mobile Headers (JioBharat ke liye best)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Accept-Language": "hi-IN,hi;q=0.9,en-US;q=0.8,en;q=0.7"
}

@app.route('/')
def home():
    query = request.args.get('q', '')
    url_to_open = request.args.get('url', '')

    # 1. FIXED GOOGLE SEARCH (Using a different endpoint)
    if query:
        # Hum Google ke 'm' (mobile) version ko use karenge jo block kam hota hai
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&adtest=off"
        try:
            res = requests.get(search_url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Sirf kaam ke links nikalna
            results = ""
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and '/url?q=' in href:
                    actual_link = href.split('/url?q=')[1].split('&')[0]
                    title = link.text if link.text else actual_link
                    if "google" not in actual_link: # Google ke internal links hatao
                        results += f'<div style="margin-bottom:15px; border-bottom:1px dotted #ccc; padding:5px;"><a href="/?url={actual_link}" style="color:blue; font-size:16px; text-decoration:none;"><b>{title}</b></a></div>'

            return f'<div style="padding:10px; background:#eee;"><form><input name="q" value="{query}" style="width:70%;"><button>Search</button></form></div><div style="padding:10px;">{results if results else "No results. Search again."}</div>'
        except:
            return "Search temporarily blocked by Google. Try again in 1 min."

    # 2. FIXED INSTA/FB LOGIN (Using Mobile Subdomain)
    if url_to_open:
        # Force Mobile Version for Facebook/Instagram
        if "facebook.com" in url_to_open:
            url_to_open = "https://m.facebook.com"
        if "instagram.com" in url_to_open:
            url_to_open = "https://www.instagram.com/accounts/login/"

        try:
            res = requests.get(url_to_open, headers=HEADERS, timeout=15)
            # Content ko simplify karna
            page_content = res.text.replace('href="/', f'href="/?url={url_to_open.split(".com")[0]}.com/')
            
            return f'<div style="background:#333; color:white; padding:5px;"><a href="/" style="color:yellow;">[ Home ]</a></div>{page_content}'
        except:
            return "Link open nahi ho raha. Site ne block kiya hai."

    # 3. CLEAN HOME PAGE
    return '''
    <div style="text-align:center; padding:20px; font-family:sans-serif;">
        <h2 style="color:red;">Jio Search Engine</h2>
        <form action="/" method="get">
            <input type="text" name="q" placeholder="Search anything..." style="width:85%; padding:10px; border-radius:5px;"><br><br>
            <button type="submit" style="padding:10px 20px; background:blue; color:white; border:none;">Google Search</button>
        </form>
        <hr>
        <div style="margin-top:20px;">
            <a href="/?url=https://m.facebook.com" style="display:block; padding:10px; background:#3b5998; color:white; text-decoration:none; margin:5px; border-radius:5px;">Open Facebook</a>
            <a href="/?url=https://www.instagram.com/accounts/login/" style="display:block; padding:10px; background:#e1306c; color:white; text-decoration:none; margin:5px; border-radius:5px;">Open Instagram</a>
            <a href="/?url=https://y2mate.is" style="display:block; padding:10px; background:green; color:white; text-decoration:none; margin:5px; border-radius:5px;">Video Downloader</a>
        </div>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
