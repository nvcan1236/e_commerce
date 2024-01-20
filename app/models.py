from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from flask_login import UserMixin


class Base1(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Base2(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


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


class User(Base1):
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
        gender = Column(Boolean)
        avatar = Column(String(100),
                        default='https://cdn.tgdd.vn/Files/2016/05/04/824270/tim-hieu-cac-cong-nghe-man-hinh-dien-thoai-5.jpg')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = Category(name='Laptop')
        c2 = Category(name='Smart Phone')
        c3 = Category(name='Tablet')
        db.session.add_all([c1, c2, c3])
        product1 = Product(name='Iphone 15 Pro Max', description='Designed by Apple', price=20000000,
                           image='https://cdn.viettelstore.vn/Images/Product/ProductImage/1349547788.jpeg',
                           category_id=2)
        product2 = Product(name='Ipad gen 9', description='Designed by Apple', price=7000000,
                           image='https://fptshop.com.vn/Uploads/Originals/2022/12/6/638059452164293984_ipad-gen-9-wifi-4g-dd.jpg',
                           category_id=3)
        db.session.add_all([product1, product2])
        db.session.commit()
