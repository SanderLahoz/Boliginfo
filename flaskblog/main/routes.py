from flask import render_template, request, Blueprint, url_for, redirect
from flask_login import login_required

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("main/home.html")


@main.route("/about")
def about():
    return render_template("main/about.html", title="About")


@main.route("/faq")
def faq():
    return render_template("main/faq.html")


@main.route("/getaquote")
def getaquote():
    return redirect(url_for("contacts.contact"))


@main.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    return render_template("main/analyze.html")



