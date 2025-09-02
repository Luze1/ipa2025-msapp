import os
from flask import Flask
from flask import request
from flask import render_template
from flask import render_template_string
from flask import redirect
from flask import url_for
from bson import ObjectId
from pymongo import MongoClient

sample = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
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
        mydict = {"ip": ip, "username": username, "password": password}
        myrouter.insert_one(mydict)
    return redirect(url_for("main"))


@sample.route("/router/<ip>")
def handle_ip(ip):
    routers = list(myint.find({"router_ip": ip}).sort("timestamp", -1).limit(3))
    html = """
    <html>
    <head>
        <title>Router: {{ ip }}</title>
        <style>
            table { border-collapse: collapse; width: 80%; background: #e6f0fa; }
            th, td { border: 1px solid #333; padding: 8px; text-align: left; }
            th { background: #b3c6e6; }
        </style>
    </head>
    <body>
        <h2>Router: {{ ip }}</h2>
        {% for router in routers %}
        <table>
            <tr>
                <th>Timestamp</th>
                <th>Interface</th>
                <th>IP Address</th>
                <th>Status</th>
                <th>Protocol</th>
            </tr>
            {% for intf in router.interfaces %}
            <tr>
                <td>{{ router.timestamp }}</td>
                <td>{{ intf.intf }}</td>
                <td>{{ intf.ipaddr }}</td>
                <td>{{ intf.status }}</td>
                <td>{{ intf.proto }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, ip=ip, routers=routers)


@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = request.form.get("idx")
        query = {"_id": ObjectId(idx)}
        myrouter.delete_one(query)
    except Exception:
        pass
    return redirect(url_for("main"))


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=8080)
