from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/oyakabuadd")
def oyakabuadd():
    return render_template("oyakabu-add.html")

@app.route("/kouhaiadd")
def kouhaiadd():
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