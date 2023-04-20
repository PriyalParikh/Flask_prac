from flask import Flask, render_template,request,session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bab7bdf92ad4eb5bb1ad9e977b784dff'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678910'
app.config['MYSQL_DB'] = 'mydb' 
mysql=MySQL(app)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        cur= mysql.connection.cursor()
        username = request.form['Username']
        password = request.form['Password']
        email = request.form['Email']
        cur.execute('SELECT * FROM user WHERE username = % s', (username, ))
        user = cur.fetchone()
        if user:
            return 'Account already exists !'
        else:
            cur.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            cur.close()
            return 'You have successfully registered !'
    return render_template('register.html', title='Register')
    
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        username = request.form['Username']
        password = request.form['Password']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE Username = % s AND Password = % s', (username, password, ))
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['username'] = request.form['Username']
            session['password'] = request.form['Password']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('Username', None)
   session.pop('Password', None)
   # Redirect to login page
   return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)