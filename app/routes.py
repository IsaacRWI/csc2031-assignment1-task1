from flask import Blueprint, render_template, request, redirect, url_for
from app.forms import RegistrationForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm
    client_ip = request.remote_addr or "Unknown IP"


    # name = request.form.get('name') if request.method == 'POST' else ''
    # return render_template('register.html', name=name)