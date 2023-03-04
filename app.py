import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    #di bawah adalah kode untuk input foto utama
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)
    
    #di bawah adalah kode untuk input foto profile
    file1 = request.files['file1_give']
    extension = file1.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename1 = f'file1-{mytime}.{extension}'
    save_to1 = f'static/{filename1}'
    file1.save(save_to1)
    
    doc = {
        'file': filename,
        'file1': filename1,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST request complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
