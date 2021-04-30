from flask import Blueprint
from flask import render_template
from flask import session
from flask import jsonify
from flask import request
from flask import make_response
from models import ClothesCategory
from models import ClothesItem
from models import ClothesItemImage
from models import ClothesSizes
from models import Comment
from datetime import datetime
from app import db

clothes = Blueprint('clothes', __name__, template_folder='templates', static_folder='static')

@clothes.route('/<itemsfor>')
def show_categories(itemsfor):
    categories = ClothesCategory.query.filter(ClothesCategory.clothes_for==itemsfor).all()
    return render_template('clothes/show_categories.html', categories=categories)

@clothes.route('/<itemsfor>/<category>')
def show_items_by_category(itemsfor, category):
    items_category = ClothesCategory.query.filter(ClothesCategory.category_path==category, ClothesCategory.clothes_for==itemsfor).first()
    items = ClothesItem.query.filter(ClothesItem.clothes_category_id==items_category.id)
    return render_template('clothes/show_items.html', items=items)

@clothes.route('/item_<item_id>')
def item_detail(item_id):
    item = ClothesItem.query.filter(ClothesItem.id==item_id).first()
    comments = Comment.query.filter(Comment.comment_clothes_id==item_id).all()
    return render_template('clothes/item_detail.html', item=item, comments=comments)


@clothes.route('/check_size_count', methods=["POST"])
def add_item():
    req = request.get_json()
    size = ClothesSizes.query.filter(ClothesSizes.id==req).first()
    size_count = size.count
    size_tag = size.size
    res = make_response(jsonify({'size_count' : size_count, 'size_tag' : size_tag}), 200)
    return res

@clothes.route('/add_comment', methods=["POST"])
def add_comment():
    req = request.get_json()
    clothes_id = int(req['id'].split('_')[1])
    comment_author = req['author']
    comment_text = req['text']
    comment_publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_comment = Comment(comment_author=comment_author,
                        comment_text=comment_text,
                        comment_publish_date=comment_publish_date,
                        comment_clothes_id=clothes_id
    )
    db.session.add(new_comment)
    db.session.commit()
    res = make_response(jsonify({'author' : comment_author, 'text' : comment_text, 'date' : comment_publish_date}), 200)
    return res

