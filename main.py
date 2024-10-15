import re
import uuid
from flask import *
from public import public
from admin import admin
from company import company
from user import user

from database import *
from model import Model
from functions import *
from api import api


from sampleeee import *

# /////////////////////////////////////////

import os
from flask_cors import CORS
from difflib import SequenceMatcher
from flask import Flask, request, jsonify

import joblib
from flask_restful import reqparse
from bson.json_util import dumps





from math import sqrt
from flask import Flask, render_template, request, jsonify
# from __future__ import division
from collections import Counter

from predict import Predictor
from model import Model
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json
from bson import json_util
from PyPDF2 import PdfFileReader

import uuid


import os
from flask_cors import CORS
from difflib import SequenceMatcher
from flask import Flask, request, jsonify

import joblib
from flask_restful import reqparse
from bson.json_util import dumps


# ////////////////////////////////////////

M = Model()
predictor = Predictor()

app=Flask(__name__)
app.secret_key='j'

app.register_blueprint(public)
app.register_blueprint(user)
app.register_blueprint(admin)
app.register_blueprint(company)
app.register_blueprint(api)


CORS(app)
parse = reqparse.RequestParser()

model = joblib.load('model.pkl')
# prediction = model.predict([[9,1,9,3,4,5,9]])[0]


@app.route('/userhome',methods=['get','post'])
def userhome():
	data={}
	q="select * from team inner join teammember using(team_id) inner join user using(user_id) WHERE teammember.user_id='%s'"%(session['id'])
	res=select(q)
	print(res)
	if res:
		data['team']=res
		q="select * from teammember inner join user using(user_id) WHERE team_id='%s'"%(data['team'][0]['team_id'])
		res=select(q)
		if res:
			data['member']=res

	else:
		data['team']="team"
	q="select * from user WHERE user_id='%s'"%(session['id'])
	data['user']=select(q)

	q="select * from application WHERE user_id='%s'"%(session['id'])
	res=select(q)
	if res:
		data['per']=res[0]['personality']
	if 'submit' in request.form:
		fname=request.form['fname']
		lname=request.form['lname']
		place=request.form['place']
		phone=request.form['phone']
		mail=request.form['mail']
		q="update user set fname='%s',lname='%s',place='%s',phone='%s',email='%s' where user_id='%s'"%(fname,lname,place,phone,mail,session['id'])
		update(q)
		return redirect(url_for('userhome'))
	return render_template("userhome.html",data=data)



@app.route('/user_profile_view',methods=['get','post'])
def user_profile_view():
	import fitz

	data={}
	d="select * from user where login_id='%s'"%(session['lid'])
	data['view']=select(d)
	if 'submit' in request.form:
		# log_id=request.form['log_id']
		pdf=request.files['file']
		path1='static/resume/'+str(uuid.uuid4())+pdf.filename

		pdf.save(path1)
	
		print("pdf : ",pdf)

		# print("pdf : ",pdf)
			# Open the PDF file in read-binary mode
		with open(path1, 'rb') as pdf_file:
			# Create a PyPDF2 PdfReader object
			pdf_reader = fitz.open(pdf_file)

			# Get the number of pages in the PDF file
			num_pages = pdf_reader.page_count

			# Iterate through all the pages and extract the text
			text = ''
			for page_num in range(num_pages):
				page = pdf_reader.load_page(page_num)
				page_text = page.get_text()
				text += page_text

			print(text)
			
			# Sample resume text
			resume_text = text.replace("'", "''")
			# Sample resume text
			# resume_text = ress[0]['resume_skills']

			# Preprocessing
			resume_text = re.sub(r'[^\w\s]', '', resume_text)  # Remove punctuation
			resume_text = resume_text.lower()


		u="update user set cv_file='%s',cv_des='%s' where login_id='%s'"%(path1,resume_text,session['lid'])
		update(u)
		return redirect(url_for('user_profile_view'))

	return render_template('user_profile_view.html',data=data)


