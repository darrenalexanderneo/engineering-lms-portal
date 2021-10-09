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
# app.config['SQLALCHEMY_DATABASE_URI'] = config('dbURL') or environ.get("dbURL")
app.config['SQLALCHEMY_DATABASE_URI'] = config('localURL') or environ.get('localURL')

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

class Registration(db.Model):
    __tablename__ = "registration"
    class_id = db.Column(db.String(10), db.ForeignKey("class_run.class_id"),primary_key=True, nullable=False)
    course_id = db.Column(db.String(10), db.ForeignKey("course.course_id"), nullable=False)
    learner_id =  db.Column(db.String(10), db.ForeignKey('learner.learner_id'), primary_key=True, nullable=False)
    reg_date = db.Column(db.String(50),nullable=False)

    def get_current_date():
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        print(current_date)
        return current_date

    # def getClassId(self):
    #     return self.class_id
    
    # def getCourseId(self):
    #     return self.course_id
    # def getLearnerId(self):
    #     return self.learner_id
    # def getRegDate(self):
    #     return self.reg_date



db.create_all()



@app.route("/course_classes/<string:course_id>")
def retrieve_course_class(course_id):
    #registration, course, class table # course_id etc

    
    # course = Course.query.filter_by(course_id = course_id).first()
    # course_name = course.course_name
    class_run_list = Class_Run.query.filter_by(course_id = course_id).all()

    if(len(class_run_list)):
        class_run_array = []
        for class_run in class_run_list:
            is_registration = class_run.check_available_date()
            if is_registration:
                class_run_array.append(class_run)
    return jsonify(
        {
            'code': 200,
                course_id: [class_run.json() for class_run in class_run_array]

        }
    )


@app.route("/courses_list")
def retrieve_all_courses():
    array = []
    course_list = Course.query.all() # course_id etc
    
    if len(course_list):
        for course in course_list:
            course_name = course.course_name
            course_id = course.course_id
            course_description = course.course_desc
            class_run_list = Class_Run.query.filter_by(course_id=course_id).all()
            if len(class_run_list):
                #got class
                class_counter = 0
                total_slot_available = 0
                for class_run in class_run_list:
                    is_registration = class_run.check_available_date()
                    if is_registration:
                        #means allow to display 
                        total_slot_available = class_run.compute_total_slot_available(total_slot_available)
                        class_counter+=1
                
            value = {
                "course_name": course_name,
                "course_id":course_id,
                "course_description":course_description,
                "total_slot_available":total_slot_available,
                "num_of_class": class_counter
            }

            array.append(value)

        
        return jsonify(
            {
                'code': 200,
                'data': {
                    "courses": [course for course in array]
                }
            }
        )




@app.route("/courses")
def get_course_list():
    course_list = Course.query.all()
    print(course_list)
    if len(course_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "courses": [course.json() for course in course_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no course."
    }
    ), 404





@app.route('/retrieve_course_learners/<string:course_id>')
def retrieve_course_learners(course_id):
    ##focus registered tab first
    preassign_learners_array = []
    enrolled_learners_array = []
    registered_learners_array = []

    ##for now remove preassign 


    course_registration_list = Registration.query.filter_by(course_id = course_id).all()
    if(len(course_registration_list)):
        for  course_reg in course_registration_list:
            learner = Learner.query.filter_by(learner_id = course_reg.learner_id).first()
            #get learner already find the emp id
            employee = Employee.query.filter_by(emp_id = learner.emp_id).first()


            string = {
                "name": employee.emp_name,
                "emp_id": learner.emp_id,
                "learner_id": course_reg.learner_id,
                "class_id":course_reg.class_id
            }
            registered_learners_array.append(string)

    class_record_list = Class_Record.query.filter_by(course_id = course_id).all()
    if(len(class_record_list)):
        for  class_record in class_record_list:
            learner = Learner.query.filter_by(learner_id = class_record.learner_id).first()
            #get learner already find the emp id
            employee = Employee.query.filter_by(emp_id = learner.emp_id).first()
            string = {
                "name": employee.emp_name,
                "emp_id": learner.emp_id,
                "learner_id": class_record.learner_id,
                "class_id":class_record.class_id
            }
            enrolled_learners_array.append(string)
    

    return jsonify(
        {
            'code': 200,
            course_id: {
                "preassign_learners": [result for result in preassign_learners_array],
                "registered_learners": [result for result in registered_learners_array],
                "enrolled_learners": [result for result in enrolled_learners_array]
            }
        }
    )


