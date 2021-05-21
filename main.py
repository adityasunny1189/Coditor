from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = 'Very hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(200), nullable=False)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	heading = db.Column(db.String(100), nullable=False)
	content = db.Column(db.String(200), nullable=False)

# db.create_all()

@app.route('/')
def home():
	return 'Hello World'

@app.route('/register', methods=['POST'])
def register():
	new_user = User(
					name=request.form['name'],
					email=request.form['email']
				)
	db.session.add(new_user)
	db.session.commit()
	return jsonify([{"message": "user added successfully"}])

@app.route('/getusers', methods=['GET'])
def get_users():
	users = db.session.query(User).all()
	data = []
	for user in users:
		user_data = {
			"name" : user.name,
			"email" : user.email
		}
		data.append(user_data)
	return jsonify(users=data)

@app.route('/addpost/<string:user>', methods=['POST'])
def add_post(user):
	if user == 'admin':
		new_post = Post(
						heading=request.form['heading'],
						content=request.form['content']
					)
		db.session.add(new_post)
		db.session.commit()
		return jsonify([{"message": "post created"}])
	else:
		return jsonify([{"message": "unauthorized access"}])

@app.route('/announcement', methods=['GET'])
def get_post():
	posts = db.session.query(Post).all()
	data = []
	for post in posts:
		post_info = {
			"heading" : post.heading,
			"content" : post.content
		}
		data.append(post_info)
	return jsonify(announcements=data)

if __name__ == '__main__':
	app.run(debug=True, port=3000)