@app.route('/usersendcomplaints',methods=['get','post'])
def usersendcomplaints():
	data={}

	if 'submit' in request.form:
		comp=request.form['comp']
		comp = comp.replace("'","''")
		q="INSERT INTO `complaint`(`user_id`,`user_type`,`complaint`,`reply`,`date`) VALUES ('%s','user','%s','pending',CURDATE())"%(session['id'],comp)
		insert(q)
		flash('COMPLAINT DELIVERED')
		return redirect(url_for('usersendcomplaints'))
	q="SELECT * FROM `complaint` WHERE `user_id`='%s' AND `user_type`='user'"%(session['id'])
	data['complaint']=select(q)
	return render_template("usersendcomplaint.html",data=data)


@app.route('/upload_pdf_file',methods=['get','post'])
def upload_pdf_file():
	import fitz
	data = {}


	import random
	import string

	def generate_random_alphanumeric(length):
		if length < 1:
			raise ValueError("Length must be at least 1")
		
		random_string = random.choice(string.ascii_letters)  # First character is an alphabet
		random_string += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length - 1))
		
		return random_string

	# Example: Generate a random alphanumeric string of length 8
	random_string = generate_random_alphanumeric(8)
	

	qq = "SELECT * FROM `user` WHERE login_id='%s'" % (session['lid'])
	ress = select(qq)
	# Sample resume text
	resume_text = ress[0]['cv_des']
	q = "SELECT * FROM `job` INNER JOIN company USING(company_id)"
	result = select(q)
	print(result,"***************************************************")

	# Initialize an empty list to store the individual skills
	all_skills = []

	# Iterate through each dictionary in the 'result' list
	# for c_skill in result:
	# 	# Append the 'skills' value to the list
	# 	all_skills.extend(skill.strip() for skill in c_skill['requirements'].split(','))

	

	# 	# Matching skills
	# 	matches = [skill for skill in all_skills if re.search(skill.lower(), resume_text)]

	# 	# Scoring matches
	# 	score = len(matches)
	# 	print("score : ", score)
	# 	matched_job_vacancies=""
	for c_skill in result:
		# Append the 'skills' value to the list
		all_skills.extend(skill.strip() for skill in c_skill['requirements'].split(','))

		# Matching skills
		matches = [skill for skill in all_skills if re.search(re.escape(skill.lower()), resume_text, re.IGNORECASE)]

		# Scoring matches
		score = len(matches)
		print("score : ", score)
		matched_job_vacancies = ""

		# Filtering resumes
		threshold = 2  # Set threshold for matches
		if score >= threshold:
			# Filter job vacancies based on matches
			matched_job_vacancies = [job for job in result if any(re.search(skill.lower(), job['requirements'].lower()) for skill in matches)]
			print('Matched Job Vacancies:', matched_job_vacancies)
			data['job']=matched_job_vacancies
		else:
			print('Resume does not match')

	return render_template("upload_pdf.html",data=data)

# @app.route('/userviewjob',methods=['get','post'])
# def userviewjob():

# 	data = {}
# 	# login_id = request.args['login_id']
# 	qq = "SELECT * FROM `resume` WHERE `user_id`=(select `user_id` from user where login_id='%s')" % (session['lid'])
# 	ress = select(qq)
# 	# Sample resume text
# 	resume_text = ress[0]['resume_skills']

# 	q = "SELECT * FROM `job_vacancy` INNER JOIN job_category USING(job_category_id) INNER JOIN company USING(company_id)"
# 	result = select(q)

# 	# Initialize an empty list to store the individual skills
# 	all_skills = []

# 	# Iterate through each dictionary in the 'result' list
# 	for c_skill in result:
# 		# Append the 'skills' value to the list
# 		all_skills.extend(skill.strip() for skill in c_skill['skills'].split(','))

	

# 	# Preprocessing
# 	resume_text = re.sub(r'[^\w\s]', '', resume_text)  # Remove punctuation
# 	resume_text = resume_text.lower()  # Convert to lowercase

# 	# Matching skills
# 	matches = [skill for skill in all_skills if re.search(skill.lower(), resume_text)]

# 	# Scoring matches
# 	score = len(matches)
# 	print("score : ", score)
# 	matched_job_vacancies=""

