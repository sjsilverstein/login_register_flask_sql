from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'ThisIsSecret' # you need to set a secret key for security purposes
# connect and store the connection in "mysql"; note that you pass the database name to the function
# routing rules and rest of server.py below
mysql = MySQLConnector(app, 'login_registration')
@app.route('/') #This is the root
def index():
	users = mysql.query_db("SELECT * FROM users")
	print users
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	# Pull innput Values from the form
	email =  request.form['email']
	password = request.form['password']
	validation = True
	# And check if the the password matches the hashed / salt password of the email
	result = mysql.query_db("SELECT * from users where users.email = '{}' and users.password = '{}'".format(email, password))
	print result
	print len(result)
	if len(result) < 1:
		print "No result found"
		flash("No user found")
		validation = False
	if len(result) == 1:
		print "return to success login"
		flash("Return successful login")
	#Return a redirect
	return redirect('/')


@app.route('/register', methods=['POST'])
def register():
	validation = True
	first_name = str(request.form['first_name'])
	last_name = str(request.form['first_name'])
	email = str(request.form['email'])
	password = str(request.form['password'])
		# Check that all the form fields have something filled in.
	# Check that the first and last name input fields are all alpha charactersr
	# Check that email input field is in the email format
	# Check input fields for password and confirm password. 
	# Is password at least 8 char strong and do they match?
	for key in request.form:
		if len(request.form[key]) < 1:
			print "Are any Values Blank This is Bad Fill the Form out FOOL!"
			flash("Are any Values Blank This is Bad Fill the Form out FOOL!")
			validation = False
	if not first_name.isalpha():
		print "First Name input field includes non alpha characters"
		flash("First Name input field includes non alpha characters")
		validation = False
	if not last_name.isalpha():
		print "Last Name input field includes non alpha characters"
		flash ("Last Name input field includes non alpha characters")
		validation = False
	if not EMAIL_REGEX.match(email):
		print "Regex does not like the email"
		flash("Regex does not like the email")
		validation = False
	if len(request.form['password']) < 8:
		print "Password must be more eight characters long"
		flash("Password must be more eight characters long")
		validation = False
	if request.form['password'] != request.form['confirm_password']:
		print "Password and Confirm do not match"
		flash("Password and Confirm do not match")
		validation = False
	# If validation is False the user did not fill out the registration form correctly
	# If validation is True then we need to check if the email is in the datebase already.
	# If email is in datebase we need to prompt the client
	# If email not in datebase add new row to datebase
	check_users = mysql.query_db("SELECT * from users where users.email = '{}'".format(email))
	if len(check_users) >= 1:
		print "Email was found in the users datebase table"
		flash("Email was found in the users datebase table")
	elif validation == True:
		q2="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
		data = {
		'first_name': first_name,
		'last_name': last_name,
		'email': email,
		'password': password
		}
		mysql.query_db(q2, data)
		print "user was added try loggin in"
		flash("User was added, try logging in")
	#Return a redirect
	return redirect('/')


app.run(debug=True)