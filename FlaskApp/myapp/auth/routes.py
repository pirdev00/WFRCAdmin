# myapp/auth/routes.py


import re

from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash
from myapp.models import User
from flask_login import login_user

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None:
            message = "User not found"
        else:
            if check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('home.home'))
                
            else:
                message = "Invalid password"

    return render_template('auth/login.html', flash_message=message)