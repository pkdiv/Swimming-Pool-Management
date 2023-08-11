from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import psycopg2


app = Flask(__name__)

# app.config['MYSQL_HOST'] = '192.168.0.150'
# app.config['MYSQL_USER'] = 'testuser'
# app.config['MYSQL_PASSWORD'] = 'testpasswd'
# app.config['MYSQL_DB'] = 'swimming'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'flask'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'swimming'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conn = psycopg2.connect(
        host="localhost",
        database="swimming",
        user='flask',
        password='password')


app.secret_key = "asdfghhjk"

mysql = MySQL(app)


def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'userID' in session:
			return f(*args, **kwargs)
		else:
			flash('Nice try, Tricks don\'t work, bud!! Please Login :)', 'danger')
			return redirect(url_for('login'))
	return wrap


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))



@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password= request.form['password']
        cur = conn.cursor()
        cur.execute('''SELECT * FROM login WHERE email = %s''', [email])
        data = cur.fetchone()
        if data[0] > 0:
            stored_password = data[2]
            if sha256_crypt.verify(password, stored_password):
                return redirect(url_for("memberDash"))
            else:
                print('Wrong Password')
            
    return render_template('login.html')




@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute('''INSERT INTO users (name) VALUES (%s) RETURNING user_id''', (name,))
        result = cur.fetchone()
        cur.execute('''INSERT INTO login (user_id, email, password) VALUES (%s,%s,%s) RETURNING user_id''', (result[0], email,sha256_crypt.encrypt(password)))
        conn.commit()
        cur.close()
        userID = result[0]
        session['userID'] = userID
        return redirect(url_for("memberDash"))

    return render_template('register.html')


@app.route('/memberDash')
@is_logged_in
def memberDash():
    # if not session.get('userID'):
    #     return redirect(url_for('login'))
    return render_template('memberDash.html')


@app.route('/logout')
def logout():
    session.pop('userID', None)
    print(request)
    return redirect(url_for('login'))


# @app.route('/memberProf', methods = ['GET', 'POST'])
# def memberProf():
#     data = None
#     if not session.get('email'):
#         return redirect(url_for('login'))
#     if request.method == 'POST':
#         name = request.form['name']
#         city = request.form['city']
#         state = request.form['state']
#         zipcode = request.form['zipcode']
#         gender = request.form['gender']
#         phone = request.form['phone']
#         cur = mysql.connection.cursor()
#         cur.execute('INSERT INTO userDetails (name, city, state, pincode, gender, phone) VALUES (%s, %s, %s, %s, %s, %s);', (name, city, state, zipcode, gender, phone))
#         mysql.connection.commit()
#         cur.close()

#     if request.method == 'GET':
#         cur = mysql.connection.cursor()
#         email = session.get('email')
#         print(email)
#         cur.execute("SELECT userID FROM users WHERE email = %s;", [email])
#         data = cur.fetchone()
#         print(data)
#         cur.close()
#         print(data)
        

#     return render_template('memberProf.html', data=data)

# @app.route("/adminDash")
# def adminDash():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM userDetails")
#     userData = cur.fetchall()
#     cur.close()
#     return render_template('adminDash.html', userData = userData)


# @app.route('/admin', methods = ['POST', 'GET'])
# def admin():
#     if request.method == 'POST':
#         email = request.form['email']
#         password= request.form['password']
#         cur = mysql.connection.cursor()
#         result = cur.execute('SELECT * FROM admin WHERE email = %s', [email])
#         if result>0:
#             data = cur.fetchone()
#             stored_password = data['passwords']
#             if sha256_crypt.verify(password, stored_password):
#                 session['email'] = email
#                 return redirect(url_for("adminDash"))
#             else:
#                 print('Wrong Password')
            
#     return render_template('admin.html')


# @app.route('/adminLogout')
# def adminLogout():
#     session.pop('email', None)
#     return redirect(url_for('admin'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html')
