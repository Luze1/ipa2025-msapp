from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from bson import ObjectId
from pymongo import MongoClient

sample = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
mydb = client["ipa2025"]
myint = mydb["interface_status"]
myrouter = mydb["routers"]

@sample.route("/")
def main():
    data = []
    for x in myrouter.find():
        data.append(x)
    return render_template("index.html", data=data)

@sample.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        mydict  = ({"ip" : ip, "username" : username, "password" : password})
        myrouter.insert_one(mydict)
    return redirect(url_for("main"))

@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        query = {'_id': ObjectId(idx)}
        myrouter.delete_one(query)
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)