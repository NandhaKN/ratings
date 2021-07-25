from flask import Flask
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from models import product as Product
# from marshmallow_sqlalchemy import ModelSchema
# from marshmallow import fields

application = Flask(__name__)
password = "Nan@1510"
application.config['SQLALCHEMY_DATABASE_URI']=f'mysql+pymysql://root:nandha10@127.0.0.1:3306/rating'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'jose'
application.config['DEBUG'] = True


@application.route('/product', methods=['POST'])
def createProduct():

    # fetch name and rate from the request
    rate = request.get_json()["rate"]
    name = request.get_json()["name"]
    id = request.get_json()["id"]

    product = Product(rate=rate, name=name, id= id) #prepare query statement

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
    from db import db
    db.init_app(application)

    if application.config['DEBUG']:
        @application.before_first_request
        def create_tables():
            db.create_all()

    application.run()