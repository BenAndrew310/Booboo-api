from API import db
from API.models import User, Device, UserKey
from API.DeviceManager import Device_Manager
from datetime import datetime


if __name__=="__main__":
	# dev = Device_Manager()
	db.create_all()
	# d=datetime.utcnow()
	# dev.create_device(name="Lamp desk",value="true",value_type="boolean",date_created=d)
	
	# devices = Device.query.all()
	# print(devices)

	# users = User.query.all()
	# for user in users:
	# 	print(user)
	# 	db.session.delete(user)
	# db.session.commit()
	# devices = Device.query.all()
	# for device in devices:
	# 	print(device)
	# 	db.session.delete(device)
	# db.session.commit()
	# keys = UserKey.query.all()
	# for key in keys:
	# 	print(key)
	# 	db.session.delete(key)
	# db.session.commit()

	# userkey = UserKey.query.filter_by(username='Benchley').first()
	# userkey.username = 'ben_andrew'
	# db.session.commit()

	users = User.query.all()
	devices = Device.query.all()
	keys = UserKey.query.all()
	print(users,"\n",devices,"\n",keys)
	