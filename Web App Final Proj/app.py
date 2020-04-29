from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

# add whatever lines you need from these four lines
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

#add this class
class ExampleTable(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	
	def __repr__(self):
		return '<User %r>' % self.username

@app.route("/")
@app.route("/welcome")
def home():
	return render_template("welcome.html")

@app.route("/members")
def members():
	return render_template("members.html")

@app.route("/motivation")
def motivation():
	return render_template("motivation.html")

#add this
@app.route("/welcome2")
def welcome2():
	return render_template("welcome2.html")

# add this
@app.route("/odds")
def odds():
	if "user" in session:
		return render_template("odds.html")
	else:
		return redirect(url_for("login"))

#add this
@app.route("/register", methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		user_name = request.form['username']
		pass_word = request.form['password']
		new_user = ExampleTable(username=user_name, password=pass_word)
		try:
			success = user_name
			session["user"] = user_name
			db.session.add(new_user)
			db.session.commit()
			# return redirect('/welcome2')
			return render_template("welcome2.html", success=success)
		except:
			return 'There was an issue adding your task'
	else:
		pass
	return render_template("register.html")


#add this
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	success = None
	if request.method == 'POST':
		user_name = request.form['username']
		pass_word = request.form['password']
		user_exists = ExampleTable.query.filter_by(username=user_name).first()
		if user_exists == None:
			error = 'Invalid Credentials. Please try again.'
		else:
			if user_exists.password == pass_word:
				success = request.form['username']
				session["user"] = user_name
				return render_template('welcome2.html', success=success)
			else:
				error = 'Invalid Credentials. Please try again.'
	else:
		if "user" in session:
			success = session["user"]
			return render_template('welcome2.html', success=success)
	return render_template('login.html', error=error)

if __name__ == "__main__":
	app.run(debug=True)