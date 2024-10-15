/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - personality_prediction_new
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`personality_prediction_new` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `personality_prediction_new`;

/*Table structure for table `answer` */

DROP TABLE IF EXISTS `answer`;

CREATE TABLE `answer` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `test_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `mark_awarded` varchar(50) DEFAULT NULL,
  `grand_total` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `answer` */

insert  into `answer`(`answer_id`,`test_type_id`,`user_id`,`mark_awarded`,`grand_total`,`date`,`company_id`) values 
(1,1,1,'1','2','2023-12-15',1);

/*Table structure for table `answers` */

DROP TABLE IF EXISTS `answers`;

CREATE TABLE `answers` (
  `answer_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `mark` int(11) DEFAULT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `answers` */

/*Table structure for table `application` */

DROP TABLE IF EXISTS `application`;

CREATE TABLE `application` (
  `application_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `resume_path` varchar(500) DEFAULT NULL,
  `personality` varchar(100) DEFAULT NULL,
  `mark` varchar(50) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  `status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`application_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `application` */

insert  into `application`(`application_id`,`user_id`,`date`,`resume_path`,`personality`,`mark`,`job_id`,`company_id`,`status`) values 
(1,1,'2023-12-19','static/uploads/71126aa2-9882-4258-a66c-d42dbd11e844abc.pdf','lively','1.0',2,1,'applied');

/*Table structure for table `company` */

DROP TABLE IF EXISTS `company`;

CREATE TABLE `company` (
  `company_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `company` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `image` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `company` */

insert  into `company`(`company_id`,`login_id`,`company`,`place`,`phone`,`email`,`image`) values 
(1,2,'riss','sss','0123456789','riss@Hhjrb','8769');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `complaint` varchar(100) NOT NULL,
  `reply` varchar(100) NOT NULL,
  `date` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`complaint_id`,`user_id`,`user_type`,`complaint`,`reply`,`date`) values 
(1,2,'company','hiii','pending','2023-12-13'),
(2,1,'user','tygg','pending','2023-12-16'),
(3,1,'user','hiii','pending','2023-12-19'),
(4,1,'user','chfu','pending','2023-12-19');

/*Table structure for table `job` */

DROP TABLE IF EXISTS `job`;

CREATE TABLE `job` (
  `job_id` int(11) NOT NULL AUTO_INCREMENT,
  `company_id` int(11) DEFAULT NULL,
  `job` varchar(100) DEFAULT NULL,
  `details` varchar(100) DEFAULT NULL,
  `last_date` varchar(100) DEFAULT NULL,
  `requirements` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`job_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `job` */

insert  into `job`(`job_id`,`company_id`,`job`,`details`,`last_date`,`requirements`) values 
(1,1,'developer','jerj wjbrj3','2023-12-19','Team Leadership and Management, Data Analysis and Interpretation Project Management, Social Media and Digital Marketing, Microsoft Office Suite'),
(2,1,'testing','jijjoihjjh','2023-12-28','jjhjh hgtyf tyfyg'),
(3,1,'developer','lkj hhgkj','2023-12-31','jkh hyugyf vytygyu');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'jini','jini','user'),
(2,'riss','riss','company'),
(3,'admin','admin','admin'),
(4,'anu','anu','user'),
(5,'amu','amu','user');

/*Table structure for table `malpractice` */

DROP TABLE IF EXISTS `malpractice`;

CREATE TABLE `malpractice` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `time` varchar(200) DEFAULT NULL,
  `image` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=MyISAM AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

/*Data for the table `malpractice` */

insert  into `malpractice`(`mid`,`user_id`,`date`,`time`,`image`) values 
(1,1,'2023-12-13','15:23:09','20231213_152309.png'),
(2,1,'2023-12-14','11:30:22','20231214_113022.png'),
(3,1,'2023-12-14','11:30:22','20231214_113022.png'),
(4,1,'2023-12-14','11:47:19','20231214_114719.png'),
(5,1,'2023-12-14','11:47:22','20231214_114721.png'),
(6,1,'2023-12-14','11:50:42','20231214_115042.png'),
(7,1,'2023-12-14','11:50:44','20231214_115044.png'),
(8,1,'2023-12-14','12:14:02','20231214_121402.png'),
(9,1,'2023-12-14','12:16:14','20231214_121614.png'),
(10,1,'2023-12-14','12:16:16','20231214_121616.png'),
(11,1,'2023-12-14','12:16:20','20231214_121620.png'),
(12,1,'2023-12-15','14:14:41','20231215_141441.png'),
(13,1,'2023-12-15','14:14:43','20231215_141443.png'),
(14,1,'2023-12-15','14:14:45','20231215_141445.png'),
(15,1,'2023-12-15','14:14:47','20231215_141447.png');

/*Table structure for table `online_test` */

DROP TABLE IF EXISTS `online_test`;

CREATE TABLE `online_test` (
  `exam_id` int(11) NOT NULL AUTO_INCREMENT,
  `test_type_id` int(11) DEFAULT NULL,
  `question` varchar(50) DEFAULT NULL,
  `option1` varchar(50) DEFAULT NULL,
  `option2` varchar(50) DEFAULT NULL,
  `option3` varchar(50) DEFAULT NULL,
  `correct_option` varchar(50) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`exam_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `online_test` */

insert  into `online_test`(`exam_id`,`test_type_id`,`question`,`option1`,`option2`,`option3`,`correct_option`,`company_id`) values 
(1,1,'red fruit','apple','orange','grape','apple',1),
(2,1,'','','','','',1),
(3,1,'red fruit','gfd','ccxd','ds','ds',2),
(4,1,'acv','r','rrr','rr','r',2);

/*Table structure for table `questionanswer` */

DROP TABLE IF EXISTS `questionanswer`;

CREATE TABLE `questionanswer` (
  `qstansr_id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `answer` varchar(500) DEFAULT NULL,
  `mark` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`qstansr_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `questionanswer` */

/*Table structure for table `questions` */

DROP TABLE IF EXISTS `questions`;

CREATE TABLE `questions` (
  `question_id` int(50) NOT NULL AUTO_INCREMENT,
  `question` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`question_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `questions` */

/*Table structure for table `team` */

DROP TABLE IF EXISTS `team`;

CREATE TABLE `team` (
  `team_id` int(11) NOT NULL AUTO_INCREMENT,
  `team` varchar(100) DEFAULT NULL,
  `no_of_members` varchar(100) DEFAULT NULL,
  `skill` varchar(50) DEFAULT NULL,
  `company_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`team_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `team` */

/*Table structure for table `teammember` */

DROP TABLE IF EXISTS `teammember`;

CREATE TABLE `teammember` (
  `taemmember_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `team_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`taemmember_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `teammember` */

/*Table structure for table `test_type` */

DROP TABLE IF EXISTS `test_type`;

CREATE TABLE `test_type` (
  `test_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`test_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `test_type` */

insert  into `test_type`(`test_type_id`,`type`) values 
(1,'Aptitude'),
(2,'General');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `place` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`login_id`,`fname`,`lname`,`place`,`phone`,`email`) values 
(1,1,'jini','jini','tsr','2345678909','jini@gmail.com'),
(2,4,'anu','gvj','ghhgf','86568','ghfhv@jgu.hff'),
(3,5,'anu','anu','chcb','5955588886','chfhfuh');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
