# import login as login
from flask_login import logout_user, login_user
from app import app, dao, login, utils
from flask import render_template, request, session, redirect, url_for, jsonify
from app.models import UserRoleEnum


@app.route('/api/cart', methods=['POST'])
def add_cart():
    cart = session.get('cart')
    if cart is None:
        cart = {}
    data = request.json
    id = str(data.get("id"))

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
        session['cart'] = cart

    else:
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/')
def index():
    kw = request.args.get('kw')
    products = dao.load_product(kw)
    categories = dao.load_category()

    return render_template('home.html', products=products, categories=categories)

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/order')
def order():
    return render_template('order.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/order-result')
def order_result():
    return render_template('order-result.html')

@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    user_role_enum_values = UserRoleEnum.__members__.values()
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        session['role'] = role
        user = dao.authenticate_user(username=username, password=password, role=role)
        if user:
            login_user(user)
            if user.user_role == UserRoleEnum.SHOP:
                return redirect(url_for('shop'))
            else:
                return redirect(url_for('index'))
    return render_template('user_login.html', user_role_enum_values=user_role_enum_values)


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('index'))


@login.user_loader
def load_user(user_id):
    role = session['role']
    user = dao.get_user_by_id(user_id, role)
    return user


if __name__ == '__main__':
    app.run(debug=True)
