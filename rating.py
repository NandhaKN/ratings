from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
# from marshmallow_sqlalchemy import ModelSchema
# from marshmallow import fields

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://root:nandha10@127.0.0.1:3306/rating'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'jose'
application.config['DEBUG'] = True

db = SQLAlchemy(application)

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Integer)
    name = db.Column(db.String(100))

    def __init__(self,id,rate,name):
        self.id = id
        self.rate = rate
        self.name = name

    def json(self):
        return {'name': self.name, 'rate': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return '<Products (%s, %s) >' % (self.rate, self.name)

# class Mobile(db.Model):

db.create_all()

@application.route('/product', methods=['POST'])
def createProduct():

    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]
    id = request.get_json()["id"]

    product = Product(rate=rate, name=name, id= id) #prepare query statement
    if Product.find_by_name(name):
        return {'message': "An item with name '{}' already exists.".format(name)}, 400

    curr_session = db.session #open database session
    try:
        curr_session.add(product) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except Exception as e:
        print(e)
        curr_session.rollback()
        curr_session.flush() # for resetting non-commited .add()

    productId = product.id #fetch last inserted id
    data = Product.query.filter_by(id=productId).first() #fetch our inserted product

    # config.read('rating_db.conf')

    result = [data.name, data.rate] #prepare visual data

    return jsonify(message="sucessfully created")

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/hello")
def hi():
    return "Hello Nandha!"

@application.route("/hi")
def hii():
    return "Hello World!"


if __name__ == "__main__":
    application.run()