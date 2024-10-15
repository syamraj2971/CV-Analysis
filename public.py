from flask import *
from database import *
import uuid
public=Blueprint('public',__name__)

@public.route('/')
def home():
	return render_template("home.html")


# @public.route('/')
# def home():
# 	return render_template("index.html")


@public.route('/login',methods=['get','post'])
def login():
	session.clear()
	if 'submit' in request.form:
		username=request.form['username']
		password=request.form['password']
		q="SELECT * FROM `login` WHERE `username`='%s' AND `password`='%s'"%(username,password)
		res=select(q)
		if not res:
			flash('INCORRECT USERNAME OR PASSWORD')
		if res:
			session['lid']=res[0]['login_id']
			if res[0]['usertype']=='admin':
				flash('WELCOME TO ADMIN HOME')
				return redirect(url_for("admin.admin_home"))
			if res[0]['usertype']=='company':
				q="SELECT * FROM `company` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res1=select(q)
				if res1:
					session['id']=res1[0]['company_id']
					session['cpnyid']=res1[0]['company_id']
					session['name']=res1[0]['company']
					flash('WELCOME TO COMPANY HOME')
					return redirect(url_for("company.company_home"))
			if res[0]['usertype']=='user':
				q="SELECT * FROM `user` WHERE `login_id`='%s'"%(res[0]['login_id'])
				res2=select(q)
				if res2:
					session['id']=res2[0]['user_id']
					session['name']=res2[0]['fname']
					flash('WELCOME TO USER HOME')
					return redirect(url_for("userhome"))
	return render_template("login.html")

@public.route('/userregister',methods=['get','post'])
def userregister():
	data={}
	
	if "add" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['p']
		ph=request.form['phone']
		em=request.form['email']
		uname=request.form['uname']
		pwd=request.form['pwd']

	
		ql="insert into login values(null,'%s','%s','user')"%(uname,pwd)
		rl=insert(ql)
		qs="insert into user values(null,'%s','%s','%s','%s','%s','%s','','')"%(rl,f,l,p,ph,em)
		insert(qs)
		flash("added successfully")
		return redirect(url_for('public.userregister'))

	return render_template('userregister.html',data=data)

@public.route('/Manage_company',methods=['get','post'])
def Manage_company():

		if 'submit' in request.form:
			company=request.form['company']
			place=request.form['place']
			phno=request.form['phno']
			email=request.form['email']
			est=request.form['est']
			uname=request.form['uname']
			pwd=request.form['pwd']
			q="SELECT * FROM `login` WHERE `username`='%s'"%(uname)
			res=select(q)
			if res:
				flash('USERNAME ALREADY EXIST')
				return redirect(url_for("public.Manage_company"))
			else:
				q="INSERT INTO `login`(`username`,`password`,`usertype`) VALUES ('%s','%s','pending')"%(uname,pwd)
				id=insert(q)
				q="INSERT INTO company VALUES (null,'%s','%s','%s','%s','%s','%s')"%(id,company,place,phno,email,est)
				insert(q)
				flash('REGISTERED')
				return redirect(url_for("public.Manage_company"))
		
		return render_template("company_regisration.html")








