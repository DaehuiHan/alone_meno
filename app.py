from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    # FIXME: GET 1. 받을 데이터는 없고, DB에 저장되어 있는 정보 가져다가 클라이언트한테 넘겨주기
    # sample_receive = request.args.get('sample_give')

    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles':articles})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    # FIXME: POST 1. 받을 데이터 정해주기
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    # FIXME: POST 2. 받은 url 가지고 title, image, desc 크롤링 해오기 (meta_prac.py에서 한것 불러오기)
    # 항상 import 해주는 것 잊지 말기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    # FIXME: POST 3. 가져온 데이터들을 DB에 저장해주기
    # 항상 import 해주는 것 잊지 말기
    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'url':url_receive,
        'comment':comment_receive
    }
    db.articles.insert_one(doc)

    return jsonify({'msg':'저장 완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)