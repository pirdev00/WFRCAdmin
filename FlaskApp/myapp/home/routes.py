from flask import Blueprint, render_template, request


home_bp = Blueprint('home', __name__, template_folder='templates', url_prefix='/home')
@home_bp.route('/')
def home():
    return render_template('home/index.html')