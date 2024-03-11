from dotenv import load_dotenv
import os.path
import os


load_dotenv()

class Config:
	SECRET_KEY = os.getenv("SOP_SECRET_KEY")

	BASE_DIR = os.path.dirname(os.path.abspath(__file__))

	SQLALCHEMY_DATABASE_URI = os.getenv("SOP_SQL_URI")
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.getenv("MAIL_USERNAME")
	MAIL_PASSWORD = os.getenv("SOP_APP_PASS")
	STRIPE_PUBLIC = os.getenv("STRIPE_PUBLIC_TEST")
	STRIPE_SECRET = os.getenv("STRIPE_SECRET_TEST")
