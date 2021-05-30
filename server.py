import subprocess
import webbrowser

from flask import Flask, request

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/')



def exec_command(voice):
    chunks = voice.split()

    if len(chunks) <= 2 or chunks[0].lower() != "linux":
        return None
    
    switcher = {
        "open": "browser",
        "file": "touch",
        "directory": "mkdir",
    }

    cmd =  switcher.get(chunks[1].lower())

    payload = chunks[2].lower()

    if cmd == "browser":
        pages = {
            "facebook":"https://www.facebook.com",
            "twitter":"https://www.twitter.com",
            "instagram":"https://www.instagram.com",
            "google":"https://www.google.com",
        }
        page = pages.get(payload,"https://www.google.com")
        print(page)
        return webbrowser.open_new_tab(page)


    return subprocess.call([cmd,payload])



@app.route('/recognition',methods=["POST"])
def root():
    data = request.get_json()
    res = exec_command(data["voice"])
    if res == None: 
        return {"message":"Cannot understand the command sorry."}
    
    return {"message":"command executed"}


if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
    print("Connection Stablish")
    print(f"Listen traffic through http://localhost:{4000}")

