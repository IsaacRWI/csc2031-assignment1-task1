from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import RegistrationForm
from bleach import clean

safe_tags = {"b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"}

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    sanitized_content = None
    if form.validate_on_submit() and form.bio.data:
        bio_content = form.bio.data
        sanitized_content = clean(bio_content, tags=safe_tags, attributes={'a': ['href', 'title']}, strip=True)
        flash("Registratiom Success")
    elif request.method == "POST":
        pass

    # client_ip = request.remote_addr or "Unknown IP"


    # name = request.form.get('name') if request.method == 'POST' else ''
    return render_template('register.html', form=form, bio=sanitized_content)