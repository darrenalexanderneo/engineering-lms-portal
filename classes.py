from decouple import config
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

# EC2 DB port is 3306 instead, change accordingly.
app = Flask(__name__)
# EC2 DB port is 3306 instead, change accordingly.
app.config['SQLALCHEMY_DATABASE_URI'] = config('dbURL') or environ.get("dbURL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)
class Role(db.Model):
    __tablename__ = "role"
    
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_desc = db.Column(db.String(50), nullable=False)

    def json(self):
        role_info = {
            'role_id': self.role_id,
            'role_desc': self.role_desc 
        }

        return role_info
    
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result


class Courses(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.String(10), primary_key=True)
    course_name = db.Column(db.String(50), nullable=False)
    course_desc = db.Column(db.String(255), nullable=False)
    prerequisite = db.Column(db.Integer, nullable=False)

    def json(self):
        course_info = {
            'course_id' : self.course_id,
            'course_name': self.course_name,
            'course_desc': self.course_desc,
            'prerequisite':self.prerequisite

        }

        return course_info

class Classes(db.Model):
    __tablename__ = "classes"
    class_id = db.Column(db.String(10), primary_key=True)
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    start_date = db.Column(db.String(50),nullable=False)
    end_date = db.Column(db.String(50),nullable=False)
    slots_available = db.Column(db.Integer, nullable=False)
    class_size = db.Column(db.Integer, nullable=False)

    def get_num_of_class(counter):
        counter+=1
        return counter
    
    def get_slot_available(slot_available,total):
        return total + slot_available

    def compute_slot_available(string,slot_available):
        if(string == "Assign"):
            updated_slot_available = slot_available- 1
        elif(string == "Withdraw"):
            updated_slot_available = slot_available + 1
        return updated_slot_available

    def json(self):
        classes_info = {
            'class_id' : self.class_id,
            'course_id': self.course_id,
            'start_date' : self.start_date,
            'end_date' :self.end_date,
            'slots_available': self.slots_available,
            'class_size': self.class_size
        }
        return classes_info


class Registration(db.Model):
    __tablename__ = "registration"
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    reg_start_date = db.Column(db.String(50), nullable=False)
    reg_end_date = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.String(10), primary_key=True, nullable=False)
    
    
    def json(self):
        registration_info = {
            'course_id' : self.course_id,
            'reg_start_date': self.reg_start_date,
            'reg_end_date' :self.reg_end_date,
            'class_id':self.class_id
        }
        return registration_info

class Course_Registration(db.Model):
    __tablename__ = "course_registration"
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    class_id = db.Column(db.String(10), primary_key=True, nullable=False)
    emp_id = db.Column(db.String(10),primary_key=True, nullable=False)
    pre_assigned = db.Column(db.Integer,nullable=False)
    
    def json(self):
        course_registration_info = {
            'course_id' : self.course_id,
            'class_id':self.class_id,
            'emp_id': self.emp_id,
            'pre_assigned' : self.pre_assigned
        }
        return course_registration_info


class Trainers_Course(db.Model):
    __tablename__ = "trainers_course"
    course_id = db.Column(db.String(10), primary_key=True, nullable=False)
    class_id = db.Column(db.String(10), primary_key=True, nullable=False)
    emp_id = db.Column(db.String(10), primary_key=True, nullable=False)
    
    def json(self):
        trainers_course_info = {
            'course_id' : self.course_id,
            'class_id':self.class_id,
            'emp_id': self.emp_id
        }
        return trainers_course_info

class Employee(db.Model):
    __tablename__ = "employee"
    emp_id = db.Column(db.String(10),primary_key=True, nullable=False)
    emp_name = db.Column(db.String(50), nullable=False)
    role_id = db.Column(db.String(50),nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'employee'
    }

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    # def json(self):
    #     employee_info = {
    #         'emp_id' : self.emp_id,
    #         'emp_name': self.emp_name,
    #         'role_id': self.role_id
  
    #     }
    #     return employee_info


class Course_Prerequisite(db.Model):
    __tablename__ = "course_prerequisite"
    course_id = db.Column(db.String(10),primary_key=True, nullable=False)
    prereq_course_id = db.Column(db.String(10),primary_key=True, nullable=False)


    
    def json(self):
        course_prereq_info = {
            'course_id' : self.course_id,
            'prereq_course_id': self.prereq_course_id,
  
        }
        return course_prereq_info


class Trainers(Employee):
    __tablename__ = "trainers"
    emp_id = db.Column(db.String(10), db.ForeignKey('employee.emp_id'),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10),nullable=False, primary_key=True)
    class_id= db.Column(db.String(10), nullable=False, primary_key=True)
    completed= db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'trainers',
    }
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        trainers_info = {
            'emp_id': self.emp_id,
            'course_id': self.course_id,
            'class_id': self.class_id,
            'completed': self.completed
  
        }
        return trainers_info

class Learners(db.Model):
    __tablename__ = "learners"
    emp_id = db.Column(db.String(10) ,db.ForeignKey('employee.emp_id'),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10),nullable=False, primary_key=True)
    class_id = db.Column(db.String(10),nullable=False, primary_key=True)
    completed = db.Column(db.Integer,nullable=False)
    


    __mapper_args__ = {
        'polymorphic_identity': 'learners',
    }

    def __init__(self,emp_id,course_id,class_id,completed):
        self.emp_id = emp_id
        self.course_id = course_id
        self.class_id = class_id
        self.completed = completed

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result
    
    def json(self):
        learners_info = {
            'emp_id': self.emp_id,
            'course_id': self.course_id,
            'class_id': self.class_id,
            'completed' : self.completed,
  
        }
        return learners_info