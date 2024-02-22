from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return redirect("/index")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=8888, debug=False)