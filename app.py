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

@application.route("/home", methods=['GET'])
def view_list():
    page = request.args.get("page", 0, type=int)
    per_page = 6 # 페이지당 상품 개수
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    products = DB.get_products()
    item_counts = len(products)
    products = dict(list(products.items())[start_idx:end_idx])

    return render_template(
        "index.html",
        products = products.items(),
        limit = per_page,
        page = page,
        page_count = int((item_counts / per_page) + 1),
        total = item_counts)

@application.route('/products/<key>')
def product_detail(key):
    product = DB.get_item_byname(str(key))
    return render_template('product_detail.html', product=product)

@application.route("/products_insert", methods=['POST', 'GET'])
def insert_products():
    if request.method == 'POST':
        image_file = request.files["file"]
        image_file.save("static/image/{}".format(image_file.filename))
        data = request.form

        DB.insert_product(data, image_file.filename)

        return redirect(url_for('hello'))
    return render_template("product_reg.html")

@application.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page = 6 # 페이지당 상품 개수
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    reviews = DB.get_reviews()
    item_counts = len(reviews)
    reviews = dict(list(reviews.items())[start_idx:end_idx])

    return render_template(
        "review.html",
        reviews = reviews.items(),
        limit = per_page,
        page = page,
        page_count = int((item_counts/per_page) + 1),
        total = item_counts)

@application.route("/reg_review", methods=['GET', 'POST'])
def reg_review():
    if request.method == 'GET':
        category = request.args.get('category')
        return render_template("review_reg.html", category=category)
    elif request.method == 'POST':
        image_file = request.files["file"]
        image_file.save("static/image/{}".format(image_file.filename))
        data = request.form

        DB.insert_review(data, image_file.filename)
        
        return redirect(url_for('hello'))

@application.route("/review_detail")
def review_detail():
    return render_template("review_detail.html")

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['password']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        # return render_template("index.html") 
        return redirect(url_for('view_list'))
    else:
        flash("잘못된 아이디/비밀번호 입니다!")
        return render_template("login.html")

@application.route("/logout")
def logout_user():
    session.clear()
    # return render_template("index.html")
    return redirect(url_for('view_list'))

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
        flash("이미 존재하는 아이디입니다!")
        return render_template("join.html")

@application.route("/mp_product")
def mp_product():
    return render_template("mp_product.html")

@application.route("/mp_review")
def mp_review():
    return render_template("mp_review.html")

@application.route("/mp_wishlist")
def mp_wishlist():
    return render_template("mp_wishlist.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')
