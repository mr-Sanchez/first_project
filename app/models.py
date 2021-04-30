from app import db
import re
from sqlalchemy.orm import backref


class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_method_name = db.Column(db.String(100))
    payment_method_caption = db.Column(db.String(100))


class ClothesCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_path = db.Column(db.String(255))
    category_name = db.Column(db.String(255))
    clothes_for = db.Column(db.String(100))
    clothes = db.relationship('ClothesItem', backref='category')


class ClothesItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clothes_name = db.Column(db.String(255))
    clothes_price = db.Column(db.Integer)
    clothes_discount = db.Column(db.Integer)
    clothes_description = db.Column(db.Text)
    clothes_category_id = db.Column(db.Integer, db.ForeignKey('clothes_category.id'))
    images = db.relationship('ClothesItemImage', backref='clothes')
    sizes = db.relationship('ClothesSizes', backref='clothes')


class ClothesItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clothes_image_path = db.Column(db.String(255))
    clothes_id = db.Column(db.Integer, db.ForeignKey('clothes_item.id'))


class ClothesSizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(100))
    count = db.Column(db.Integer)
    clothes_id = db.Column(db.Integer, db.ForeignKey('clothes_item.id'))
    purchases = db.relationship('SoldClothes', backref='size')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255))
    user_email = db.Column(db.String(255), unique=True)
    user_password = db.Column(db.String(255))
    purchases = db.relationship('Purchase', backref='user')


class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coupon_code = db.Column(db.String(20))
    coupon_discount = db.Column(db.Integer)
    coupon_is_added = db.Column(db.Boolean)
    coupon_is_active = db.Column(db.Boolean)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime)
    purchase_cost = db.Column(db.Integer)
    purchase_discount = db.Column(db.Integer)
    purchase_address = db.Column(db.String(255))
    purchase_payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    purchase_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sizes = db.relationship('SoldClothes', backref='purchase')
    

class SoldClothes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sold_clothes_quantity = db.Column(db.Integer)
    sold_clothes_size_id = db.Column(db.Integer, db.ForeignKey('clothes_sizes.id'))
    sold_clothes_size = db.relationship('ClothesSizes', backref=backref('sold', passive_deletes='all'))
    sold_clothes_purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'))
    sold_clothes_purchase = db.relationship('Purchase', backref=backref('sold', passive_deletes='all'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_author = db.Column(db.String(100))
    comment_text = db.Column(db.Text)
    comment_publish_date = db.Column(db.DateTime)
    comment_clothes_id = db.Column(db.Integer, db.ForeignKey('clothes_item.id'))