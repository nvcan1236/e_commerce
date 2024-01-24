import hashlib

from app.models import Category, Product, Customer, Seller
from app import db


def get_user_by_id(user_id, role):
    if role == "SHOPPER":
        return Customer.query.get(user_id)
    if role == "SHOP":
        return Seller.query.get(user_id)

def load_category():
    return Category.query.all()


def load_product(kw):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains(kw))

    return products.all()


def get_product_by_id(product_id):
    return Product.query.join(Seller).filter(Product.id == product_id).first()


def authenticate_user(username, password, role):
    if role == 'SHOPPER':
        return Customer.query.filter(Customer.username.__eq__(username),
                                     Customer.password.__eq__(hashlib.md5(password.encode()).hexdigest())).first()
    if role == 'SHOP':
        return Seller.query.filter(Seller.username.__eq__(username),
                                   Seller.password.__eq__(hashlib.md5(password.encode()).hexdigest())).first()
