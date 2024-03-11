from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    is_premium = db.Column(db.Boolean, default=False, nullable=False)
    is_newsletter_subscribed = db.Column(db.Boolean, default=False, nullable=False)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User<username: '{self.username}', email: '{self.email}', is premium: '{self.is_premium}'>"


#parent of Postnummer
class Region(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    postnumre = db.relationship("Postnummer", backref="region")


    def __repr__(self):
        return f"Region<region: '{self.region}>"


#parent of House
class Postnummer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    postnummer = db.Column(db.Integer, nullable=False)
    houses = db.relationship("House", backref="postnummer")
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))


    def __repr__(self):
        return f"Postnummer<postnummer: '{self.postnummer}', region id: '{self.region_id}'>"


#Main data
class House(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    square_footages = db.Column(db.Integer, nullable=True)
    expenses = db.Column(db.Integer, nullable=True)
    land = db.Column(db.Integer, nullable=True)
    rooms = db.Column(db.Integer, nullable=True)
    for_sale_days = db.Column(db.Integer, nullable=True)
    construction_year = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    postnummer_id = db.Column(db.Integer, db.ForeignKey('postnummer.id'))


    def __repr__(self):
        return f"House<address: '{self.address}', url: '{self.url}', postnummer id: '{self.postnummer_id}'>"



