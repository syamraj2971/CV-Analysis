import re
from flask import *
from database import *

import demjson
from predictt import predict
import uuid
import cv2
import io
import requests
from functions import *

from model import Model


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


from math import sqrt
from flask import Flask, render_template, request, jsonify
# from __future__ import division
from collections import Counter
from flask import Flask, request
from predict import Predictor
from model import Model
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json
from bson import json_util
from PyPDF2 import PdfFileReader
from flask import *
from database import *
import uuid

from functions import *


import os
from flask_cors import CORS
from difflib import SequenceMatcher
from flask import Flask, request, jsonify

import joblib
from flask_restful import reqparse
from bson.json_util import dumps

api=Flask(__name__)
api.secret_key="J"

# ////////////////////////////////////////
api=Blueprint('api',__name__)
M = Model()
predictor = Predictor()

CORS(api)
parse = reqparse.RequestParser()

model = joblib.load('model.pkl')
prediction = model.predict([[9,1,9,3,4,5,9]])[0]
print(prediction)



@api.route('/loginapi',methods=['get','post'])
def loginapi():
	data={}
	
	username = request.args['username']
	password = request.args['password']
	q="SELECT * from login where username='%s' and password='%s'" % (username,password)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
		session['id']=res[0]['login_id']
	else:
		data['status']	= 'failed'
	data['method']='login'
	return  str(data)


@api.route('/userregisterapi',methods=['get','post'])
def userregisterapi():
	data={}

	uname = request.args['uname']
	passs = request.args['pass']
	fname = request.args['fname']
	lname = request.args['lname']
	email = request.args['email']
	place = request.args['place']
	phone = request.args['phone']

	q="insert into login values(null,'%s','%s','user')" %(uname,passs)
	id=insert(q)
	q="insert into user values(null,'%s','%s','%s','%s','%s','%s')" %(id,fname,lname,place,phone,email) 
	insert(q)
	
	data['status']  = 'success'
	
	data['method']='userregister'
	return  str(data)


# @api.route('/UserViewJobs',methods=['get','post'])
# def UserViewJobs():
# 	data={}
	
# 	q="SELECT * from job"
# 	res = select(q)
# 	if res :
# 		data['status']  = 'success'
# 		data['data'] = res
# 	else:
# 		data['status']	= 'failed'
# 	data['method']='UserViewJobs'
# 	return  str(data)


@api.route('/UserViewJobs',methods=['get','post'])
def UserViewJobs():
	
	import fitz
	data = {}


	import random
	import string
	lid=request.args['lid']
	def generate_random_alphanumeric(length):
		if length < 1:
			raise ValueError("Length must be at least 1")
		
		random_string = random.choice(string.ascii_letters)  # First character is an alphabet
		random_string += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length - 1))
		
		return random_string

	# Example: Generate a random alphanumeric string of length 8
	random_string = generate_random_alphanumeric(8)
	

	qq = "SELECT * FROM `user` WHERE login_id='%s'" % (lid)
	ress = select(qq)
	print("_____________________________res________________________________",ress)
	# Sample resume text
	resume_text = ress[0]['cv_des']
	print("##################################################################",type(resume_text))
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
			data['data'] = matched_job_vacancies

		else:
			print('Resume does not match')
	
	# q="SELECT * from job"
	# res = select(q)


	if matched_job_vacancies :
		data['status']  = 'success'
	else:
		data['status']	= 'failed'
	data['method']='UserViewJobs'
	return  str(data)





@api.route('/UserViewcompany',methods=['get','post'])
def UserViewcompany():
	data={}
	
	cid = request.args['cid']
	q="SELECT * from company where company_id='%s'" %(cid)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='UserViewcompany'
	return  str(data)



@api.route('/UserViewrequests',methods=['get','post'])
def UserViewrequests():
	data={}
	
	lid = request.args['lid']
	q="SELECT * from application inner join job using(job_id)  where user_id=(select user_id from user where login_id='%s')" %(lid)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
		data['method']='UserViewrequests'

	else:
		data['status']	= 'failed'
		data['method']='UserViewrequests'
	return  str(data)




