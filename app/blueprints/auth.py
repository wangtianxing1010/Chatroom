# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("chat.home"))

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        remember_me = request.form.get('remember', False)

        if remember_me:
            remember_me = True

        user = User.query.filter_by(email=email).first()

        if user is not None:
            if user.password_hash is None:
                flash("please use third party service to log in")
                return redirect(url_for(".login"))

            if user.verify_password(password):
                login_user(user, remember_me)
                return redirect(url_for("chat.home"))
        flash("Invalid credentials")
        return redirect(url_for('.login'))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('auth/login.html')


@auth_bp.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email'].lower()

        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash('This email has been registered.')
            return redirect(url_for('.login'))

        nickname = request.form['nickname']
        password = request.form['password']

        user = User(email=email, nickname=nickname)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('chat.profile'))

    return render_template("auth/register.html")