#@app.route("/update_slot_available_for_class/<string:class_id>", methods=['PUT'])
def update_slot_available_for_class(class_id,action):
    #taking in the account if there is only unique class_id in the database table ONLY
    try:
        class_info = Class_Run.query.filter_by(class_id = class_id).first()
        class_info.compute_slot_available(action)
        db.session.commit()
        return 200
    except Exception as e:
        return 501

#@app.route("/delete_registration", methods=['DELETE'])
def delete_registration(data):
    try:
        class_id = data["class_id"]
        course_id = data["course_id"]
        learner_id = data["learner_id"]
        #delete based on emp_id and course_id from front end, assuming this 2 can be a composite key
        registration = Registration.query.filter_by(class_id=class_id,course_id = course_id,learner_id = learner_id).first()
        db.session.delete(registration)
        db.session.commit()
        return 200
    except Exception as e:
        return 502

#@app.route("/insert_class_record")
def insert_class_record(data):
    try:
        print(data)
        print(data['class_id'])
        print(data['course_id'])
        print(data['learner_id'])

        #def __init__(self,emp_id,course_id,class_id,completed):
        class_record = Class_Record(
            class_id=data['class_id'],
            course_id=data['course_id'],
            learner_id=data['learner_id']
        )
        print(class_record)
        db.session.add(class_record)
        db.session.commit()
        return 200
    except Exception as e:
        return 500

@app.route("/assign_course", methods=['POST'])
def assign_to_course():
    #insert into class record, update slot available, delete from registration
    try:
        data = request.get_json()
        insert_code = insert_class_record(data)
        #update slot available 
        update_code = update_slot_available_for_class(data['class_id'],'Assign')
        delete_code = delete_registration(data)

        if(insert_code == 500 or update_code == 501 or delete_code ==502):
            return jsonify(
            {
                "insert_code": insert_code,
                "update_code": update_code,
                "delete_code": delete_code,
                "message": "There is an problem performing the execution"
            }
            ), 500
        return jsonify(
            {
                "code": 200,
                "message": "Successfully enrolled into the class."
            }
            ), 200



    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occur when update the slot " + str(e)
            }
        ), 500


def delete_class_record(data):
    class_id = data["class_id"]
    course_id = data["course_id"]
    learner_id = data["learner_id"]
    try:
        class_record = Class_Record.query.filter_by(class_id=class_id,course_id = course_id,learner_id = learner_id).first()
        db.session.delete(class_record)
        db.session.commit()
        return 200
    except Exception as e:
        return 500
    



@app.route("/withdraw_course", methods=['PUT'])
def withdraw_course():
    try:
        data = request.get_json()
        delete_code = delete_class_record(data)
        update_code = update_slot_available_for_class(data['class_id'],'Withdraw')
        if(delete_code == 500 or update_code == 501):
            return jsonify(
            {
                "delete_code": delete_code,
                "update_code": update_code,
                "message": "There is an problem performing the execution"
            }
            ), 500
            
        return jsonify(
            {
                "code": 200,
                "data": {
                    "message": "successful withdraw from the course!"
                }
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "message": "error"
                },
                "message": "learner not found."
            }
        ), 404

############################################################################################################################
if __name__ == '__main__':
    print("RUNNING TEST LETS GO")
    app.run(host='0.0.0.0', port=5000, debug=True)