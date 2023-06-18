from flask import Flask, request
from threading import Thread
import json

app = Flask('')

@app.route('/')
def home():
  return "<b> Welcome to Main Page!</b>"


@app.route('/getInfo')
def setToken():
    username = request.args.get("username")
    data = getInfo(username)
    return json.dumps(data)



def getInfo(username):
    from bs4 import BeautifulSoup
    import requests

    user = {}
    req = requests.get(f"https://t.me/{username}")
    for i in req.iter_content(1000, decode_unicode=True):
        soup = BeautifulSoup(i, "html.parser")
        meta_tags = soup.find_all('meta')

        if len(meta_tags) > 3:
            content = str(meta_tags[3].get('content'))
            if content.startswith("http"):
                user['photo'] = content.strip("\n") if content.strip("\n") != 'https://telegram.org/img/t_logo.png' else None

        if soup.find(class_ = "tgme_page_description"):
            user['bio'] = soup.find(class_ = "tgme_page_description").string if soup.find(class_ = "tgme_page_description").string else None

    return user


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()
keep_alive()






