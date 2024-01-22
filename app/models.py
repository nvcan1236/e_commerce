import hashlib

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float, Enum, MetaData
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as MyEnum

metadata = MetaData()


class UserRoleEnum(MyEnum):
    USER = "SHOPPER"
    SELLER = "SHOP"


class Base1(db.Model):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)


class Base2(db.Model):
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

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
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)


class Seller(User):
    __tablename__ = 'seller'
    products = relationship('Product', backref='seller', lazy=True)


class Customer(User):
    __tablename__ = 'customer'
    reviews = relationship('Review', backref='customer', lazy=True)


class Review(Base1):
    __tablename__ = 'review'
    review = Column(String(100), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name='Laptop')
        # c2 = Category(name='Smart Phone')
        # c3 = Category(name='Tablet')
        # db.session.add_all([c1, c2, c3])
        #
        # customer1 = Customer(last_name='Duong', first_name='Van Khanh', email='duongvan845@gmail.com',
        #                      phone='0123456789', username='khanh',
        #                      password=str(hashlib.md5('khanh'.encode('utf-8')).hexdigest()),
        #                      user_role=UserRoleEnum.USER)
        # seller1 = Seller(last_name='Nguyen', first_name='Van Canh', email='canh@gmail.com', phone='0123456788',
        #                  username='canh', password=str(hashlib.md5('canh'.encode('utf-8')).hexdigest()),
        #                  user_role=UserRoleEnum.SELLER)
        # review1 = Review(review='San pham tot qua', customer_id=1)
        # product1 = Product(name='Iphone 15 Pro Max', description='Designed by Apple', price=20000000,
        #                    image='https://cdn.viettelstore.vn/Images/Product/ProductImage/1349547788.jpeg',
        #                    category_id=2, seller_id=1)
        # product2 = Product(name='Ipad gen 9', description='Designed by Apple', price=7000000,
        #                    image='https://fptshop.com.vn/Uploads/Originals/2022/12/6/638059452164293984_ipad-gen-9-wifi-4g-dd.jpg',
        #                    category_id=3, seller_id=1)
        # db.session.add_all([product1, product2, customer1, seller1, review1])
        # db.session.commit()
