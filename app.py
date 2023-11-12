from flask import Flask, render_template, request, redirect, url_for
import sys
from database import DBhandler

application = Flask(__name__)

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

if __name__ == "__main__":
    application.run(host='0.0.0.0')
    
    