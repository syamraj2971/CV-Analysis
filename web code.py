from flask import *
from DBConnection import *
from werkzeug.utils import secure_filename
import os
import uuid
from sample import *
appp = Flask(__name__,template_folder="template")
appp.secret_key="dfgdf"

import functools
from core import *

def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "lid" not in session:
            return render_template('index.html')
        return func()

    return secure_function


@appp.route('/')
def log():
    return render_template('index.html')



@appp.route('/login',methods=['post'])
def login():
    username=request.form['textfield']
    password=request.form['textfield2']

    qry="select * from login where username=%s and password=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return'''<script>alert("invalid");
        window.location="/"</script>'''
    elif res['type']=='admin':
        session['lid']=res['id']
        return '''<script>alert("valid");
               window.location="/admin_home"</script>'''

    elif res['type']=='staff':
        session['lid'] = res['id']
        return '''<script>alert("valid");
               window.location="/staff_home"</script>'''
    else:
        return '''<script>alert("invalid");
               window.location="/"</script>'''



@appp.route('/logout',methods=['get','post'])
def logout():
    session.clear()
    return render_template("index.html")


@appp.route('/admin_home')
@login_required
def admin_home():
    return render_template("aindex.html")

@appp.route('/staff_home')
@login_required
def staff_home():
    return render_template("staff/sindex.html")


@appp.route('/manage_timetable')
@login_required
def manage_timetable():
    q="SELECT `timetable`.*,`exam`.`exam` FROM `exam` JOIN `timetable` ON `timetable`.`exam_id`=`exam`.`id`"
    res=selectall(q)
    return render_template("add and manage timetable.html",val=res)


@appp.route('/delete_timetable')
@login_required
def delete_timetable():
    id=request.args.get('id')
    q="DELETE FROM `timetable` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_timetable"</script>'''


@appp.route('/staff',methods=['post'])
@login_required
def staff():
    return render_template("add staff.html")

@appp.route('/hall',methods=['post'])
@login_required
def hall():
    return render_template("add hall.html")

@appp.route('/add')
@login_required
def add():
    return render_template("add.html")

@appp.route('/allocation')
@login_required
def allocation():
    return render_template("add allocation.html")

@appp.route('/manage_course')
@login_required
def manage_course():
    qry = "select * from course"
    res = selectall(qry)
    return render_template("add and manage course.html",val = res)


@appp.route('/delete_course')
@login_required
def delete_course():
    id=request.args.get('id')
    q="DELETE FROM `course` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_course"</script>'''



@appp.route('/manage_examdetails')
@login_required
def manage_examdetails():
    qry = "SELECT `exam`.*,`course`.`course` FROM `course` JOIN `exam` ON `exam`.`course_id`=`course`.`id`"
    res = selectall(qry)
    return render_template("add and manage exam details.html",val=res)




@appp.route('/delete_examdetails')
@login_required
def delete_examdetails():
    id=request.args.get('id')
    q="DELETE FROM `exam` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_examdetails"</script>'''



@appp.route('/manage_hall')
@login_required
def manage_hall():
    qry = "select *from hall"
    res = selectall(qry)
    return render_template("add and manage hall.html",val = res)

@appp.route('/manage_staff')
@login_required
def manage_staff():
    qry = "select *from staff"
    res = selectall(qry)
    return render_template("add and manage staff.html",val=res)


@appp.route('/addhall',methods=['post'])
@login_required
def addhall():
    hallno=request.form['textfield']
    details=request.form['textfield2']
    q="INSERT INTO `hall` VALUES(NULL,%s,%s)"
    v=(hallno,details)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_hall"</script>'''





