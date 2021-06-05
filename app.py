import flask
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import datetime
import smtplib


app = Flask(__name__,template_folder='template')

app.secret_key = 'Complain Management System'

# database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root501'
app.config['MYSQL_DB'] = 'pro39'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
@app.route('/register/', methods=['GET', 'POST'])
def register():
	msg=''
	# if request.method=="POST" and 'userid' in request.form and 'username' in request.form and 'department' in request.form and 'phoneno' in request.form and 'password' in request.form:
	if request.method=="POST":	
		username=request.form['username']
		userid=request.form['userid']
		dept=request.form['dept']
		mobile=request.form['mobile']
		password=request.form['password']
		# Existing Acc
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM faculty WHERE userid = %s', (userid,))
		account=cursor.fetchone()
		# If account exists show error and validation checks
		if account:
			msg='Account already exists!'
		elif not username or not password or not userid or not dept or not mobile:
			msg='Please fill out the form!'
		else:
			cursor.execute('INSERT INTO faculty VALUES (%s, %s, %s,%s, %s)', (userid, username, dept, mobile, password,))
			mysql.connection.commit()
			msg='You have successfully registered!'
	# elif request.method=="POST":
	# 	msg='Please Fill out the Form!'
	return render_template('index.html',msg=msg)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST' and 'userid' in request.form and 'password' in request.form:

        userid = request.form['userid']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM faculty WHERE userid = %s AND password = %s', (userid, password,))
        account = cursor.fetchone()


        if account:
            session['loggedin'] = True
            session['id'] = account['userid']
            session['username'] = account['username']
            session['dept']=account['department']
            return redirect(url_for('complaints'))
            
            
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'


    return render_template('login.html', msg='')


@app.route('/complaints/', methods=['GET', 'POST'])
def complaints():

    loginid=session['id']
    loginname=session['username']
    dept=session['dept']
    
    if request.method=="GET":
    	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    	cursor.execute('SELECT * FROM complaintstable WHERE facultyid = %s', (loginid,))
    	data=cursor.fetchall()
    	# for row in data:
    	# 	print(row)
    	# print(data[0]['compid'])
    	return render_template('home.html',loginid=loginid,loginname=loginname,dept=dept,value=data)
        
    elif request.method=="POST":
    	cattype=request.form['Category']
    	issuedescription=request.form['issuedesc']

    	cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    	cursor.execute('SELECT * FROM issuecategory WHERE type = %s', (cattype,))
    	row=cursor.fetchone()
    	comptype=row['type']
    	compoffname=row['offname']
    	compoffemail=row['offemail']
    	compstatus="open"

    	cursor1=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    	cursor1.execute("SELECT COUNT(*) FROM complaintstable")
    	property_count=cursor1.fetchone()
    	count=property_count['COUNT(*)']

    	x = datetime.datetime.now()
    	compId=x.strftime("%x")+"-->"+str(count)


    	s = smtplib.SMTP('smtp.gmail.com', 587)
    	s.starttls()
    	s.login("srk.complaintform.x4@gmail.com ","Complaint-x4")
    	message = " Complaint Id: "+compId+" \n Faculty Id: "+loginid+" \n Name: "+loginname+" \n Department: "+dept+" \n Issue : "+issuedescription+" "
    	print(message)
    	s.sendmail("srk.complaintform.x4@gmail.com",compoffemail, message)
    	s.quit()
		

    	cursor2=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    	cursor2.execute('INSERT INTO complaintstable VALUES (%s,%s, %s, %s,%s, %s,%s, %s)', (compId,loginid, dept, cattype, issuedescription, compoffname,compoffemail,compstatus,))
    	mysql.connection.commit()
    	return redirect(url_for('complaints'))



    else:
    	return render_template('login.html', msg='')




@app.route('/adminlogin/', methods=['GET', 'POST'])
def adminlogin():
	msg = ''
	if request.method=="POST" and 'useremail' in  request.form and 'password' in request.form:
		useremail=request.form['useremail']
		password=request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM admin WHERE email = %s AND password = %s', (useremail, password,))
		account=cursor.fetchone()
		print(account['email'])
		if account:
			session['adminlogin']=True
			session['adminid']=account['email']
			session['adminname']=account['name']
			
			
			
			return redirect(url_for('admindashboard'))
		else:
			msg='Incorrect username/password!'
	return render_template('adminlogin.html',msg='')



@app.route('/admindashboard/', methods=['GET', 'POST'])
def admindashboard():
	loginid1='abc'#session['adminid']
	loginname2='abc123'#session['adminname']
	print(request.method)
	# if request.method=="GET":
	# 	cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
	# 	cursor.execute('SELECT * FROM complaintstable')
	# 	data=cursor.fetchall()
	# 	return render_template('adminhome.html',loginid=loginid1,loginname=loginname2,value=data)
	return render_template('adminhome.html')

	#elif request.method=="POST":
		#ComplaintId=request.form['complaintId']
		#updateStatus=request.form['revisestatus']
		#cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		#cursor.execute('UPDATE complaintstable set status=%s where compid=%s',(updateStatus,ComplaintId,))
		#mysql.connection.commit()
		#return redirect(url_for('admindashboard'))





@app.route('/adminlogout/')
def adminlogout():
    # Remove session data, this will log the user out
   session.pop('adminlogin', None)
   session.pop('adminid', None)
   session.pop('adminname', None)
   # Redirect to login page
   return redirect(url_for('adminlogin'))



@app.route('/logout/')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(port=5000,debug=True)