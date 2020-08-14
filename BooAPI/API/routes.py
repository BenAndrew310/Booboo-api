from flask import Flask,render_template,url_for,jsonify,flash,redirect,request
from flask_login import login_user, current_user, logout_user, login_required
from API.DeviceManager import Device_Manager
from API.CreateDevice import Create_Device
from API.Registration import Signup, Login, ChangeUserInformation
from API.models import User, Device, UserKey
from API import app, db, bcrypt
import markdown
from datetime import datetime
import os

DEVICE = Device_Manager()
img = "\\resources\\technology-computer.jpg"
background_image = os.path.dirname(os.path.realpath(__file__))+img

@app.route("/",methods=("GET","POST"))
@app.route("/api",methods=("GET","POST"))
def home():
	return render_template("home.html",title="BOOBOO API",bg_img=background_image)

@app.route("/api/documentation",methods=["GET","POST"])
def documentation():
	#with open(os.path.dirname(app.root_path)+"\\API\\README.md",'r') as file:
	#with open("\\API\\README.md",'r') as file:
		#content = file.read()
		#content = markdown.markdown(content)
		#return markdown.markdown(content)
	return render_template("documentation.html",title="documentation")

@app.route("/api/create-device",methods=["GET","POST"])
@login_required
def create_device():
	form=Create_Device()
	#if form.validate_on_submit():
	if form.is_submitted():
		result = request.form
		# today = datetime.date.today()
		# date = (today.day,today.month,today.year)
		date = datetime.utcnow()

		try:
			device = DEVICE.create_device(result['name'],result['value'],result['value_type'],current_user,date,result['description'])
		except KeyError:
			return redirect(url_for('create_device'))

		#return render_template("device_created.html",title="success",id=device["id"])
		return redirect(url_for('devices'))

	return render_template("create_device_form.html",title="new device",form=form)

@app.route("/api/device/<device_id>")
@login_required
def access_device(device_id):
	device = DEVICE.get_device(device_id)
	if device not in current_user.devices:
		device=None
	
	return render_template("my_device.html",title=device.name,device=device,none=None,refresh_on=True,str=str)

@app.route("/api/device/delete/<device_id>")
@login_required
def delete_device(device_id):
	device = Device.query.filter_by(device_id=device_id).first()
	# flash(f"{device.name} is deleted")
	db.session.delete(device)
	db.session.commit()
	return redirect(url_for('devices'))

@app.route("/api/devices")
@login_required
def devices():
	devices = current_user.devices
	return render_template("all_devices.html",title="my devices",devices=devices, str=str)

@app.route("/api/login",methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.auth.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password.','danger')
	return render_template("login.html",title='Login' ,form=form)

@app.route("/api/signup",methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = Signup()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data,email=form.email.data,password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		UserKey(username=form.username.data)
		flash('Your account has been successfully created','sucsess')
		return redirect(url_for('home'))

	return render_template("signup.html",title="Register",form=form)

@app.route("/api/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/api/<username>",methods=["GET","POST"])
@login_required
def manage_account(username):
	form = ChangeUserInformation(username=current_user.username,
								email=current_user.email)
	if form.validate_on_submit():
		return redirect(url_for('update_information',
								username=form.username.data,
								email=form.email.data))
	user = UserKey.query.filter_by(username=username).first()
	key = user.key
	return render_template("account.html",title=username,key=str(key),form=form)


@app.route("/api/account/update/<username>+<email>", methods=["GET","POST"])
@login_required
def update_information(username,email):
	username = str(username)
	email    = str(email)
	CURR_USER = User.query.filter_by(username=current_user.username).first()
	CURR_USER_KEY = UserKey.query.filter_by(username=current_user.username).first()
	if username != CURR_USER.username:
		users = User.query.all()
		for user in users:
			if username==user.username or len(username)<4:
				flash(f'Invalid username {username}, please pick a new one.','danger')
				return redirect(url_for('manage_account',username=CURR_USER.username))
		CURR_USER.username = username
		CURR_USER_KEY.username = username
		if email!=CURR_USER.email:
			CURR_USER.email = email
		db.session.commit()
		flash(f'Information saved successfully. Please login with your new username {username}')
		return redirect(url_for('logout'))
	if email != CURR_USER.email:
		CURR_USER.email = email
		db.session.commit()
		flash('Information saved successfully.')
	return redirect(url_for('home'))
	
