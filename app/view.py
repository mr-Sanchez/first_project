from app import app
from app import db
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import make_response
from flask import jsonify
from models import User
from models import Purchase
from models import SoldClothes
from models import ClothesSizes
from models import ClothesItem
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = False

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = User.query.filter(User.id==user_id).first()
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        print(self.__user.id)
        return self.__user.id
    


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        if email and password:
            user = User.query.filter(User.user_email==email).first()
            if user and check_password_hash(user.user_password, password):
                userlogin = UserLogin().create(user)
                remember_me = True if request.form.get("rememberMe") else False
                login_user(userlogin, remember=remember_me)
                return redirect(request.args.get('next') or url_for('profile'))
            if not user:
                flash('Пользователь с таким e-mail не зарегистрирован', category='email_errors')
            elif not check_password_hash(user.user_password, password):
                flash('Неверный пароль', category='password_errors')
        if not email:
            flash('Это поле не может быть пустым', category="email_errors")
        if not password:
            flash('Это поле не может быть пустым', category="password_errors")

        return redirect(request.referrer)
    return render_template("login.html")


@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == "POST":
        name = request.form["InputName"]
        email = request.form["InputEmail"]
        password = request.form["InputPassword1"]
        confirm_password = request.form["InputPassword2"]

        if (len(name) > 0 and len(email) > 0
            and len(password) >= 6 
            and password == confirm_password):
            check_user = User.query.filter(User.user_email==email).first()
            if not check_user:
                pass_hash = generate_password_hash(password)
                user = User(user_name=name, user_email=email, user_password=pass_hash)
                if user:
                    db.session.add(user)
                    db.session.commit()
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    flash('Пользователь успешно зарегистрирован', category='success')
                    return redirect(request.args.get('next') or url_for('profile'))
            else:
                flash('Пользователь с таким email уже зарегистрирован', category='danger')
        else:
            flash('Неверно заполнены поля', category='danger')
        return redirect(request.referrer)
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user_info = User.query.filter(User.id==current_user.get_id()).first()
    purchases = Purchase.query.filter(Purchase.purchase_user_id==current_user.get_id()).order_by(Purchase.purchase_date.desc())
    '''response = []
    for purchase in purchases:
        purchase_items = purchase.sizes
        response.append([purchase, purchase_items])'''
    return render_template('profile.html', user_info=user_info, purchases=purchases)

@app.route('/get_user_info')
def get_user_info():
    req = request.get_json()
    user = User.query.filter(User.id==req).first()
    user_name = user.name
    user_email = user.email
    res = make_response(jsonify({'name' : user_name, 'email' : user_email}), 200)
    return res

