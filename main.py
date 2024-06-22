from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap4
from forms import Item_Entry_form, Login_form, Registration_form
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
import json
import os

app = Flask(__name__)
Bootstrap4(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
csrf = CSRFProtect()
csrf.init_app(app)
CKEditor(app)

# TODO: Connect to DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy()
db.init_app(app)
# TODO: Configure Flask-Login

login_manager = LoginManager()
login_manager.init_app(app)

# TODO: decorator for loading user
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# USer Table

class User(UserMixin, db.Model):
    __tablename__ = "parent_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True)
    items = relationship("Item_list", back_populates="author")

class Item_list(db.Model):
    __tablename__ = "item_list"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("parent_table.id"))
    item_title = db.Column(db.String(100))
    date = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(500))
    author = relationship("User", back_populates="items")

    # def __init__(self, content):
    #     self.content = json.dumps(content)

    def get_content(self):
        return json.loads(self.content)


# class Show_items(db.Model):
#     __tablename__ = "show_me"
#     item_list = db.Column(db.String(250))
#     item_author = relationship("Item_list", back_populates="all_items")
#     parant_item = relationship("User", back_populates="all_items")

with app.app_context():
    db.create_all()

@app.route("/")
def login_page():
    form = Login_form()
    return render_template("login.html", my_form=form)

@login_required
@app.route("/home_page", methods=["GET", "POST"])
def home():
    all_todo = db.session.query(Item_list).all()
    if request.method == "POST":
        form = request.form
        value = {"members": form.get("radioButtonValue").split(",")}
        value_json = json.dumps(value)
        if current_user.is_authenticated:
            new_list = Item_list(
                user_id = current_user.id,
                item_title = form.get("title"),
                date = form.get("date"),
                content = value_json,
            )
            db.session.add(new_list)
            db.session.commit()
            return render_template("index.html", item_content = all_todo, current_user=current_user)
    return render_template("index.html", item_content=all_todo, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login_me():
    form = Login_form()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        if not user:
            flash("This email does not exist, plz try agian")
            return redirect(url_for("login_me"))
        elif not check_password_hash(user.password, password):
            flash("Password incorrect, please try again.")
            return redirect(url_for("login_me"))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html", my_form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = Registration_form()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login_me'))
        hash_and_salted_password = generate_password_hash(
            request.form.get("password"),
            method="pbkdf2:sha256",
            salt_length=8
        )
        new_user = User(
            email = request.form.get("email"),
            password=hash_and_salted_password,
            name=request.form.get("name")
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login_me"))
    return render_template("register.html", reg_form=form)

@login_required
@app.route("/show_list/<list_id>", methods=["GET", "POST"])
def show_list(list_id):
    new_list = db.session.execute(db.select(Item_list).where(Item_list.id == list_id)).scalars().all()
    list_content = new_list
    return render_template("show_list.html", content_list=list_content)

@login_required
@app.route("/create_new", methods=["GET", "POST"])
def create_new():
    form = Item_Entry_form()
    current_date = datetime.now()
    today = current_date.strftime("%d-%m-%Y")
    return render_template("Create_new.html", new_form=form, today=today)

@login_required
@app.route("/update", methods=["GET", "POST"])
def update_me():
    if request.method == "POST":
        data = request.get_json()
        title = data.get("title")
        item = Item_list.query.filter_by(item_title=title).first()
        new_content = data.get("radioButtonValue")
        if item:
            item.content = new_content
            db.session.commit()
            print("Updated Successfully")
        else:
            print("Item not found")
        # return redirect(url_for("home"))
    return redirect(url_for("home"))

@app.route("/logout", methods=["GET", "POST"])
def logout_me():
    logout_user()
    return redirect(url_for("login_me"))

@app.route("/delete_card", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        data = request.get_json()
        card_id = data.get("cardId")
        card_to_delete = db.get_or_404(Item_list, card_id)
        db.session.delete(card_to_delete)
        db.session.commit()
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)