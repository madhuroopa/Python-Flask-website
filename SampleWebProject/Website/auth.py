from flask import Blueprint, render_template, \
    request,flash, redirect, url_for
# Blueprint means define that this file is the blueprint of our application
from .models import User,db
from werkzeug.security import   generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!')
                login_user(user,remember=True)
                return redirect(url_for('sampleviews.home'))
            else:
                flash('Incorrect Password, tryagain',category='error')

        else:
            flash("User doesnot exists", category='error')

    return render_template("login.html", user=current_user)
@auth.route('/logout')
@login_required # we cannot access the page unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2=request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category ='error')
        elif(len(email)) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstname) <2:
            flash('Firstname must be greater than 2 characters', category='error')
        elif password1!=password2:
            flash('passwords don\'t match',category='error')
        elif len(password1) < 7:
            flash('Password must be atleast 7 characters', category='error')
        else:
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category='success')
            return redirect(url_for('sampleviews.home'))
    return render_template("signup.html", user=current_user)
