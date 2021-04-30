from flask import Blueprint
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
import json
from models import ClothesSizes
from models import ClothesItem
from models import User
from models import PaymentMethod
from models import Purchase
from models import Coupon
from models import SoldClothes
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import current_user
from datetime import datetime
from app import db

cart = Blueprint('cart', __name__, template_folder='templates', static_folder='static')

@cart.route('/')
def show_cart():
    return render_template('cart/cart.html')

@cart.route('/order', methods=["POST"])
def order():
    req = json.loads(request.form['cartData'])
    res = {}
    for item in req:
        item_quantity = ClothesSizes.query.filter(ClothesSizes.id==req[item]['sizeId']).first().count
        if item_quantity < int(req[item]['inCart']):
            res[item] = f'Максимальное количество для этого товара: {item_quantity}'
    if res:
        return render_template('cart/cart.html', data=json.dumps(res))
    if current_user.is_authenticated:
        return redirect(url_for('cart.order_submit'))
    else:
        return redirect(url_for('cart.checkout'))

@cart.route('/order_submit')
def order_submit():
    user = User.query.filter(User.id==current_user.get_id()).first()
    payment_methods = PaymentMethod.query.all()
    return render_template('cart/order_submit.html', user_info=user, payment_methods=payment_methods)

@cart.route('/order/checkout')
def checkout():
    return render_template('cart/checkout.html')

@cart.route('/check_discount_code', methods=["POST"])
def check_discount_code():
    req = request.get_json()
    coupon = Coupon.query.filter(Coupon.coupon_code==req).first()
    if coupon and coupon.coupon_is_active:
        res = {'coupon_id': coupon.id, 'coupon_discount': coupon.coupon_discount}
    else:
        res = {'error': 'Скидочный код недействителен'}
    return make_response(jsonify(res), 200)

@cart.route('/create_purchase', methods=["POST"])
def create_purchase():
    req = request.get_json()
    purchase_date = datetime.now()
    purchase_address = req['address']
    purchase_payment_method_id = req['paymentMethod']
    purchase_user_id = current_user.get_id()
    total_cost = 0
    total_discount = 0
    purchase_discounts = req['discounts']

    for item in req['cart']:
        clothes_incart_item = req['cart'][item]
        clothes_item_size = ClothesSizes.query.get(clothes_incart_item['sizeId'])
        clothes_incart_quantity = clothes_incart_item['inCart']
        clothes_price = ClothesItem.query.get(clothes_incart_item['id']).clothes_price
        total_cost += clothes_price * clothes_incart_quantity
        quantity_errors = 0
        if clothes_item_size.count < clothes_incart_quantity:
            quantity_errors += 1
    if quantity_errors:
        resp = make_response()
        resp.headers['redirect'] = '/cart'
        return resp
    
    for discount in purchase_discounts:
        discount_value = Coupon.query.get(discount).coupon_discount
        total_discount += discount_value

    total_cost = total_cost - (total_cost / 100 * total_discount)

    purchase = Purchase(purchase_date=purchase_date, 
                        purchase_cost=total_cost,
                        purchase_discount=total_discount,
                        purchase_address=purchase_address,
                        purchase_payment_method_id=purchase_payment_method_id,
                        purchase_user_id=purchase_user_id
    )
    db.session.add(purchase)
    db.session.commit()

    for item in req['cart']:
        clothes_incart_item = req['cart'][item]
        clothes_item_size = ClothesSizes.query.get(clothes_incart_item['sizeId'])
        clothes_incart_quantity = clothes_incart_item['inCart']
        sold_clothes_item = SoldClothes(sold_clothes_quantity=clothes_incart_quantity,
                                        sold_clothes_size_id=clothes_incart_item['sizeId'],
                                        sold_clothes_purchase_id=purchase.id
        )
        db.session.add(sold_clothes_item)
        db.session.commit()
    
    return make_response(jsonify(req), 200)

@cart.route('/thanks')
def thanks():
    return render_template('cart/thanks.html')