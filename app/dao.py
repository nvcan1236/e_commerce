import hashlib

from app.models import Category, Product, Customer, Seller, Review, Order
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


def load_review(product_id):
    reviews = db.session.query(Review, Customer).join(Customer, Review.customer_id == Customer.id
                                                      ).filter(Review.product_id == product_id).all()
    return reviews


def save_review(product_id, content, customer_id):
    review = Review(product_id=product_id, review=content, customer_id=customer_id)
    db.session.add(review)
    db.session.commit()
    return review


def get_orders(customer_id):
    orders = Order.query.filter(Order.customer_id == customer_id).all()
    return orders


def get_order(order_id):
    if order_id is not None:
        order = Order.query.get(order_id)
        return order
    else:
        return None


def pay(order_id):
    order = Order.query.get(order_id)
    order.paid = True
    db.session.add(order)
    db.session.commit()
