from flask import *
from database import *
from sample import *

user=Blueprint('user',__name__)



@user.route('/userviewcompanies')
def userviewcompanies():
      
	data={}
	d="select * from company"
	res=select(d)
	data['view']=select(d)
	print("##################",res)
	return render_template('userviewcompanies.html',data=data)

@user.route('/user_view_tests')
def user_view_tests():
	data={}
	cid=request.args['cid']
	d="select * from test_type"
	data['view']=select(d)
	return render_template('user_view_tests.html',data=data,cid=cid)


# from sample import *
from em import *
from threading import Event
import threading

@user.route('/start_test',methods=['get','post'])
def start_test():
	import cv2
	import mediapipe as mp
	import numpy as np
	import threading
	cid=request.args['cid']
	tid=request.args['tid']
	data={}
	uid=session['id']
	s="select * from answer where test_type_id='%s' and user_id='%s'"%(tid,uid)
	res=select(s)
	if not res:
		# cid=request.args['cid']
		stop_camera_event.clear()
		camera_thread = threading.Thread(target=detection, args=(uid,cid,))
		camera_thread.start()
		d="select * from online_test where test_type_id='%s' and company_id='%s'"%(tid,cid)
		data['view']=select(d)
		if "submit" in request.form:
			stop_camera_event.set() 
			
			# camera_thread.join()
			# global camera_running
			# camera_running = False
			j=1
			a=0
			counter = 0
			for i in data['view']:
				counter += 1
				radio=request.form["ans"+str(j)]
				if i['correct_option']==radio:
					a=a+1
					
				j=j+1
			print(a,counter)
			print("^^^^^^^^^^^^^^^^^^^^^^^^mark^^^^^^",a)
			
			qry="insert into answer values(null,'%s','%s','%s','%s',curdate(),'%s')"%(tid,session['id'],a,counter,cid)
			session['ansid']=insert(qry)
			x="select * from application where user_id='%s' and company_id='%s'"%(uid,cid)
			xr=select(x)
			if xr:
				q = "SELECT SUM(mark_awarded) FROM `answer` WHERE user_id='%s'" % (session['id'])
				print(q)
				res = select(q)
				point = res[0]['SUM(mark_awarded)']
				u="update application set mark=mark+'%s' where user_id='%s' and company_id='%s'"%(point,uid,cid)
				update(u)
				
				
			
			return redirect(url_for('viewscore'))
		return render_template('start_test.html',data=data)
	else:
		# flash('You Already Taken The Test')
		return '''<script>alert("You Already Taken The Test");window.location='/userviewcompanies'</script>'''
		return redirect(url_for('userviewcompanies'))
	