@appp.route('/addstaff',methods=['post'])
@login_required
def addstaff():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gender=request.form['radiobutton']
    dob=request.form['textfield3']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    phone=request.form['textfield7']
    email=request.form['textfield8']
    uname=request.form['textfield9']
    pswd=request.form['textfield10']
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'staff')"
    val=(uname,pswd)
    id=iud(qry,val)
    q="INSERT INTO `staff` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    v=(str(id),fname,lname,gender,dob,place,post,pin,phone,email)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_staff"</script>'''



@appp.route('/editstaff')
@login_required
def editstaff():
    id=request.args.get('id')
    session['estid']=id
    q="SELECT * FROM `staff` WHERE `login_id`=%s"
    res=selectone(q,str(id))
    return render_template("editstaff.html",val=res)





@appp.route('/editstaff1',methods=['post'])
@login_required
def editstaff1():
    fname=request.form['textfield']
    lname=request.form['textfield2']
    gender=request.form['radiobutton']
    dob=request.form['textfield3']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    phone=request.form['textfield7']
    email=request.form['textfield8']
    q="update `staff` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`dob`=%s,`place`=%s,`post`=%s,`pin`=%s,`phone`=%s,`email`=%s WHERE `login_id`=%s"
    v=(fname,lname,gender,dob,place,post,pin,phone,email,session['estid'])
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_staff"</script>'''



@appp.route('/delete_staff')
@login_required
def delete_staff():
    id=request.args.get('id')
    q="DELETE FROM `login` WHERE `id`=%s"
    iud(q,str(id))

    q = "DELETE FROM `staff` WHERE `login_id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/manage_staff"</script>'''




@appp.route('/manage_subject')
@login_required
def manage_subject():
    qry = "SELECT `subject`.*,`course`.`course` FROM `course` JOIN `subject` ON `course`.`id`=`subject`.`course_id`"
    res = selectall(qry)
    return render_template("add and manage subject.html",val=res)

@appp.route('/delete_subject')
@login_required
def delete_subject():
    id=request.args.get('id')
    q="DELETE FROM `subject` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_subject"</script>'''



@appp.route('/delete_hall')
@login_required
def delete_hall():
    id=request.args.get('id')
    q="DELETE FROM `hall` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/manage_hall"</script>'''


@appp.route('/course',methods=['post'])
@login_required
def course():
    return render_template("add course.html")

@appp.route('/addcourse',methods=['post'])
@login_required
def addcourse():
    course=request.form['textfield']
    details=request.form['textfield2']
    q="INSERT INTO `course` VALUES(NULL,%s,%s)"
    v=(course,details)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_course"</script>'''



@appp.route('/editcourse')
@login_required
def editcourse():
    id=request.args.get('id')
    session['ecid']=id
    q="SELECT* FROM `course` WHERE `id`=%s"
    res=selectone(q,str(id))
    return render_template("editcourse.html",val=res)

