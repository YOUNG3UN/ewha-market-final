import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f )
            
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        
    def insert_product(self, data, img_path):
        product_info ={
            "category": data['category'],
            "region": data['region'],
            "price": data['price'],
            "status": data['status'],
            "title": data['title'],
            "content": data['content'],
            "img_path": img_path
        }
    
        # 기본키(new_product_key) index 알아서 생성해서 db에 넣어주기
        new_product_ref = self.db.child("product").push(product_info)
        new_product_key = new_product_ref.key()
        print("New product key:", new_product_key)
        self.db.child("product").child(new_product_key).update(product_info)
        
        return True