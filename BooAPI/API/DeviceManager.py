from collections import deque
import secrets 
import json
import re

from API import db
from API.models import Device

class Device_Manager:
	
	FILE = "devices.json"

	verbose = True

	def __split_dict(self,x):
		# EX = 
		# {"name": "Desk Lamp", "type": "int", "description": "", "id": "bf02c8a960fc78bdffd6"} 
		pattern = re.compile(r'[}]')
		matches = pattern.finditer(x)

		for match in matches:
			yield match

	def __print(self,message,type="info"):
		if self.verbose:
			print(f"[{type}] {message}")

	def create_device(self,name,value,value_type,owner,date_created,description=""):
		device = {
			'name':str(name),
			'value':str(value),
			'type':str(value_type),
			'description':str(description),
			'owner':owner,
			'date_created':date_created,
			'id':secrets.token_hex(10)
		}

		while self.get_device(device['id']) is not None:
			device['id'] = secrets.token_hex(10)

		Device(device)

		device['date_created'] = str(device['date_created'])
		device['owner'] = device['owner'].username

		with open(Device_Manager.FILE,"a") as file:
			json.dump(device,file)

		return device

	def get_devices(self):
		file = open(Device_Manager.FILE,"r")
		content = file.read()
		file.close()

		devices = deque([])
		start_index = 0
		for device in self.__split_dict(content):
			devices.append(json.loads(content[start_index:device.span()[1]]))
			start_index = device.span()[1]

		return devices

	def get_device(self,ID,from_="db"):
		if from_=="json":
			for device in self.get_devices():
				if device["id"]==ID:
					return device 

		elif from_=="db":
			return Device.query.filter_by(device_id=ID).first()

		return None

	def delete_all_devices(self,permission_code="default"):
		if permission_code=="default":
			devices = Device.query.all()
			for device in devices:
				db.session.delete(device)
			db.session.commit()

			self.__print("All devices have been deleted")
		

def main():
	d = Device_Manager()

	# device = d.create_device("Desk Lamp",0,"int")
	# print(device)

	print(d.get_devices())
	
	device = d.get_device("faf53d1cd66e046c8f19")
	print(device)

if __name__=="__main__":
	main()