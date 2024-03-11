from flask import render_template, request, Blueprint

payment = Blueprint("payment", __name__)



@payment.route("/pricing")
def pricing():
	#other functionallity
	#-------here---------
	return render_template("payment/pricing.html")
