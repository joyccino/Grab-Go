from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()           #SQLAlchemy를 사용해 데이터베이스 저장

class Fcuser(db.Model): 
    __tablename__ = 'customers'   #테이블 이름 : fcuser
    customer_id = db.Column(db.Integer,db.Sequence('customer_seq'), primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    customer_name = db.Column(db.String(120), index=True, unique=True)
    customer_pass = db.Column(db.String(120), index=True, unique=True)
    login_session = db.Column(db.String(120), index=True, unique=True)
    verification = db.Column(db.Integer, index=True, unique=True)

# class Carts(db.Model):
#     __tablename__ = 'carts'
#     cart_id = db.Column(db.Integer,db.Sequence('cart_seq'), primary_key=True)
#     # customer_id = db.Column(db.Integer(64), foreign_key=True)
#     customer_id = db.Column(db.Integer(64), index=True, unique=True)
#     product_id = db.Column(db.Integer(120), index=True, unique=True)
#     cart_stock = db.Column(db.Integer(120), index=True, unique=True)
#     cart_in  = db.Column(db.Date, index=True, unique=True)

class Orders(db.Model):
    __tablename__ = 'orders'
    customer_id = db.Column(db.Integer,db.Sequence('customer_seq'), primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True)
    customer_name = db.Column(db.String(120), index=True, unique=True)
    customer_pass = db.Column(db.String(120), index=True, unique=True)
    login_session = db.Column(db.String(120), index=True, unique=True)
    verification = db.Column(db.Integer, index=True, unique=True)