@api.route('/userviewcomplaint',methods=['get','post'])
def userviewcomplaint():
	data={}
	
	lid = request.args['lid']
	q="SELECT * from complaint where user_id=(select user_id from user where login_id='%s')" %(lid)
	res = select(q)
	if res :
		data['status']  = 'success'
		data['data'] = res
	else:
		data['status']	= 'failed'
	data['method']='userviewcomplaint'
	return  str(data)

@api.route('/usersendcomplaint',methods=['get','post'])
def usersendcomplaint():
	data={}

	lid = request.args['lid']
	comp = request.args['comp']

	q="insert into complaint values(null,(select user_id from user where login_id='%s'),'user','%s','pending',curdate())" %(lid,comp) 
	insert(q)
	
	data['status']  = 'success'
	
	data['method']='usersendcomplaint'
	return  str(data)


@api.route('/upload_pdf',methods=['get','post'])
def user_upload_pdf():
	data={}

	logid = request.args['logid']
	# aid = request.args['aid']
	jid=request.args['jid']
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",jid)

	cid=request.args['cid']
	# print("logid,aid,jid,cid",logid,aid,jid,cid)
	# print(image)
	u="select * from user where login_id='%s'"%(logid)
	ui=select(u)
	uid=ui[0]['user_id']
	q="select * from application where user_id=(select user_id from user where login_id='%s') and job_id='%s'" %(logid,jid)
	print(q)
	res=select(q)
	print("##############",res)
	if res:
		print("__________________________have_______________________________________")
		data['status']='already exist'
		
	else:
		image = request.files['pdf']
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",image)


		
		print("__________________________not_______________________________________________")
		path='static/uploads/'+str(uuid.uuid4())+image.filename
		image.save(path)
		print(path)		
		skill="sdfdsg"


		splitpath=path.split('.')
		types=splitpath[1]
		print(types)
		if types=='txt':
			value=txtreader(path)
		if types=='docx':
			value=docreader(path)
		if types=='pdf':
			value=pdfreader(path)

		print("***********************",value)


		prediction =  predictor.predict([value])
		print(prediction['pred_sOPN'])
		print(prediction['pred_sCON'])
		print(prediction['pred_sEXT'])
		print(prediction['pred_sAGR'])
		print(prediction['pred_sNEU'])

		# parm1 = int(gender)
		# parm2 = int(age)
		parm1 = 3
		parm2 = 44

		parm3 = int(prediction['pred_sOPN'])
		parm4 = int(prediction['pred_sCON'])
		parm5 = int(prediction['pred_sEXT'])
		parm6 = int(prediction['pred_sEXT'])
		parm7 = int(prediction['pred_sNEU'])

		prediction = model.predict([[parm1, parm2, parm3, parm4,parm5, parm6, parm7]])[0]

		print("________________________________________________",prediction)



		q = "SELECT SUM(mark_awarded) FROM `answer` WHERE user_id='%s'" % (uid)
		
		res = select(q)
		point = res[0]['SUM(mark_awarded)']
		# q="SELECT * FROM answer WHERE user_id='%s'"%(logid)
		# print(q)
		# res=select(q)
		# point=res[0]['mark_awarded']
		if point:
			q = "INSERT INTO application VALUES (null,'%s',curdate(),'%s','%s','%s','%s','%s','applied')" % (
			uid, path, prediction, point,jid,cid)
			insert(q)
			data['status'] ="success"

		else:
			q = "INSERT INTO application VALUES (null,'%s',curdate(),'%s','%s',0,'%s','%s','applied')" % (
			uid, path, prediction,jid,cid)
			insert(q)

	

		# # p=request.form['p']
		# q="insert into application values (null,'%s',curdate(),'%s','%s','%s','%s','%s','pending')"%(uid,path,prediction,point,jid,cid)
		# insert(q)
			data['status'] ="success"
	data['method']="upload_pdf"

	return str(data)




