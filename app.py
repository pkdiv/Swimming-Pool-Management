from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps
import psycopg2
import psycopg2.extras



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
			flash('Please Login', 'error')
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
        if data:
            userID = data[0]
            stored_password = data[2]
            session['userID'] = userID
            if sha256_crypt.verify(password, stored_password):
                cur.execute('''SELECT roleid FROM users WHERE user_id = %s''', [userID])
                roleID = cur.fetchone()[0]
                cur.close()
                if roleID == 1:
                    return redirect(url_for("adminDash"))
                else:
                    return redirect(url_for("memberDash"))
            else:
                cur.close()
                flash('Wrong Password', 'error')
                return redirect(url_for("login"))
        else:
             flash('Email not found. Please Register', 'error')
             return redirect(url_for("login"))
            
    return render_template('login.html')




@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cur = conn.cursor()
        cur.execute('''SELECT * FROM login WHERE email = %s''', [email])
        result = cur.fetchall()
        if result == []:
            cur.execute('''INSERT INTO users (name,roleid) VALUES (%s,%s) RETURNING user_id''', (name,3))
            result = cur.fetchone()
            cur.execute('''INSERT INTO login (user_id, email, password) VALUES (%s,%s,%s) RETURNING user_id''', (result[0], email,sha256_crypt.encrypt(password)))
            conn.commit()
            cur.close()
            userID = result[0]
            session['userID'] = userID
            return redirect(url_for("memberProf"))
        else:
             flash("Email already registered.")
             return render_template('register.html')

    return render_template('register.html')


@app.route('/memberDash')
@is_logged_in
def memberDash():
    return render_template('memberDash.html')


@app.route('/logout')
def logout():
    session.pop('userID', None)
    print(request)
    return redirect(url_for('login'))


@app.route('/memberProf', methods = ['GET', 'POST'])
@is_logged_in
def memberProf():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        dob = request.form['dob']
        address = request.form['address']
        address2 = request.form['address2']
        state = request.form['state']
        country = request.form['country']
        pincode = request.form['pincode']
        cur = conn.cursor()
        cur.execute('''SELECT * FROM users WHERE user_id = %s''', (session['userID']))
        if len(cur.fetchone()) != 0:
            cur.execute(''' UPDATE users
                        SET name = %s,
                        phone = %s,
                        address = %s,
                        address2 = %s,
                        dob = %s,
                        state = %s,
                        country = %s,
                        pincode = %s
                        WHERE user_id = %s''',
                        (name,phone,address,address2,dob,state,country,pincode,session['userID']))
            
            cur.execute(''' UPDATE login
                        SET email = %s,
                    password = %s
                    WHERE user_id = %s''',
                    (email, sha256_crypt.encrypt(password), session['userID']))
        else:
            result = cur.execute('''INSERT INTO users (name,phone,address,address2,dob,state,country,pincode,roleid) VALUES (%s,%s) RETURNING user_id''', (name,phone,address,address2,dob,state,country,pincode,3))
            cur.execute('''INSERT INTO login (user_id, email, password) VALUES (%s,%s,%s) RETURNING user_id''', (result[0], email,sha256_crypt.encrypt(password)))

        conn.commit()
        cur.close()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('''SELECT * FROM users WHERE user_id = %s''', [session['userID']])
    data = cur.fetchone()
    cur.close()
    return render_template('memberProf.html', data=data)

@app.route("/dashboard")
def dashboard():
    cur = conn.cursor()
    cur.execute('''SELECT roleid FROM users WHERE user_id = %s''', [session['userID']])
    roleID = cur.fetchone()[0]
    cur.close()
    print(session['userID'])
    print(roleID)

    if roleID == 3:
         return redirect(url_for('memberDash'))
    elif roleID == 1:
        return redirect(url_for('adminDash'))
    else:
        return render_template('index.html')

@app.route("/adminDash", methods = ['GET', 'POST'])
def adminDash():
    data = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE roleid = 3 ")
    data['members'] = len(cur.fetchall())
    cur.execute("SELECT * FROM users WHERE roleid = 2 ")
    data['coaches'] = len(cur.fetchall())
    cur.execute("SELECT * FROM users WHERE roleid = 4 ")
    data['athlete'] = len(cur.fetchall())
    cur.execute("SELECT * FROM competition")
    data['competition'] = len(cur.fetchall())
    cur.execute("SELECT * FROM equipment")
    data['equipment'] = len(cur.fetchall())
    cur.close()
    return render_template('adminDash.html', data=data)

@app.route("/adminMemberTable", methods = ['GET', 'POST'])
def adminMemberTable():
    if request.method == 'POST':
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print(request.form['user_id'])
        cur.execute('''SELECT * FROM users WHERE user_id = %s''', [request.form['user_id']])
        data = cur.fetchone()
        cur.execute('''SELECT * FROM login WHERE user_id = %s''', [request.form['user_id']])
        loginData = cur.fetchone()
        data['email'] = loginData['email']
        cur.close()
        return render_template('memberProf.html', data=data)
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE roleid = 3")
        userData = cur.fetchall()
        cur.close()
        return render_template('adminMemberTable2.html', userData = userData)

@app.route("/adminCoachesTable")
def adminCoachesTable():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE roleid = 2")
    userData = cur.fetchall()
    cur.close()
    return render_template('adminCoachesTable2.html', userData = userData)

@app.route("/adminAthleteTable", methods = ['GET', 'POST'])
def adminAthleteTable():
    if request.method == 'POST':
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print(request.form['user_id'])
        cur.execute('''SELECT * FROM users WHERE user_id = %s''', [request.form['user_id']])
        data = cur.fetchone()
        cur.execute('''SELECT * FROM login WHERE user_id = %s''', [request.form['user_id']])
        loginData = cur.fetchone()
        data['email'] = loginData['email']
        cur.close()
        return render_template('memberProf.html', data=data)
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE roleid = 4")
        userData = cur.fetchall()
        cur.close()
        return render_template('adminAthleteTable.html', userData = userData)

@app.route('/competition')
def competition():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM competition")
    data = cur.fetchall()
    cur.close()
    return render_template('competition.html', compData = data)

@app.route('/equipment')
def equipment():
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM equipment")
    data = cur.fetchall()
    cur.close()
    return render_template('equipment.html', data = data)


@app.route('/addCompetition', methods = ['GET', 'POST'])
def addCompetition():
    if request.method == "POST":
        name = request.form['compName']
        location = request.form['compLocation']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        cur = conn.cursor()
        cur.execute("INSERT INTO competition(name,location,startdate,enddate) VALUES(%s,%s,%s,%s)", (name, location, startDate, endDate))
        conn.commit()
        cur.close()
    return render_template('/addCompetition.html')


@app.route('/addEquipment', methods = ['GET', 'POST'])
def addEquipment():
    # if request.method == "POST":
    #     name = request.form['compName']
    #     location = request.form['compLocation']
    #     startDate = request.form['startDate']
    #     endDate = request.form['endDate']
    #     cur = conn.cursor()
    #     cur.execute("INSERT INTO competition(name,location,startdate,enddate) VALUES(%s,%s,%s,%s)", (name, location, startDate, endDate))
    #     conn.commit()
    #     cur.close()
    return render_template('/addEquipment.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/temp')
def temp():
    return render_template('temp.html')



@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html')
