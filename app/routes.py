from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import RegistrationForm
from bleach import clean
import logging
from datetime import datetime

safe_tags = {"b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"}

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_event(level, message, username=None):
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} Client IP:{ip}, User:{username or "N/A"} | {message}"
    if level == "info":
        logging.info(log_message)
    elif level == "warning":
        logging.warning(log_message)

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

        if bio_content == sanitized_content:
            log_event("info", "Successful Registration", form.username.data)
            flash("Registration Success", "info")
        else:
            log_event("warning", "bio contained restricted tags", form.username.data)
            sanitized_content = ""
            flash("Registration Failed, Bio content contained restricted tags", "warning")

    elif request.method == "POST":
        for field, errors in form.errors.items():
            for i in errors:
                log_event("warning", f"Validation Failed: {field} - {i}", form.username.data)
                print(f"validation error {field} - {i}")
                flash(f"Registration Failed, Validation Error {field} - {i}", "warning")

    # client_ip = request.remote_addr or "Unknown IP"


    # name = request.form.get('name') if request.method == 'POST' else ''
    return render_template('register.html', form=form, bio=sanitized_content)