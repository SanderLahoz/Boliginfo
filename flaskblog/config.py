import os

class Config:
	SECRET_KEY = os.environ.get("SOP_SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.environ.get("SOP_SQL_URI")
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("SOP_APP_PASS")
	STRIPE_PUBLIC = os.environ.get("STRIPE_PUBLIC_TEST")
	STRIPE_SECRET = os.environ.get("STRIPE_SECRET_TEST")
