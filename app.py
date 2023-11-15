from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

DB = DBhandler()

@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/products_insert", methods=['POST', 'GET'])
def insert_products():
    if request.method == 'POST':
        image_file = request.files["file"]
        image_file.save("static/image/{}".format(image_file.filename))
        data = request.form
        
        DB.insert_product(data, image_file.filename)

        return redirect(url_for('hello'))
    return render_template("product_reg.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/join")
def join():
    return render_template("join.html")

@application.route("/join_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("join.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    
    