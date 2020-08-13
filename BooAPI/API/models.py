from API import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import secrets

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class UserKey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	key      = db.Column(db.String(20), unique=True, nullable=False)

	def __init__(self,username):
		k = secrets.token_hex(10)
		while UserKey.query.filter_by(key=k).first() is not None:
			k = secrets.token_hex(10)

		self.username = username
		self.key = k

		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return f"UserKey('{self.username}','{self.key}')"


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email    = db.Column(db.String(100), unique=True, nullable=False)
	img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	devices  = db.relationship('Device', backref='owner', lazy=True)

	def __repr__(self):
		return f"USER('{self.username}','{self.email}','{self.img_file}')"

class Device(db.Model):
	id           = db.Column(db.Integer, primary_key=True)
	name         = db.Column(db.String(30), nullable=False)
	device_id    = db.Column(db.String(20), unique=True, nullable=False)
	value        = db.Column(db.String(50), nullable=False)
	value_type   = db.Column(db.String(20), nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	description  = db.Column(db.Text, nullable=True)
	user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __init__(self,device : dict):
		self.name = device['name']
		self.device_id = device['id']
		self.value = device['value']
		self.value_type = device['type']
		self.owner = device['owner']
		self.date_created = device['date_created']
		self.description = device['description']

		db.session.add(self)
		db.session.commit()

	def __repr__(self):
		return f"DEVICE('{self.name}','{self.device_id}','{self.value}')"



