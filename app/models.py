import hashlib

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as MyEnum


class UserRoleEnum(MyEnum):
    SHOPPER = "SHOPPER"
    SHOP = "SHOP"


class Base1(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Base2(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(Base1, UserMixin):
    __tablename__ = 'user'
    __abstract__ = True
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    date_of_birth = Column(DateTime, default=datetime.now())
    email = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://media.dolenglish.vn/PUBLIC/MEDIA/9590ffca-47b8-43ef-98a7-742ca207ca23.jpg')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.SHOPPER)


class Seller(User):
    __tablename__ = 'seller'
    products = relationship('Product', backref='seller', lazy=True)


class Customer(User):
    __tablename__ = 'customer'
    reviews = relationship('Review', backref='customer', lazy=True)
    orders = relationship('Order', backref='customer', lazy=True)

    def __str__(self):
        return self.last_name + ' ' + self.first_name


class Category(Base2):
    __tablename__ = "category"
    products = relationship('Product', backref='category', lazy=True)


class Product(Base2):
    __tablename__ = "product"
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    seller_id = Column(Integer, ForeignKey(Seller.id), nullable=False)
    order_details = relationship('OrderDetail', backref='product', lazy=True)
    reviews = relationship('Review', backref='product', lazy=True)


class Order(Base1):
    paid = Column(Boolean, default=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    details = relationship('OrderDetail', backref='Order', lazy=True)


class OrderDetail(Base1):
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    quantity = Column(Integer, default=1)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    is_review = Column(Boolean, default=False)



class Review(Base1):
    __tablename__ = 'review'
    review = Column(String(100), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    create_at = Column(DateTime, default=datetime.now())


# class Reply(Review):
#     __tablename__ = 'reply'
#     reply_to = Column(Integer, ForeignKey(Review.id), default=0)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # customer3 = Customer(last_name='Nghia', first_name='Nguyen Trong', email='nghia@gmail.com',
        #                      phone='0223456789', username='nghia',
        #                      password=str(hashlib.md5('nghia'.encode('utf-8')).hexdigest()),
        #                      user_role=UserRoleEnum.SHOPPER)
        review1 = Review(product_id=1, customer_id=1, review="Sản phẩm này tốt quá")
        review2 = Review(product_id=1, customer_id=2, review="Sản phẩm tệ quá")
        db.session.add_all([review1, review2])
        db.session.commit()

        # seller1 = Seller(last_name='Nguyen', first_name='Van Canh', email='canh@gmail.com', phone='0123456788',
        #                  username='canh', password=str(hashlib.md5('canh'.encode('utf-8')).hexdigest()),
        #                  user_role=UserRoleEnum.SHOP)
        # product1 = Product(name='Iphone 15 Pro Max', description='Designed by Apple', price=20000000,
        #                    image='https://cdn.viettelstore.vn/Images/Product/ProductImage/1349547788.jpeg',
        #                    category_id=2, seller_id=1)
        # product2 = Product(name='Ipad gen 9', description='Designed by Apple', price=7000000,
        #                    image='https://fptshop.com.vn/Uploads/Originals/2022/12/6/638059452164293984_ipad-gen-9-wifi-4g-dd.jpg',
        #                    category_id=3, seller_id=1)
        # db.session.add_all([product1, product2, customer1, seller1])

        # db.session.add_all([review1, review2])
