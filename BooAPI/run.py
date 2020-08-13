from API import app
# from API import db

# from API.models import User, Device

#users = User.query.all()

# @app.before_first_request
# def create_tables():
# 	db.create_all()

# user = User(username="Benchley",email="andreben2442@gmail.com",password="password")
# db.session.add(user)
# db.session.commit() 

if __name__=="__main__":
	# if not os.path.exists('db.sqlite'):
	# 	db.create_all()
	app.run(debug=True)
