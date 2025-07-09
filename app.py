from flask import Flask, render_template, url_for
from pymongo import MongoClient

client=MongoClient("mongodb://localhost:27017/")

db=client.shop

items=db.items
accounts=db.accounts

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/page3")
def page3():
    return render_template("page3.html")

@app.route("/logo")
def logo():
    return render_template("logo.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

