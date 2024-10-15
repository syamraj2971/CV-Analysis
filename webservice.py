from flask import *
from DBConnection import *
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)


@app.route('/login_post',methods=['post'])
def login():
    username=request.form['uname']
    password=request.form['pswd']

    qry="select * from login where username=%s and password=%s and type='student'"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return jsonify({"task":"invalid"})
    else:

        return jsonify({"task":"valid","lid":res['id']})


@app.route('/viewsubjects',methods=['post'])
def viewsubjects():
    lid=request.form['lid']
    qry="SELECT `course_id` FROM `student` WHERE `login_id`=%s"
    res=selectone(qry,lid)
    print(res)
    q="SELECT * FROM `subject` WHERE `course_id`=%s"
    cid=res['course_id']
    r=selectall2(q,cid)
    print(r)
    return jsonify(r)

@app.route('/viewnotes',methods=['post'])
def viewnotes():
    sid=request.form['sid']
    q="SELECT * FROM `notes` WHERE `subject_id`=%s"
    res=selectall2(q,sid)
    return jsonify(res)


@app.route('/viewqnpapers',methods=['post'])
def viewqnpapers():
    sid = request.form['sid']
    q = "SELECT *FROM `questionpaper` WHERE `subjet_id`=%s"
    res = selectall2(q, sid)
    return jsonify(res)


@app.route('/viewexamdetails',methods=['post'])
def viewexamdetails():
    q="SELECT `exam`.*,`course`.`course`,`timetable`.`timetable` FROM `exam` JOIN `course` ON `course`.`id`=`exam`.`course_id` JOIN `timetable` ON `timetable`.`exam_id`=`exam`.`id`"
    res=selectall(q)
    return jsonify(res)















app.run(host='0.0.0.0',port=5000)



