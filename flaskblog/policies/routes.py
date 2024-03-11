from flask import render_template, request, Blueprint

policies = Blueprint("policies", __name__)


@policies.route("/privacy_policy")
def privacy_policy():
	return render_template("policies/privacy_policy.html")


@policies.route("/cookie_policy")
def cookie_policy():
	return render_template("policies/cookie_policy.html")


@policies.route("/termsandconditions")
def termsandconditions():
	return render_template("policies/termsandconditions.html")


@policies.route("/termsofuse")
def termsofuse():
	return render_template("policies/termsofuse.html")