from flask import Flask, render_template, request, redirect, session , url_for
import os
import sqlite3
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

UPLOAD_FOLDER = 'static/img'
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
    return redirect("/oyakabuadd")

@app.route("/kouhaiadd")
def kouhaiadd():
    conn = sqlite3.connect("OyaKabu.db")
    c = conn.cursor()
    c.execute("select tgid,image from oyakabu where sex = 0")
    OkabuIds = []
    for row in c.fetchall():
        OkabuIds.append({"tgid":row[0], "image":row[1]})
    c.execute("select tgid,image from oyakabu where sex = 1")
    MekabuIds = []
    for row in c.fetchall():
        MekabuIds.append({"tgid":row[0], "image":row[1]})
    conn.close()
    print(OkabuIds,MekabuIds)
    return render_template("kouhai-add.html", MekabuIds = MekabuIds , OkabuIds = OkabuIds)

@app.route("/kouhaiupload", methods=['POST'])
def kouhaiupload():
    OkabuId = request.form.get("OkabuId")
    MekabuId = request.form.get("MekabuId")
    remarks = request.form.get("remarks")
    KokabuId = OkabuId + "-" + MekabuId
    date = datetime.date.today()
    conn = sqlite3.connect("OyaKabu.db")
    c = conn.cursor()
    c.execute("insert into kouhai values(null,?,?,?,?,?)",(OkabuId,MekabuId,date,remarks,KokabuId))
    conn.commit()
    c.close()
    return redirect("/kouhaiadd")


@app.route("/kouhaikokabuadd")
def kouhaikokabuadd():
    KokabuId = request.args.get("KokabuId")
    print(KokabuId)
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("select OkabuId,MekabuId from kouhai where KokabuId = ?",(KokabuId,))
    OyakabuIds = c.fetchone()
    if OyakabuIds:  # 結果がある場合のみ処理
        OkabuId, MekabuId = OyakabuIds  # 結果から2つの値を展開
        print(OkabuId, MekabuId)
    else:
        return redirect("/")
    
    c.execute("select image from oyakabu where tgid = ?", (OkabuId,))
    OkabuImage = c.fetchone()
    if OkabuImage:  # 結果がある場合のみ処理
        (OkabuImage,) = OkabuImage  # タプルから値を抽出
    c.execute("select image from oyakabu where tgid = ?", (MekabuId,))
    MekabuImage = c.fetchone()
    if MekabuImage:  # 結果がある場合のみ処理
        (MekabuImage,) = MekabuImage  # タプルから値を抽出
    c.close()
    print(OkabuImage,MekabuImage)
    return render_template("kouhai-kokabu-add.html", OkabuId = OkabuId, MekabuId = MekabuId, OkabuImage = OkabuImage, MekabuImage = MekabuImage, KokabuId = KokabuId)

@app.route('/kokabuupload', methods=['POST'])
def KokabuUpload():
    if 'image' not in request.files:
        return redirect("/kouhaikokabuadd")
    
    file = request.files['image']

    if file.filename == '':
        return redirect("/kouhaikokabuadd")
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        KokabuId = request.form.get("KokabuId")
        color = request.form.get("color")
        pattern = request.form.get("pattern")
        blooming = request.form.get("blooming")
        shape = request.form.get("shape")
        remarks = request.form.get("remarks")
        date = datetime.date.today()
        print(color,pattern,blooming,shape,remarks)
        conn = sqlite3.connect("OyaKabu.db")
        c = conn.cursor()
        c.execute("insert into kokabu values(null,?,?,?,?,?,?,?,?)",(KokabuId,color,pattern,blooming,shape,date,filename,remarks))
        conn.commit()
        c.close()
    return redirect(f"/kouhaikokabuadd?KokabuId={KokabuId}")

@app.route("/syousai")
def syousai():
    return render_template("syousai.html")

@app.route("/yearlist")
def yearlist():
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("select distinct substr(date, 1, 4) from kouhai order by substr(date, 1, 4)")
    years = [row[0] for row in c.fetchall()]
    c.close()
    return render_template("year-list.html", years = years)

@app.route("/yearlist/datelist/<year>")
def datelist(year):
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("SELECT DISTINCT substr(date, 6) FROM kouhai WHERE substr(date, 1, 4) = ? ORDER BY substr(date, 6)", (year,))
    dates = [row[0] for row in c.fetchall()]
    c.close()
    return render_template("date-list.html", dates=dates, year = year)

@app.route("/yearlist/datelist/<year>/<date>")
def kouhailist(year, date):
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("SELECT * FROM kouhai WHERE substr(date, 1, 10) = ?", (f"{year}-{date}",))
    breeding_infos = c.fetchall()
    print(breeding_infos)
    
    # OkabuId と MekabuId の取得
    OkabuIds = [info[1] for info in breeding_infos]  # OkabuId のリスト
    MekabuIds = [info[2] for info in breeding_infos]  # MekabuId のリスト
    KokabuIds = [info[5] for info in breeding_infos]  # KokabuId のリスト
    
    # 画像の取得
    OkabuImages = [get_image_from_oyakabutable(OkabuId) for OkabuId in OkabuIds]
    MekabuImages = [get_image_from_oyakabutable(MekabuId) for MekabuId in MekabuIds]
    KokabuImages = [get_image_from_kokabutable(KokabuId) for KokabuId in KokabuIds]

    c.close()
    
    return render_template("kouhai-list.html", breeding_infos=breeding_infos, date=date, year=year, OkabuImages=OkabuImages, MekabuImages=MekabuImages, KokabuImages=KokabuImages)

def get_image_from_oyakabutable(image_id):
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("SELECT image FROM oyakabu WHERE tgid = ?", (image_id,))
    result = c.fetchone()
    c.close()
    return result[0] if result else None

def get_image_from_kokabutable(image_id):
    conn = sqlite3.connect("Oyakabu.db")
    c = conn.cursor()
    c.execute("SELECT image FROM kokabu WHERE KokabuId = ?", (image_id,))
    result = c.fetchone()
    c.close()
    return result[0] if result else None

if __name__ == "__main__":
    app.run(port=8888, debug=False)