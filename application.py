from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "helloosp"

DB = DBhandler()

@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('view_list'))

@application.route("/home")
def view_list():
    per_page = 6
    per_row = 3
    row_count = int(per_page / per_row)

    data = DB.get_products()
    # product_key = next(iter(data))
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "index.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        total=tot_count)


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
    data = request.form
    pw = request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("join.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
