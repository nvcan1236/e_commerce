from app.models import Category, Product, Seller
from app import db


def load_category():
    return Category.query.all()


def load_product(kw):
    products = Product.query
    if kw:
        products = products.filter(Product.name.contains(kw))

    return products.all()


def get_product_by_id(product_id):
    return Product.query.join(Seller).filter(Product.id == product_id).first()
