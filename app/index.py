# import login as login
from flask_login import logout_user, login_user, current_user
from app import app, dao, login, utils
from flask import render_template, request, session, redirect, url_for, jsonify
from app.models import *


@app.context_processor
def common_response():
    cart = session.get('cart')
    if cart is None:
        cart = {}
    return {
        'cart_static': utils.count_cart(cart)
    }


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


@app.route('/api/review', methods=['POST'])
def send_review():
    data = request.json
    product_id = data.get('productId')
    content = data.get('content')
    customer_id = data.get('customerId')
    detail_id = data.get('detailId')
    detail = OrderDetail.query.get(detail_id)

    if detail.is_review:
        return jsonify({
            'status-code': 401,
            'message': 'Đã gửi đánh giá!!'
        })

    if dao.save_review(product_id, content, customer_id):
        detail.is_review = True
        db.session.add(detail)
        db.session.commit()

        return jsonify({
            'status-code': 200,
            'message': 'Đã lưu thành công!!'
        })

    return jsonify({
        'status-code': 400,
        'message': 'Lưu không thành công!!'
    })


@app.route('/api/order', methods=['POST'])
def buy():
    data = request.json
    if len(data.values()) >= 1:
        order = Order(customer_id=current_user.id)
        db.session.add(order)
        db.session.commit()

        for d in data.values():
            detail = OrderDetail(order_id=order.id, quantity=d['quantity'], product_id=d['id'])
            db.session.add(detail)

        db.session.commit()

    return jsonify({
        'order-id': order.id,
        'status-code': 200,
        'message': 'Đã lưu thành công!!'
    })


@app.route('/')
def index():
    kw = request.args.get('kw')
    products = dao.load_product(kw)
    categories = dao.load_category()
    if current_user.is_authenticated and current_user.user_role == UserRoleEnum.SHOP:
        return render_template('shop.html', products=products, categories=categories)
    else:
        return render_template('home.html', products=products, categories=categories)


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = dao.get_product_by_id(product_id)
    is_shop = current_user.is_authenticated and current_user.user_role == UserRoleEnum.SHOP
    return render_template('product_detail.html', product=product, is_shop=is_shop)


@app.route('/order')
def order():
    global details
    details = {}
    detail = request.args.get('detail')
    if detail == 'cart':
        details = session.get('cart')
    elif type(int(detail)) is int:
        product = Product.query.get(detail)
        details = {'1': {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': 1
        }}

    total = sum(map(lambda x: (x['quantity'] * x['price']), details.values()))

    return render_template('order.html', details=details, total=total)


@app.route('/history')
def history():
    orders = dao.get_orders(current_user.id)
    review_id = request.args.get('review')
    order_review = dao.get_order(review_id)
    return render_template('history.html', orders=orders, order_review=order_review)


@app.route('/cart')
def cart():
    cart = session.get('cart')
    return render_template('cart.html', cart=cart)


@app.route('/order-result')
def order_result():
    if request.args.get('from') == 'cart' and session.get('cart'):
        del session['cart']
    order_id = request.args.get('order-id')
    print(order_id)
    dao.pay(order_id)

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
