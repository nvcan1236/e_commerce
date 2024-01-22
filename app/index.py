from app import app, dao
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

from app.models import UserRoleEnum


@app.route('/')
def index():
    kw = request.args.get('kw')
    products = dao.load_product(kw)
    categories = dao.load_category()

    return render_template('home.html', products=products, categories=categories)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

    user_role_enum_values = UserRoleEnum.__members__.values()
    return render_template('user_login.html', user_role_enum_values=user_role_enum_values)


if __name__ == '__main__':
    app.run(debug=True)
