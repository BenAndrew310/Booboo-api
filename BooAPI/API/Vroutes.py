from flask import jsonify, request
from API import app, db, bcrypt
from API.models import User, Device,UserKey
from API.routes import access_device

def error_handler(message,status_code=404,payload=None):
	return jsonify({
		'message':message,
		'status_code':status_code,
		'payload':payload or ()
		})

#@app.route("/api/v1/devices/all/<owner>/<password>", methods=['GET'])
@app.route("/api/v1/devices/all/<user_key>", methods=['GET'])
def api_devices(user_key):
	# user = User.query.filter_by(username=owner).first()
	# if user and bcrypt.check_password_hash(user.password, password):
	key = UserKey.query.filter_by(key=user_key).first()
	if key:
		user = User.query.filter_by(username=key.username).first()
		devices = user.devices
		result = []
		for device in devices:
			result.append({'name':device.name,
							'ID':device.device_id,
							'value':device.value,
							'value type':device.value_type,
							'date created':device.date_created,
							'description':device.description})

		return jsonify(result)

	return error_handler("No such user key")

@app.route("/api/v1/device/<user_key>/<device_id>", methods=['GET'])
def api_device(user_key,device_id):
	key = UserKey.query.filter_by(key=user_key).first()
	if key:
		user = User.query.filter_by(username=key.username).first()
		devices = user.devices
		for device in devices:
			if device_id==device.device_id:
				# device = Device.query.filter_by(device_id=device_id).first()
				return jsonify({'name':device.name,
						'ID':device.device_id,
						'value':device.value,
						'value type':device.value_type,
						'date created':device.date_created,
						'description':device.description})

	return error_handler("Erroneous 'user key' or 'device id'")

# @app.route("/api/v1/device/post-value/<device_id>/<new_value>", methods=['POST'])
# def api_device_post(device_id,new_value):
# 	device = Device.query.filter_by(device_id=device_id).first()
# 	device.value = new_value
# 	db.session.commit()

# 	result = {'name':device.name,
# 			'ID':device.device_id,
# 			'value':device.value,
# 			'value type':device.value_type,
# 			'date created':device.date_created,
# 			'description':device.description}
# 	# access_device(device_id)
# 	return jsonify(result)

@app.route("/api/v1/device/post-value/<user_key>/<device_id>/<new_value>", methods=['POST'])
def api_device_post(user_key,device_id,new_value):
	key = UserKey.query.filter_by(key=user_key).first()
	if key:

		device = Device.query.filter_by(device_id=device_id).first()
		device.value = new_value
		db.session.commit()

		result = {'name':device.name,
				'ID':device.device_id,
				'value':device.value,
				'value type':device.value_type,
				'date created':device.date_created,
				'description':device.description}
		# access_device(device_id)
		return jsonify(result)

	return error_handler("Erroneous 'user key' or 'device id'")