@appp.route('/editcourse1',methods=['post'])
@login_required
def editcourse1():
    course=request.form['textfield']
    details=request.form['textfield2']
    q="update course SET `course`=%s,`details`=%s WHERE `id`=%s"
    v=(course,details,session['ecid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_course"</script>'''





@appp.route('/subject',methods=['post'])
@login_required
def subject():
    q="SELECT * FROM `course`"
    res=selectall(q)
    return render_template("add subject.html",val=res)

@appp.route('/addsubject',methods=['post'])
@login_required
def addsubject():
    sem=request.form['select']
    course=request.form['select2']
    sub=request.form['textfield']
    q="INSERT INTO `subject` VALUES(NULL,%s,%s,%s)"
    v=(course,sub,sem)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_subject"</script>'''


@appp.route('/editsubject')
@login_required
def editsubject():
    id = request.args.get('id')
    session['esid'] = id
    q = "SELECT* FROM `subject` WHERE `id`=%s"
    res1 = selectone(q, str(id))
    q="SELECT * FROM `course`"
    res=selectall(q)
    return render_template("editsubject.html",val=res,val1=res1)

@appp.route('/editsubject1',methods=['post'])
@login_required
def editsubject1():
    sem=request.form['select']
    course=request.form['select2']
    sub=request.form['textfield']
    q="UPDATE `subject` SET `course_id`=%s,`subject`=%s,`sem`=%s WHERE `id`=%s"
    v=(course,sub,sem,session['esid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_subject"</script>'''




@appp.route('/timetable',methods=['post'])
@login_required
def timetable():
    q = "SELECT * FROM `exam`"
    res = selectall(q)
    return render_template("add timetable.html",val=res)

@appp.route('/addtimetable',methods=['post'])
@login_required
def addtimetable():
    eid=request.form['select']
    timetable=request.files['file']
    tim=secure_filename(timetable.filename)
    timetable.save(os.path.join('static/timetable',tim))
    q=" INSERT INTO `timetable` VALUES(NULL,%s,%s,CURDATE())"
    v=(tim,eid)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_timetable"</script>'''



@appp.route('/allocate_examhall',methods=['post'])
@login_required
def allocate_examhall():
    q = "SELECT * FROM `exam`"
    res = selectall(q)
    q1 = "SELECT * FROM `hall`"
    r = selectall(q1)
    return render_template("allocate exam hall.html",val=res,v=r)


@appp.route('/allocate_examhall1',methods=['post'])
@login_required
def allocate_examhall1():
    exm=request.form['select']
    hall=request.form['select2']
    qry="SELECT * FROM `examhall_allocation` WHERE `exam_id`=%s"
    res=selectone(qry,exm)
    if res is None:

        q="INSERT INTO `examhall_allocation` VALUES(NULL,%s,%s)"
        v=(exm,hall)
        iud(q,v)
        return '''<script>alert("allocated");window.location="/allocation_exam"</script>'''
    else:
        return '''<script>alert("already allocated");window.location="/allocation_exam"</script>'''




@appp.route('/allocate_staff',methods=['post'])
@login_required
def allocate_staff():
    q="SELECT * FROM `staff`"
    res=selectall(q)
    q1="SELECT * FROM `subject`"
    r=selectall(q1)
    return render_template("allocate staff.html",val=res,v=r)

@appp.route('/allocatesub',methods=['post'])
@login_required
def allocatesub():
    stid=request.form['select']
    sub=request.form['select2']
    qry="SELECT * FROM `assign_sub` WHERE `staff_id`=%s AND `subject_id`=%s"
    va=(stid,sub)
    res=selectone(qry,va)
    if res is None:
        q="INSERT INTO `assign_sub` VALUES(NULL,%s,%s)"
        v=(stid,sub)
        iud(q,v)
        return '''<script>alert("allocated");window.location="/allocate_subject"</script>'''

    else:
        return '''<script>alert(" already allocated");window.location="/allocate_subject"</script>'''


@appp.route('/allocate_subject')
@login_required
def allocate_subject():
    q="SELECT `subject`.`subject`,`staff`.`first_name`,`last_name`,`assign_sub`.* FROM `staff` JOIN `assign_sub` ON `assign_sub`.`staff_id`=`staff`.`login_id` JOIN `subject` ON `subject`.`id`=`assign_sub`.`subject_id`"
    res=selectall(q)
    return render_template("allocate subject for staff.html",val=res)


@appp.route('/deleteallocation')
@login_required
def deleteallocation():
    id=request.args.get('id')
    q="DELETE FROM `assign_sub` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/allocate_subject"</script>'''



@appp.route('/exam_details',methods=['post'])
@login_required
def exam_details():
    q = "SELECT * FROM `course`"
    res = selectall(q)
    return render_template("exam details.html",val=res)

@appp.route('/addexam_details',methods=['post'])
@login_required
def addexam_details():
    cid=request.form['select']
    exm=request.form['textfield']
    det=request.form['textarea']
    date=request.form['textfield3']
    q="INSERT INTO `exam` VALUES(NULL,%s,%s,%s,%s)"
    v=(cid,exm,det,date)
    iud(q,v)
    return '''<script>alert("added");window.location="/manage_examdetails"</script>'''




@appp.route('/editexm_details')
@login_required
def editexm_details():
    id=request.args.get('id')
    session['exmid']=id
    qry="SELECT * FROM `exam` WHERE `id`=%s"
    res1=selectone(qry,str(id))
    q = "SELECT * FROM `course`"
    res = selectall(q)
    return render_template("editexamdetails.html",val=res,val1=res1)

@appp.route('/editexm_details1',methods=['post'])
@login_required
def editexm_details1():
    cid=request.form['select']
    exm=request.form['textfield']
    det=request.form['textarea']
    date=request.form['textfield3']
    q="UPDATE `exam` SET `course_id`=%s,`exam`=%s,`details`=%s,`date`=%s WHERE `id`=%s"
    v=(cid,exm,det,date,session['exmid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/manage_examdetails"</script>'''





@appp.route('/hall_to_staff',methods=['post'])
@login_required
def hall_to_staff():
    q = "SELECT * FROM `staff`"
    res = selectall(q)
    qry="SELECT `examhall_allocation`.*,`exam`.`exam`,`hall`.`hall_no` FROM `examhall_allocation` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id`"
    r=selectall(qry)
    return render_template("assign hall to staff.html",v=r,val=res)

@appp.route('/hall_to_staff1',methods=['post'])
@login_required
def hall_to_staff1():
    sid=request.form['select']
    allid=request.form['select2']
    q="INSERT INTO `hall allocation to staff` VALUES(NULL,%s,%s)"
    v=(allid,sid)
    iud(q,v)
    return '''<script>alert("allocated");window.location="/hall_allocation_staff"</script>'''




@appp.route('/assign_duties',methods=['post'])
@login_required
def assign_duties():
    q="SELECT * FROM `staff`"
    res=selectall(q)
    return render_template("assign duties.html",val=res)

@appp.route('/assign_duty',methods=['post'])
@login_required
def assign_duty():
    staff=request.form['select']
    duty=request.form['textfield']
    q="INSERT INTO `assign_duties` VALUES(NULL,%s,%s,CURDATE(),'pending')"
    v=(staff,duty)
    iud(q,v)
    return '''<script>alert("assigned");window.location="/assign_duties_to_staff"</script>'''



@appp.route('/assign_duties_to_staff')
@login_required
def assign_duties_to_staff():
    q="SELECT `assign_duties`.*,`staff`.`first_name`,`last_name` FROM `staff` JOIN `assign_duties` ON `assign_duties`.`staff_id`=`staff`.`login_id`"
    res=selectall(q)
    return render_template("assign duties to staff.html",val=res)

@appp.route('/hall_allocation_staff')
@login_required
def hall_allocation_staff():
    q="SELECT `hall allocation to staff`.*,`exam`.`exam`,`hall`.`hall_no`,`staff`.`first_name`,`last_name` FROM `exam` JOIN `examhall_allocation` ON `examhall_allocation`.`exam_id`=`exam`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id` JOIN `hall allocation to staff` ON `hall allocation to staff`.`examhall_id`=`examhall_allocation`.`id` JOIN `staff` ON `staff`.`login_id`=`hall allocation to staff`.`staff_id`"
    res=selectall(q)
    return render_template("hall allocation to staff.html",val=res)


@appp.route('/dltallocation')
@login_required
def dltallocation():
    id=request.args.get('id')
    q="DELETE FROM `hall allocation to staff` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/hall_allocation_staff"</script>'''


@appp.route('/allocation_exam')
@login_required
def allocation_exam():
    q="SELECT `examhall_allocation`.*,`exam`.`exam`,`hall`.`hall_no` FROM `examhall_allocation` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id`"
    res=selectall(q)
    return render_template("hall allocaton to exam.html",val=res)



@appp.route('/dltallocation_exam')
@login_required
def dltallocation_exam():
    id=request.args.get('id')
    q="DELETE FROM `examhall_allocation` WHERE `id`=%s"
    iud(q,str(id))
    return '''<script>alert("deleted");window.location="/hall_allocation_staff"</script>'''



###############################staff##########################

@appp.route('/managestudent')
@login_required
def managestudent():
    q="SELECT `student`.*,`course`.`course` FROM `student` JOIN `course` ON `course`.`id`=`student`.`course_id`"
    res=selectall(q)

    return render_template("staff/add&manage student.html",v=res)






@appp.route('/addstudent',methods=['post'])
@login_required
def addstudent():
    q="SELECT* FROM `course` "
    res=selectall(q)
    return render_template("staff/add student.html",v=res)


@appp.route('/addstudent1',methods=['post'])
@login_required
def addstudent1():
    FirstName = request.form['textfield']
    LastName = request.form['textfield2']
    Gender = request.form['RadioGroup1']
    Dob = request.form['textfield3']
    Place = request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']
    un = request.form['textfield9']
    pwd = request.form['textfield10']
    crs = request.form['select']
    sem = request.form['select2']
    qry="INSERT INTO `login` VALUES(NULL,%s,%s,'student')"
    val=(un,pwd)
    id=iud(qry,val)
    q="INSERT INTO `student` VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    v=(str(id),FirstName,LastName,Gender,Dob,Place,Post,Pin,crs,sem,Phone,Email)
    pid=str(iud(q,v))
    isFile = os.path.isdir("static/trainimages/"+pid)  
    print(isFile)
    if(isFile==False):
        os.mkdir('static/trainimages/'+pid)
    image1=request.files['img1']
    path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image1.filename
    image1.save(path)

    image2=request.files['img2']
    path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image2.filename
    image2.save(path)

    image3=request.files['img3']
    path="static/trainimages/"+pid+"/"+str(uuid.uuid4())+image3.filename
    image3.save(path)
    enf("static/trainimages/")
    return '''<script>alert("added");window.location="/addstudent1"</script>'''



@appp.route('/mngnotes')
@login_required
def mngnotes():
    q="SELECT `notes`.*,`subject`.`subject` FROM `subject` JOIN `notes` ON `notes`.`subject_id`=`subject`.`id`"
    res=selectall(q)
    return render_template("staff/add & manage notes.html",val=res)


@appp.route('/addnotes',methods=['post'])
@login_required
def addnotes():
    q="SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res=selectall2(q,session['lid'])
    print(res)
    return render_template("staff/add notes.html",val=res)

@appp.route('/addnotes1',methods=['post'])
@login_required
def addnotes1():
    sub=request.form['select']
    note=request.files['file']
    n=secure_filename(note.filename)
    note.save(os.path.join('static/notes',n))
    q="INSERT INTO `notes` VALUES(NULL,%s,%s)"
    v=(sub,n)
    iud(q,v)
    return '''<script>alert("added");window.location="/mngnotes"</script>'''




@appp.route('/mngqnpaper')
@login_required
def mngqnpaper():
    q="SELECT `questionpaper`.*,`subject`.`subject` FROM `subject` JOIN `questionpaper` ON `questionpaper`.`subjet_id`=`subject`.`id`"
    res=selectall(q)
    return render_template("staff/add & manage qstn paper.html",val=res)


@appp.route('/addqnpaper',methods=['post'])
@login_required
def addqnpaper():
    q="SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res=selectall2(q,session['lid'])
    print(res)
    return render_template("staff/add qstn paper.html",val=res)

@appp.route('/addqnpaper1',methods=['post'])
@login_required
def addqnpaper1():
    sub=request.form['select']
    note=request.files['file']
    n=secure_filename(note.filename)
    note.save(os.path.join('static/question',n))
    q="INSERT INTO `questionpaper` VALUES(NULL,%s,%s)"
    v=(n,sub)
    iud(q,v)
    return '''<script>alert("added");window.location="/mngqnpaper"</script>'''

@appp.route('/viewallocatedsub')
@login_required
def viewallocatedsub():
    q = "SELECT `subject`.* FROM `subject` JOIN `assign_sub` ON `assign_sub`.`subject_id`=`subject`.`id` WHERE `assign_sub`.`staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view allocated subject.html",val=res)




@appp.route('/viewassignedworks')
@login_required
def viewassignedworks():
    q = "SELECT * FROM `assign_duties` WHERE `staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view assigned works.html",val=res)


@appp.route('/updatestts')
@login_required
def updatestts():
    id=request.args.get('id')
    session['duid']=id
    return render_template("staff/status.html")

@appp.route('/updatestts1',methods=['post'])
@login_required
def updatestts1():
    stts=request.form['ss']
    q="UPDATE `assign_duties` SET `status`=%s WHERE `id`=%s"
    v=(stts,session['duid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/viewassignedworks"</script>'''




@appp.route('/viewallocatedhall')
@login_required
def viewallocatedhall():
    q = "SELECT `hall allocation to staff`.*,`exam`.`exam`,`hall`.`hall_no` FROM `hall allocation to staff` JOIN `examhall_allocation` ON `examhall_allocation`.`id`=`hall allocation to staff`.`examhall_id` JOIN `exam` ON `exam`.`id`=`examhall_allocation`.`exam_id` JOIN `hall` ON `hall`.`id`=`examhall_allocation`.`hall_id` WHERE `hall allocation to staff`.`staff_id`=%s"
    res = selectall2(q, session['lid'])
    print(res)
    return render_template("staff/view allocated hall.html",val=res)

@appp.route('/dltstudent')
@login_required
def dltstudent():
    id=request.args.get('id')
    q="DELETE FROM `login` WHERE `id`=%s"
    iud(q,str(id))
    qry="DELETE FROM `student` WHERE `login_id`=%s"
    iud(qry,str(id))
    return '''<script>alert("deleted");window.location="/managestudent"</script>'''

@appp.route('/dltnote')
@login_required
def dltnote():
    id = request.args.get('id')
    q = "DELETE FROM `notes` WHERE `id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/mngnotes"</script>'''


@appp.route('/dltquestion')
@login_required
def dltquestion():
    id = request.args.get('id')
    q = "DELETE FROM `questionpaper` WHERE `id`=%s"
    iud(q, str(id))
    return '''<script>alert("deleted");window.location="/mngqnpaper"</script>'''



@appp.route('/viewmalpractice')
@login_required
def viewmalpractice():
    qry="SELECT `malpractice`.*,`hall`.`hall_no` FROM `malpractice` JOIN `hall` ON `hall`.`id`=`malpractice`.`hallid`"
    res=selectall(qry)
    print(res)
    return render_template("staff/viewmalpractice.html",val=res)


@appp.route('/viewmalpractice1')
@login_required
def viewmalpractice1():
    qry="SELECT `malpractice`.*,`hall`.`hall_no` FROM `malpractice` JOIN `hall` ON `hall`.`id`=`malpractice`.`hallid`"
    res=selectall(qry)
    return render_template("viewmalpractice.html",val=res)



@appp.route('/editstudent')
@login_required
def editstudent():
    id=request.args.get('id')
    session['studid']=id
    qry="SELECT * FROM `student` WHERE `login_id`=%s"
    res1=selectone(qry,str(id))
    q1="SELECT * FROM `course`"
    res=selectall(q1)
    print(res)
    return render_template("staff/edit_student.html",val2=selectall(q1),v=res1)


@appp.route('/editstudent1',methods=['post'])
@login_required
def editstudent1():
    FirstName = request.form['textfield']
    LastName = request.form['textfield2']
    Gender = request.form['RadioGroup1']
    Dob = request.form['textfield3']
    Place = request.form['textfield4']
    Post = request.form['textfield5']
    Pin = request.form['textfield6']
    Phone = request.form['textfield7']
    Email = request.form['textfield8']
    crs = request.form['select']
    sem = request.form['select2']


    q="update `student` SET `first_name`=%s,`last_name`=%s,`gender`=%s,`dob`=%s,`place`=%s,`post`=%s,`pin`=%s,`course_id`=%s,`sem`=%s,`phone`=%s,`email`=%s WHERE `login_id`=%s"
    v=(FirstName,LastName,Gender,Dob,Place,Post,Pin,crs,sem,Phone,Email,session['studid'])
    iud(q,v)
    return '''<script>alert("updated");window.location="/managestudent"</script>'''




# @appp.route("/camera")
# def camera():
#     # id1=request.args['id1']
#     from em import camclick
#     q=rec_face_image()
#     print(q)
#     session['r3']=q
#     return redirect(url_for('staff.camera'))



@appp.route('/startclass')
@login_required
def startclass():
    id=request.args['id']
    val=detection(id)
    return '''<script>window.location="/staff_home"</script>'''



    




appp.run(debug=True,port=5080)







