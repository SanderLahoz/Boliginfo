from flask import render_template, Blueprint, url_for, request, flash, redirect, after_this_request
from flaskblog.software.dataExtractor import extracter
from flaskblog.software.forms import PostnummerForm, QueryForm, CalculatorForm
from flaskblog.software.utils import query_data, calc_success, get_stats, download_excel, get_house_data, calculate_value
from flask_login import login_required
from threading import Thread
import sys, os


software = Blueprint("software", __name__)

@software.route("/boligdata", methods=['GET', 'POST'])
@login_required
def boligdata():
	form = PostnummerForm()
	if form.validate_on_submit():
		extracter(form.region_id.data)

	return render_template("software/boligdata.html", form=form)


@software.route("/investment", methods=['GET', 'POST'])
@login_required
def investment():
	house_id = request.args.get("house")
	house = get_house_data(house_id)
	return render_template("software/investment.html", house=house)


@software.route("/calculator", methods=['GET', 'POST'])
@login_required
def calculator():
	form = CalculatorForm()

	if form.validate_on_submit():

		if not form.pay_increase.data:
			value = calculate_value(investment_sum=form.investment_sum.data,
				scrap_value=form.scrap_value.data,
				payment=form.payment.data,
				number_of_payments=form.number_of_payments.data,
				interest=form.interest.data)
			return render_template("software/calculator.html", form=form, value=value)
		elif form.pay_increase.data and not form.step.data:
			value = calculate_value(investment_sum=form.investment_sum.data,
				scrap_value=form.scrap_value.data,
				payment=form.payment.data,
				number_of_payments=form.number_of_payments.data,
				interest=form.interest.data,
				pay_increase=form.pay_increase.data)
			return render_template("software/calculator.html", form=form, value=value)
		else:
			value = calculate_value(investment_sum=form.investment_sum.data,
			scrap_value=form.scrap_value.data,
			payment=form.payment.data,
			number_of_payments=form.number_of_payments.data,
			interest=form.interest.data,
			pay_increase=form.pay_increase.data,
			step=form.step.data)
			return render_template("software/calculator.html", form=form, value=value)


	return render_template("software/calculator.html", form=form)


@software.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():

	form = QueryForm()
	if form.validate_on_submit():
		try:
			data = query_data(int(form.postnummer.data))
			statistics = get_stats(data)
		except:
			flash("Postnummer findes ikke", "danger")
			return redirect(url_for("software.dashboard"))

	try:
		if form.afkastkrav.data and form.leje.data:
			try:
				return render_template("software/dashboard.html", calc_success=calc_success,
					afkastkrav=form.afkastkrav.data, leje=form.leje.data, 
					postnummer=form.postnummer.data, data=data, statistics=statistics, form=form)
			except:
				flash("Ugyldigt afkastkrav eller leje", "danger")
				return redirect(url_for("software.dashboard"))

		else:
			return render_template("software/dashboard.html", postnummer=form.postnummer.data, 
				data=data, statistics=statistics, form=form)
	except:
		return render_template("software/dashboard.html", postnummer=form.postnummer.data, form=form)


@software.route("/download", methods=['GET', 'POST'])
@login_required
def download_file():
	
	try:
		postnummer = request.args.get("form")
		data = query_data(int(postnummer))
	except ValueError:
		flash("Could not find data", "danger")
		return redirect(url_for("software.dashboard"))

	response, path = download_excel(data)
	
	@after_this_request
	def remove_file(response):
		try:
			os.remove(path)
			print("File removed successfully:", path)
		except Exception as e:
			print("Error removing file:", e)
		return response

	return response
			

	