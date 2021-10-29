# Might change this to using os.environ.get() instead in future sprints
from decouple import config
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
from datetime import datetime

# Database connection

# EC2 DB port is 3306 instead, change accordingly.
app = Flask(__name__)
# EC2 DB port is 3306 instead, change accordingly.
app.config['SQLALCHEMY_DATABASE_URI'] = config('dbURL') or environ.get("dbURL")
# app.config['SQLALCHEMY_DATABASE_URI'] = config('localURL') or environ.get('localURL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Employee(db.Model):
    __tablename__ = "employee"
    emp_id = db.Column(db.String(10),primary_key=True, nullable=False)
    emp_name = db.Column(db.String(50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }

    def json(self):
        employee_info = {
            'emp_id': self.emp_id,
            'emp_name': self.emp_name
        }
        return employee_info
    
    # def getName(self):
    #     return self.emp_name
    
    # def getEmpId(self):
    #     return self.emp_id

class Senior_Engineer(Employee):
    __tablename__ = "senior_engineer"
    emp_id =  db.Column(db.String(10), db.ForeignKey('employee.emp_id'),primary_key=True, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'senior_engineer',
    }
    
class Engineer(Employee):
    __tablename__ = "engineer"
    emp_id =  db.Column(db.String(10), db.ForeignKey('employee.emp_id'),primary_key=True, nullable=False)


    __mapper_args__ = {
        'polymorphic_identity': 'engineer',
    }

class Trainer(db.Model):
    __tablename__ = "trainer"
    emp_id =  db.Column(db.String(10), db.ForeignKey('employee.emp_id'), nullable=False)
    trainer_id =  db.Column(db.String(10), primary_key=True, nullable=False)



class Learner(db.Model):
    __tablename__ = "learner"
    emp_id =  db.Column(db.String(10), db.ForeignKey('employee.emp_id'), nullable=False)
    learner_id =  db.Column(db.String(10), primary_key=True, nullable=False)

    # def getEmpId(self):
    #     return self.emp_id


class Completion_Record(db.Model):
    __tablename__ = "completion_record"
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"),primary_key=True, nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255), nullable=False)
    prerequisite = db.Column(db.Integer, nullable=False)

    def json(self):
        Course_info = {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'course_desc': self.course_desc,
            'prerequisite': self.prerequisite
        }
        return Course_info

    # def getCourseName(self):
    #     return self.course_name
    
    # def getCourseDesc(self):
    #     return self.course_name
        
    # def getPrerequisite(self):
    #     return self.prerequisite
    
    # def getCourseId(self):
    #     return self.course_id



class Course_Prerequisite(db.Model):
    __tablename__ = "course_prerequisite"
    course_id = db.Column(db.String(10),primary_key=True, nullable=False)
    prereq_course_id = db.Column(db.String(10),primary_key=True, nullable=False)


class Class_Run(db.Model):
    __tablename__ = "class_run"

    # Assuming class_id contains information of the course itself, thus it can be a singular primary key (Important, let team know.)
    class_id = db.Column(db.String(10), primary_key=True)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), primary_key=True, nullable=False)
    class_start_date = db.Column(db.String(50),nullable=False)
    class_end_date = db.Column(db.String(50),nullable=False)
    reg_start_date = db.Column(db.String(50),nullable=False)
    reg_end_date = db.Column(db.String(50),nullable=False)

    # Just slots available is enough, don't need class_size.
    slots_available = db.Column(db.Integer, nullable=False)


    def check_available_end_date(self):
        now = datetime.now()
        ## double check
        dt_string = now.strftime("%Y-%m-%d")
        if(dt_string <= self.reg_end_date):
            return True
        return False

    def check_available_date(self):
        now = datetime.now()
        ## double check
        dt_string = now.strftime("%Y-%m-%d")
        if(self.reg_start_date <= dt_string <= self.reg_end_date):
            return True
        return False
    
    def compute_total_slot_available(self,total_slot_available):
        return total_slot_available + self.slots_available

    
    def compute_slot_available(self,string):
        if(string == "Assign"):
            self.slots_available = self.slots_available- 1
        elif(string == "Withdraw"):
            self.slots_available = self.slots_available + 1
        #return self.slots_available


    def json(self):
        class_run_info = {
            'class_id': self.class_id,
            'course_id': self.course_id,
            'class_start_date': self.class_start_date,
            'class_end_date': self.class_end_date,
            'reg_start_date': self.reg_start_date,
            'reg_end_date': self.reg_end_date
        }
        return class_run_info

class Trainer_Record(db.Model):
    __tablename__ = "trainer_record"
    class_id = db.Column(db.String(10), db.ForeignKey("class_run.class_id"),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), nullable=False)
    trainer_id =  db.Column(db.String(10), db.ForeignKey('trainer.trainer_id'), primary_key=True, nullable=False)



