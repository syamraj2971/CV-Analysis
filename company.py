from flask import *
from database import *
import uuid
company=Blueprint('company',__name__)

@company.route('/company_home',methods=['get','post'])
def company_home():
	if not session.get("lid") is None:
		data={}
		qry="select * from company where company_id='%s'"%(session['cpnyid'])
		data['res']=select(qry)
		if 'submit' in request.form:
			name=request.form['cname']
			place=request.form['place']
			phone=request.form['phone']
			mail=request.form['email']
			q="update company set company='%s',place='%s',phone='%s',email='%s' where company_id='%s'"%(name,place,phone,mail,session['cpnyid'])
			update(q)
			return redirect(url_for('company.company_home'))
		return render_template("company_home.html",data=data)
	else:
		return redirect(url_for('public.login'))

@company.route('/company_Manage_job',methods=['get','post'])
def company_Manage_job():
	if not session.get("lid") is None:
		data={}
		q="SELECT * FROM job WHERE `company_id`='%s'"%(session['cpnyid'])
		data['job']=select(q)
		if 'submit' in request.form:
			job=request.form['job']
			det=request.form['det']
			date=request.form['date']
			req=request.form['req']
			q="INSERT INTO `job` VALUES (null,'%s','%s','%s','%s','%s')"%(session['id'],job,det,date,req)
			insert(q)
			flash('JOB DETAILS ADDED')
			return redirect(url_for('company.company_Manage_job'))
		if 'action' in request.args:
			action=request.args['action']
			id=request.args['id']
		else:
			action=None
		if action=='delete':
			q="DELETE FROM job WHERE job_id='%s'"%(id)
			delete(q)
			
			flash('JOB DETAILS DELETED')
			return redirect(url_for('company.company_Manage_job'))
		if action=='update':
			q="SELECT * FROM job WHERE job_id='%s'"%(id)
			data['job_up']=select(q)
		if 'updatez' in request.form:
			job=request.form['job']
			det=request.form['det']
			date=request.form['date']
			req=request.form['req']
			q="UPDATE `job` SET `job`='%s',`details`='%s',`last_date`='%s',requirements='%s'  WHERE job_id='%s'"%(job,det,date,req,id)
			
			update(q)
			flash('JOB DETAILS UPDATED')
			return redirect(url_for('company.company_Manage_job'))
		return render_template("company_Manage_job.html",data=data)
	else:
		return redirect(url_for('public.login'))
	







@company.route('/company_View_application',methods=['get','post'])
def company_View_application():
	if not session.get("lid") is None:
		data={}
		jid=request.args['jid']
		data['jid']=jid
		print(jid)
		# q="SELECT *,CONCAT(`user`.`fname`,' ',`user`.`lname`) AS `user` FROM `application` INNER JOIN `job` ON application.company_id=job.company_id INNER JOIN `company` ON application.company_id=company.company_id INNER JOIN `user` ON application.`user_id`=`user`.`user_id` WHERE job.job_id='%s' ORDER BY `application_id`DESC"%(jid)
		q="SELECT *,CONCAT(`user`.`fname`,' ',`user`.`lname`) AS `user` FROM `application` INNER JOIN `job` USING(job_id)  INNER JOIN `company` ON company.company_id=application.company_id INNER JOIN `user` USING(user_id) WHERE job_id='%s' ORDER BY `application_id`  DESC"%(jid)
 
		data['resume']=select(q)
		return render_template("company_View_application.html",data=data)
	else:
		return redirect(url_for('public.login'))





@company.route('/company_View_resume',methods=['get','post'])
def company_View_resume():
	if not session.get("lid") is None:
		data={}
		return render_template("company_View_resume.html",data=data)
	else:
		return redirect(url_for('public.login'))





@company.route('/company_Sent_complaint',methods=['get','post'])
def company_Sent_complaint():
	if not session.get("lid") is None:
		data={}
		if 'submit' in request.form:
			comp=request.form['comp']
			q="INSERT INTO `complaint`(`user_id`,`user_type`,`complaint`,`reply`,`date`) VALUES ('%s','company','%s','pending',CURDATE())"%(session['id'],comp)
			insert(q)
			flash('COMPLAINT DELIVERED')
			return redirect(url_for('company.company_Sent_complaint'))
		q="SELECT * FROM `complaint` WHERE `user_id`='%s' AND `user_type`='company'"%(session['id'])
		data['complaint']=select(q)
		return render_template("company_Sent_complaint.html",data=data)
	else:
		return redirect(url_for('public.login'))


@company.route('/company_addtest',methods=['get','post'])
def company_addtest():
	data={}
	cid=session['cpnyid']
	d="select * from online_test inner join test_type using(test_type_id) where company_id='%s'"%(session['cpnyid'])
	data['view']=select(d)
	s="select * from test_type "
	data['res']=select(s)
	if 'submit' in request.form:
		type=request.form['testtype']
		qstn=request.form['question']
		qstn=qstn.replace("'","''")

		opt1=request.form['option1']
		opt2=request.form['option2']
		opt3=request.form['option3']
		# opt4=request.form['option4']
		copt=request.form['coption']

		qry="insert into online_test values(null,'%s','%s','%s','%s','%s','%s','%s')"%(type,qstn,opt1,opt2,opt3,copt,cid)
		insert(qry)
		return redirect(url_for('company.company_addtest'))
	return render_template("company_addtest.html",data=data)

@company.route('/company_view_malpractice')
def company_view_malpractice():
	data={}
	# d="select * from malpractice inner join user using (user_id) where company_id='%s'"%(session['cpnyid'])
	d="select * from malpractice inner join user using (user_id) where company_id='%s'"%(session['cpnyid'])

	data['view']=select(d)
	return render_template('company_view_malpractice.html',data=data)

@company.route('/company_view_testresult')
def company_view_testresult():
	data={}
	d="select * from answer inner join test_type using(test_type_id) inner join user using(user_id) where company_id='%s'"%(session['cpnyid'])
	data['view']=select(d)
	return render_template('company_view_testresult.html',data=data)


