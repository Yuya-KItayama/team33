from flask import Flask, render_template, request, redirect, session , url_for
import os
import sqlite3
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

UPLOAD_FOLDER = 'FlowerImage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/oyakabuadd")
def oyakabuadd():
    return render_template("oyakabu-add.html")

@app.route('/OyakabuUpload', methods=['POST'])
def OyakabuUpload():
    if 'image' not in request.files:
        return redirect("/oyakabuadd")
    
    file = request.files['image']

    if file.filename == '':
        return redirect("/oyakabuadd")
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        color = request.form.get("color")
        pattern = request.form.get("pattern")
        blooming = request.form.get("blooming")
        shape = request.form.get("shape")
        remarks = request.form.get("remarks")
        tgid = request.form.get("tgid")
        sex = request.form.get("sex")
        date = datetime.date.today()
        print(color,pattern,blooming,shape,remarks,sex)
        conn = sqlite3.connect("OyaKabu.db")
        c = conn.cursor()
        c.execute("insert into oyakabu values(null,?,?,?,?,?,?,?,?,?)",(color,pattern,blooming,shape,date,filename,tgid,remarks,sex))
        conn.commit()
        c.close()
        # ここでデータベースにカテゴリと備考を保存する処理を追加
    
    return redirect("/oyakabuadd")

@app.route("/kouhaiadd")
def kouhaiadd():
    conn = sqlite3.connect("myTask.db")
    c = conn.cursor()
    c.execute("select tg from oyakabu where sex = 0")
    
    return render_template("kouhai-add.html")


@app.route("/kouhaikokabuadd")
def kouhaikokabuadd():
    return render_template("kouhai-kokabu-add.html")

@app.route("/syousai")
def syousai():
    return render_template("syousai.html")

@app.route("/yearlist")
def yearlist():
    return render_template("year-list.html")

@app.route("/yearlist/datelist")
def datalist():
    return render_template("date-list.html")

@app.route("/yearlist/datelist/kouhailist")
def kouhailist():
    return render_template("kouhai-list.html")

if __name__ == "__main__":
    app.run(port=8888, debug=False)