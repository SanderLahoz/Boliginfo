import os
import pandas as pd
from flask import send_file
from flaskblog import db
from flaskblog.models import House, Postnummer, Region
from secrets import token_hex


def query_data(postnummer):

	postnummer_id = Postnummer.query.filter_by(postnummer=postnummer).first().id
	data = House.query.filter_by(postnummer_id=postnummer_id).order_by("price").all()
	return data


def calc_success(afkastkrav, leje, item):

	calculated_leje = (float(item.price) * float(afkastkrav)/100 + float(item.expenses) * 12) / float(item.square_footages)
	if calculated_leje >= float(leje):
		return False
	else:
		return True


def get_stats(data):
	
	average_price = 0
	average_price_per_square_footages = 0
	average_expenses = 0
	average_for_sale_days = 0
	average_rooms = 0
	average_size = 0

	for item in data:
		average_price += item.price
		average_price_per_square_footages += item.price / item.square_footages
		average_expenses += item.expenses
		average_for_sale_days += item.for_sale_days
		average_rooms += item.rooms
		average_size += item.square_footages

	length = len(data)
	if length < 1:
		return [0, 0, 0, 0, 0, 0]

	average_price = round((average_price / length), 2)
	average_price_per_square_footages = round((average_price_per_square_footages / length), 2)
	average_expenses = round((average_expenses / length), 2)
	average_for_sale_days = round((average_for_sale_days / length))
	average_rooms = round((average_rooms / length))
	average_size = round((average_size / length))

	statistics = [average_price, average_price_per_square_footages, 
	average_expenses, average_for_sale_days, average_rooms, average_size]
	
	return statistics


def download_excel(data):

	formated_data = []
	for item in data:
		row = [
			item.address,
			item.price,
			item.square_footages,
			item.expenses,
			item.land,
			item.rooms,
			item.for_sale_days,
			item.construction_year,
			item.url
		]
		formated_data.append(row)

	df = pd.DataFrame(formated_data, columns=["Adresse", 
		"Pris", "Kvadratmeter", "Ejerudgift/Ydelse", 
		"Grund", "Værelser", "Liggetid", "Opbyggelsesår", "URL"])

	name = str(token_hex(16) + ".xlsx")
	path = (os.getcwd() +"/flaskblog/static/temp/" + name)
	df.to_excel(path, index=False)

	return send_file(path, as_attachment=True), path


def get_house_data(house_id):
	return House.query.filter_by(id=house_id).first()


def calculate_value(investment_sum, scrap_value, payment, number_of_payments, interest, pay_increase=None, step=1):

	interest = interest/100

	NB = []
	NB.append(investment_sum * (-1))

	if pay_increase == None:
		payments = []
		for i in range(number_of_payments):
			payments.append(payment)
	else:
		payments = []
		for i in range(number_of_payments):
			payments.append(payment)
			if (i + 1) % step == 0:
				payment = payment * (1 + (pay_increase/100))

	for i in range(len(payments)):
		NB.append(payments[i])

	NB[-1] = NB[-1] + scrap_value

	NV = 0
	N = len(NB)

	for t in range(N):
		NV += NB[t] / ((1 + interest)**(t))

	return round(NV, 2)

