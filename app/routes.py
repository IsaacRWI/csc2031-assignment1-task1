from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import RegistrationForm
from bleach import clean
import logging
from datetime import datetime

safe_tags = {"b", "i", "u", "em", "strong", "a", "p", "ul", "ol", "li"}  # safe tags for bio content

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # sets up logging

def log_event(level, message, username=None):
    """defines legging message format and log tags"""
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} Client IP:{ip}, User:{username or "N/A"} | {message}"  # sets up logging message template
    if level == "info":
        logging.info(log_message)
    elif level == "warning":
        logging.warning(log_message)  # logs a warning message if warning tag passed in

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.register'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    """the block on the webpage"""
    form = RegistrationForm()  # form = new instance of RegistrationForm
    sanitized_content = None  # for sanitized bio content later on
    if form.validate_on_submit():  # if form validates on submit
        if form.bio.data:  # if bio input is not empty
            bio_content = form.bio.data
            sanitized_content = clean(bio_content, tags=safe_tags, attributes={'a': ['href', 'title']}, strip=True)  # cleaning bio input using bleach

            if bio_content == sanitized_content:  # bio contained no disallowed tags
                log_event("info", "Successful Registration", form.username.data)
                flash(f"Registration Success, Username {form.username.data} registered", "info")
            else:  # bio contained disallowed tags
                log_event("warning", "bio contained restricted tags", form.username.data)
                sanitized_content = ""  # empties sanitized content
                flash("Registration Failed, Bio content contained restricted tags", "warning")
        else:  # form validates and bio input is empty
            log_event("info", "Successful Registration, no bio", form.username.data)
            flash(f"Registration Success, Username {form.username.data} registered with no bio", "info")

    elif request.method == "POST":  # form validation failed
        for field, errors in form.errors.items():
            for i in errors:
                log_event("warning", f"Validation Failed: {field} - {i}", form.username.data)
                print(f"validation error {field} - {i}")
                flash(f"Registration Failed, Validation Error {field} - {i}", "warning")

    # client_ip = request.remote_addr or "Unknown IP"


    # name = request.form.get('name') if request.method == 'POST' else ''
    return render_template('register.html', form=form, bio=sanitized_content)