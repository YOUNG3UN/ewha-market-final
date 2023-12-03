from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
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
    return render_template('product_detail.html', key=key, product=product)

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
        sellerID = request.args.get('writerID')
        category = request.args.get('category')
        return render_template("review_reg.html", category=category, sellerID=sellerID)
    elif request.method == 'POST':
        image_file = request.files["file"]
        image_file.save("static/image/{}".format(image_file.filename))
        data = request.form

        DB.insert_review(data, image_file.filename)
        
        return redirect(url_for('view_review'))

@application.route('/review/<key>')
def review_detail(key):
    review = DB.get_review_byname(str(key))
    return render_template("review_detail.html", review=review)

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

@application.route('/show_heart/<key>/', methods=['GET'])
def show_heart(key):
    my_heart = DB.get_heart_byname(session['id'],key)
    return jsonify({'my_heart': my_heart})
 
@application.route('/like/<key>/', methods=['POST'])
def like(key):
    my_heart = DB.update_heart(session['id'],'Y',key)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<key>/', methods=['POST'])
def unlike(key):
    my_heart = DB.update_heart(session['id'],'N',key)
    return jsonify({'msg': '좋아요 취소!'})

@application.route("/mp_wishlist", methods=['GET'])
def wish_list():
    page = request.args.get("page", 0, type=int)
    per_page = 6 # 페이지당 상품 개수
    start_idx = per_page * page
    end_idx = per_page * (page + 1)
    products = DB.get_wishlist_items(session.get('id', ''))
    item_counts = len(products)
    products = products[start_idx:end_idx]

    print("Retrieved wishlist items:", products)

    return render_template(
    "mp_wishlist.html",
    products = products,
    limit=per_page,
    page=page,
    page_count=int((item_counts / per_page) + 1),
    total=item_counts
)

@application.route("/mp_product_a")
def my_product_a():
    if 'id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
    print(session['id'])
    writer_id = session['id']
    my_products = DB.get_my_products(writer_id) 
    print("..................................................")
    return render_template("mp_product.html", my_products=my_products)

#     print("Retrieved wishlist items:", products)

    return render_template(
    "mp_wishlist.html",
    products = products,
    limit=per_page,
    page=page,
    page_count=int((item_counts / per_page) + 1),
    total=item_counts
)

@application.route("/mp_review", methods=['GET'])
def mp_review():
     page = request.args.get("page", 0, type=int)
     per_page = 6 # 페이지당 상품 개수
     start_idx = per_page * page
     end_idx = per_page * (page + 1)
     products = DB.get_myreview_items(session.get('id', ''))
     item_counts = len(products)
     products = products[start_idx:end_idx]

     print("Retrieved wishlist items:", products)

     return render_template(
     "mp_review.html",
     products = products,
     limit=per_page,
     page=page,
     page_count=int((item_counts / per_page) + 1),
     total=item_counts
 )


@application.route("/find_pw")
def find_pw():
    return render_template("find_pw.html")

@application.route("/find_password", methods=['POST'])
def find_password():
    id_ = request.form['id']
    email_ = request.form['email']

    if DB.check_user(id_, email_):
        return render_template("find_pw.html", id=id_)
    else:
        flash("아이디와 이메일이 일치하지 않습니다. 다시 입력해주세요!")
        return render_template("find_pw.html")

@application.route("/reset_password/<user_id>", methods=["POST"])
def reset_password(user_id):
    pw = request.form['pw']
    confirm_pw = request.form['confirm_pw']

    if pw == confirm_pw:
        pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
        DB.change_password(user_id, pw_hash)
        flash("[비밀번호 변경 완료] 변경된 비밀번호로 로그인 해주세요!")
        return redirect(url_for('login'))
    else:
        flash("비밀번호가 일치하지 않습니다. 다시 입력해주세요!")
        return render_template("find_pw.html", id=user_id)


if __name__ == "__main__":
    application.run(host='0.0.0.0')