# 	# Filtering resumes
# 	threshold = 2  # Set threshold for matches
# 	if score >= threshold:
# 		# Filter job vacancies based on matches
# 		matched_job_vacancies = [job for job in result if any(re.search(skill.lower(), job['skills'].lower()) for skill in matches)]
# 		print('Matched Job Vacancies:', matched_job_vacancies)
# 	else:
# 		print('Resume does not match')

# 	if matched_job_vacancies:
# 		data['status'] = "success"
# 		data['data'] = matched_job_vacancies
# 	else:
# 		data['status'] = 'failed'
# 	data['method'] = "User_view_job_vacancy"
# 	return render_template("userviewjob.html",data=data)


@app.route('/usersendapplication', methods=['GET', 'POST'])
def usersendapplication():
	if "job_id" in request.args:
		session['job_id'] = request.args['job_id']
		session['company_id']=cid = request.args['company_id']
	data = {}

	sid = session['id']

	q = "SELECT * FROM application WHERE user_id='%s' AND job_id='%s'" % (sid, session['job_id'])
	res = select(q)
	print(sid)
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
	if res:
		flash("YOU ALREADY REQUESTED")
		return redirect(url_for('userhome'))

	if not res:
		if "send" in request.form:
			print("_______________________________________________stage1")
			age = request.form['age']
			gender = request.form['gender']			
			re = request.files['re']
			print(">>>>>>>>>>>>>>>>>>>", age, gender)
			path = 'static/uploads/' + str(uuid.uuid4()) + re.filename
			re.save(path)
			print(path)
			splitpath = path.split('.')
			types = splitpath[1]
			print(types)
			value = ""
			if types == 'txt':
				value = txtreader(path)
			elif types == 'docx':
				value = docreader(path)
			elif types == 'pdf':
				value = pdfreader(path)

			print("???????????????????????", value)

			prediction = predictor.predict([value])

			print(prediction['pred_sOPN'])
			print(prediction['pred_sCON'])
			print(prediction['pred_sEXT'])
			print(prediction['pred_sAGR'])
			print(prediction['pred_sNEU'])

			parm1 = int(gender)
			parm2 = int(age)

			print("age++++++++++++++++++++++++++++++++", parm2)
			print("gender++++++++++++++++++++++++++++++++", parm1)

			parm3 = int(prediction['pred_sOPN'])
			parm4 = int(prediction['pred_sCON'])
			parm5 = int(prediction['pred_sEXT'])
			parm6 = int(prediction['pred_sEXT'])
			parm7 = int(prediction['pred_sNEU'])
			prediction = model.predict([[parm1, parm2, parm3, parm4, parm5, parm6, parm7]])[0]

			q = "SELECT SUM(mark_awarded) FROM `answer` WHERE user_id='%s'" % (session['id'])
			print(q)
			res = select(q)
			point = res[0]['SUM(mark_awarded)']

			# p=request.form['p']
			if point:
				q = "INSERT INTO application VALUES (null,'%s',curdate(),'%s','%s','%s','%s','%s','applied')" % (
				session['id'], path, prediction, point, session['job_id'], session['company_id'])
				insert(q)
				flash('send successfully')
			else:
				q = "INSERT INTO application VALUES (null,'%s',curdate(),'%s','%s',0,'%s','%s','applied')" % (
                session['id'], path, prediction, session['job_id'], session['company_id'])
				insert(q)
				flash('send successfully')
			return redirect(url_for('userhome'))

	return render_template('userapp.html', data=data)


@app.route('/viewscore')
def viewscore():
	data={}
	qry="select mark_awarded,grand_total from answer where answer_id='%s'"%(session['ansid'])
	data['res']=select(qry)
	return render_template("userviewscore.html",data=data)


@app.route('/userapplication')
def userapplication():
	data={}
	qry="select * from application inner join company using(company_id) where user_id='%s'"%(session['id'])
	data['res']=select(qry)
	print(data['res'],'fffffffffffffffffffffffffffffffff''''''''''''''''''''''''''''''''''''''''''''''''')
	return render_template("userapplication.html",data=data)
@app.route('/userviewcompany')
def userviewcompany():
	data={}
	qry="select * from company"
	data['res']=select(qry)
	return render_template("userviewcompany.html",data=data)


app.run(debug=True,port=5123,host="0.0.0.0")