class Class_Record(db.Model):
    __tablename__ = "class_record"
    class_id = db.Column(db.String(10), db.ForeignKey("class_run.class_id"),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)

# class Registration(db.Model):
#     __tablename__ = "registration"
#     class_id = db.Column(db.String(10), db.ForeignKey("class_run.class_id"),primary_key=True, nullable=False)
#     course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), nullable=False)
#     learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
#     reg_date = db.Column(db.String(50),nullable=False)


#     # Why must this be inside Reg class? Mmmm...
#     def get_current_date():
#         now = datetime.now()
#         current_date = now.strftime("%Y-%m-%d")
#         print(current_date)
#         return current_date

    # def getClassId(self):
    #     return self.class_id
    
    # def getCourseId(self):
    #     return self.course_id
    # def getLearnerId(self):
    #     return self.learner_id
    # def getRegDate(self):
    #     return self.reg_date



# db.create_all()

class Registration(db.Model):
    __tablename__ = "registration"
    class_id = db.Column(db.String(10), db.ForeignKey("class_run.class_id"),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
    reg_date = db.Column(db.String(50),nullable=False)


    # Why must this be inside Reg class? Mmmm...
    def get_current_date():
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        print(current_date)
        return current_date

class Chapter(db.Model): 
    __tablename__ = "chapter" 
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"),primary_key=True, nullable=False)
    chapter_id = db.Column(db.String(30), primary_key=True, nullable=False)

    def json(self):
        chapter_info = {
            'course_id': self.course_id,
            'chapter_id': self.chapter_id
        }
        return chapter_info
    

class Chapter_Learner(db.Model):
    __tablename__ = "chapter_learner"
    # chapter_id = db.Column(db.String(10), db.ForeignKey("chapter.chapter_id"), primary_key=True, nullable=False)
    chapter_id = db.Column(db.String(30), primary_key=True, nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
    completion = db.Column(db.Integer, nullable=False)

    def update_completion(self):
        self.completion = 1

    def json(self):
        info = {
            'chapter_id': self.chapter_id,
            'learner_id': self.learner_id,
            'completion': self.completion
        }

        return info

class Quiz(db.Model):
    __tablename__ = "quiz"
    quiz_id = db.Column(db.String(30), primary_key=True, nullable=False)
    timing = db.Column(db.String(50),nullable=False)

class Chapter_Quiz(Quiz):
    __tablename__ = "chapter_quiz"
    quiz_id = db.Column(db.String(30), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
    # Need to fix this - Somehow the chapter_id is not able to be referenced - Darren 24/10
    # chapter_id = db.Column(db.String(10), db.ForeignKey("chapter.chapter_id"), primary_key=True, nullable=False)
    chapter_id = db.Column(db.String(30), primary_key=True, nullable=False)
    total_marks = db.Column(db.String(10), nullable=False)

    def check_pass(self,learner_marks):
        is_pass = 1
        percentage = (int(learner_marks) / int(self.total_marks)) * 100
        if(percentage >= 50):
            return is_pass
        is_pass = 0
        return is_pass


class Final_Quiz(Quiz): 
    __tablename__ = "final_quiz"
    quiz_id = db.Column(db.String(30), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"),primary_key=True, nullable=False)
    total_marks = db.Column(db.String(10), nullable=False)

class Question(db.Model):
    __tablename__ = "question"
    quiz_id = db.Column(db.String(30), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
    question_id = db.Column(db.String(10), primary_key=True, nullable=False)
    question = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.String(10), nullable=False)
    option = db.Column(db.String(10000), nullable=False)
    question_mark = db.Column(db.String(10), nullable=False)
    answer = db.Column(db.String(255), nullable=False)

    def json(self):
        self.quiz_id = {
            'quiz_id': self.quiz_id,
            'question_id': self.question_id,
            'question': self.question,
            'question_type': self.question_type,
            'option': self.option,
            'question_mark': self.question_mark,
            'answer': self.answer
        }
        return self.quiz_id 

    def compute_marks(self,answer):
        if(self.answer ==answer):
            return int(self.question_mark)
        return 0 

# class Question_Option(db.Model):
#     __tablename__ = "question_option"
#     quiz_id = db.Column(db.String(10), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
#     option = db.Column(db.String(255), primary_key=True, nullable=False)

class Chapter_Quiz_Result(db.Model): 
    __tablename__ = "chapter_quiz_result"
    quiz_id = db.Column(db.String(30), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
    marks = db.Column(db.String(10), nullable=False)

    def update_mark_existing_chapter_quiz_result(self, learner_marks):
        self.marks = learner_marks


class Final_Quiz_Result(db.Model):
    __tablename__ = "final_quiz_result"
    quiz_id = db.Column(db.String(30), db.ForeignKey("quiz.quiz_id"), primary_key=True, nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
    marks = db.Column(db.String(10), nullable=False)