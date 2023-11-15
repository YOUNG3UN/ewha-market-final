import pyrebase
import json

class DBhandler:
    def __init__(self ):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
            
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
    
        self.db.child("product").push(product_info)
        
        return True