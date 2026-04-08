from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/')
def home():
    url_to_open = request.args.get('url', '')

    # AGAR USER NE URL DAALA HAI (20 Seconds Wait Logic)
    if url_to_open:
        if not url_to_open.startswith('http'):
            url_to_open = 'https://' + url_to_open
            
        return f'''
        <div style="text-align:center; padding-top:50px; font-family:sans-serif;">
            <h2 style="color:#de5833;">Connecting Safely...</h2>
            <p style="font-size:18px;">Please wait for <b>20 seconds</b> while we prepare your page.</p>
            
            <div style="margin:20px auto; width:80%; background:#eee; height:10px; border-radius:5px;">
                <div style="width:0%; background:#de5833; height:10px; border-radius:5px; animation: progress 20s linear forwards;"></div>
            </div>

            <p style="color:#888;">Live conversation processing...</p>

            <style>
                @keyframes progress {{
                    from {{ width: 0%; }}
                    to {{ width: 100%; }}
                }}
            </style>

            <meta http-equiv="refresh" content="20; url={url_to_open}">
        </div>
        '''

    # SIMPLE HOME UI (Sirf URL Address Box)
    return '''
    <div style="text-align:center; padding:40px; font-family:sans-serif; background:#fff; min-height:100vh;">
        <h1 style="color:#333; font-size:30px;">Jio<span style="color:#de5833;">Gateway</span></h1>
        <p style="color:#666;">Enter Website Address to Open</p>
        
        <form action="/" method="get" style="margin-top:30px;">
            <input type="text" name="url" placeholder="example.com" 
                   style="width:85%; padding:15px; border:2px solid #333; border-radius:10px; outline:none; font-size:16px;">
            <br><br>
            <button type="submit" style="width:90%; padding:15px; background:#333; color:white; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">
                OPEN WEBSITE
            </button>
        </form>

        <div style="margin-top:50px; padding:15px; border:1px dashed #ccc; border-radius:10px;">
            <p style="font-size:12px; color:#888;">Note: Every link will take exactly 20 seconds to load for security processing.</p>
        </div>
    </div>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
