from flask import Blueprint, render_template, flash
from flaskblog.contacts.forms import ContactForm
from flask_login import current_user
from flaskblog.contacts.utils import send_mail

contacts = Blueprint("contacts", __name__)

@contacts.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
    	send_mail(form.name.data, form.email.data, form.subject.data, form.content.data)
    	flash(f"Mail has been send!", "success")

    return render_template("contacts/contact.html", form=form, header="Contact Us")