# Might change this to using os.environ.get() instead in future sprints
from decouple import config
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

# Database connection

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

    def __init__(self,learner_id,emp_id,course_id,class_id,completed):
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
#-------------------------------------------------------------------------------------------

@app.route("/classes")
def get_class_list():
    classes = Classes.query.all()
    if len(classes):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "Classes": [class_one.json() for class_one in classes]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no raffle companies."
    }
    ), 404

@app.route("/courses")
def get_course_list():
    course_list = Courses.query.all()
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


@app.route("/course_prerequisite")
def get_course_prerequisite_list():
    course_prerequisites = Course_Prerequisite.query.all()
    if len(course_prerequisites):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "course_prerequisites": [course_prerequisite.json() for course_prerequisite in course_prerequisites]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no raffle companies."
    }
    ), 404


@app.route("/course_registration")
def get_course_registration_list():
    course_registration_list = Course_Registration.query.all()
    print(course_registration_list)
    if len(course_registration_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "course_registrations": [course_registration.json() for course_registration in course_registration_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no course_registration."
    }
    ), 404

@app.route("/employee")
def get_employee_list():
    employees = Employee.query.all()
    print(employees)
    if len(employees):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "employees": [employee.json() for employee in employees]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no employee."
    }
    ), 404


@app.route("/learners")
def get_learners_list():
    learners = Learners.query.all()
    print(learners)
    if len(learners):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "learner": [learner.to_dict() for learner in learners]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no learner."
    }
    ), 404



@app.route("/registration")
def get_registration_list():
    registration_list = Registration.query.all()
    print(registration_list)
    if len(registration_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "registration_list": [registration.json() for registration in registration_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no registration."
    }
    ), 404

@app.route("/role")
def get_role_list():
    roles = Role.query.all()
    if len(roles):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "roles": [role.json() for role in roles]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no raffle companies."
    }
    ), 404


@app.route("/trainers")
def get_trainer_list():
    trainers = Trainers.query.all()
    print(trainers)
    if len(trainers):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "trainers": [trainer.to_dict() for trainer in trainers]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no trainer."
    }
    ), 404



@app.route("/trainers_course")
def get_trainers_course_list():
    trainer_course_list = Trainers_Course.query.all()
    print(trainer_course_list)
    if len(trainer_course_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "trainer_course_list": [trainer_course.json() for trainer_course in trainer_course_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no trainer to courses."
    }
    ), 404
#------------------------------up top clear------------------------------------







@app.route("/course_reg_period")
def get_course_reg_period_list():
    course_reg_period_list = Course_Reg_Period.query.all()
    print(course_reg_period_list)
    if len(course_reg_period_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "course_reg_periods": [course_reg_period.json() for course_reg_period in course_reg_period_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no course_reg_period."
    }
    ), 404



@app.route("/course_emp_assignment")
def get_course_emp_assignment_list():
    course_emp_assignment_list = Course_Emp_Assignment.query.all()
    print(course_emp_assignment_list)
    if len(course_emp_assignment_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "course_emp_assignments": [course_emp_assignment.json() for course_emp_assignment in course_emp_assignment_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no course_emp_assignment."
    }
    ), 404


@app.route("/course_class")
def get_course_class_list():
    course_class_list = Course_Class.query.all()
    print(course_class_list)
    if len(course_class_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "course_classes": [course_class.json() for course_class in course_class_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no course_classes."
    }
    ), 404


@app.route("/class_emp_assignment")
def get_class_emp_assignment_list():
    class_emp_assignment_list = Class_Emp_Assignment.query.all()
    print(class_emp_assignment_list)
    if len(class_emp_assignment_list):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "class_emp_assignment": [class_emp_assignment.json() for class_emp_assignment in class_emp_assignment_list]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no class_emp_assignment."
    }
    ), 404
#------------------------------------------------------------------------------------------------




########################################################################

#homepage for learner
#1API call : class [ID and name] + ccourses  [number of class + slot avaialble]
@app.route("/courses_list")
def retrieve_all_courses():
    array = []
    course_list = Courses.query.all() # course_id etc
    
    if len(course_list):
        for course in course_list:
            course_name = course.course_name
            course_id = course.course_id
            course_description = course.course_desc
            class_list = Classes.query.filter_by(course_id=course_id).all()
            if len(class_list):
                #got class
                class_counter = 0
                slot_available = 0
                for one_class in class_list:
                    slot_available = Classes.get_slot_available(one_class.slots_available,slot_available)
                    class_counter = Classes.get_num_of_class(class_counter)

                # class_size = class_list[0].class_size
                # number_of_class = len(class_list)
                
            value = {
                "course_name": course_name,
                "course_id":course_id,
                "course_description":course_description,
                "slot_available":slot_available,
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






@app.route("/retrieve_course/<string:course_id>")
def retrieve_course(course_id):
    prereq_array = []
  
    course = Courses.query.filter_by(course_id = course_id).first()
    print("course is" + str(course))
    if(not course):
        return jsonify(
            {
                "code": 404,
                "message": "Course id is incorrect."
                }
                ), 404
    #course.course_name, course.course_id, course_desc
   
###################################NEED TO REMOVE COURSE.PREREQ == 0 ####################################
    ########
    if(course.prerequisite == 1):
        #got prereq 
        prereq_list = Course_Prerequisite.query.filter_by(course_id = course_id).all()
        print("lengthh" + str(len(prereq_list)))
        if(len(prereq_list)):
            #go find prereq everything  -> prereq.prereq_course_id
            for prereq in prereq_list: 
                #find all the prereq 
                pre_req_course = Courses.query.filter_by(course_id = prereq.prereq_course_id).first()
                value = {
                    "course_id": pre_req_course.course_id,
                    "course_name":pre_req_course.course_name
                }
                prereq_array.append(value)
    
    return jsonify({
        'code': 200,
        'result': {
            'course_title' :course.course_id + " - " + course.course_name,
            'course_description' : course.course_desc,
            'pre_req': [prereq for prereq in prereq_array]
            }

    })





   
@app.route('/registration/<string:course_id>')
def retrieve_registration(course_id):
    list_of_class = Registration.query.filter_by(course_id = course_id).all()
    if len(list_of_class):
        return jsonify(
            {
                'code': 200,
                'data': {
                    "classes": [class_info.json() for class_info in list_of_class]
                }
            }
        )

    return jsonify(
    {
        "code": 404,
        "message": "There are no classes."
    }
    ), 404

#2nd pages
#course registration + course[description] +  
#preassign tab -> select course registration where preassign = 1
#registered tab -> select course_registration  where = 0 
#enrolled tab -> learners table retrieve all based on the course

@app.route('/retrieve_course_learners/<string:course_id>')
def retrieve_course_learners(course_id):
    ##focus registered tab first
    preassign_learners_array = []
    enrolled_learners_array = []
    registered_learners_array = []

    course_registration_list = Course_Registration.query.filter_by(course_id = course_id, pre_assigned = 1).all()
    if(len(course_registration_list)):
        for  course_reg in course_registration_list:
            employee = Employee.query.filter_by(emp_id = course_reg.emp_id).first()
            class_info = Classes.query.filter_by(class_id = course_reg.class_id).first()

            string = {
                "name": employee.emp_name,
                "emp_id": course_reg.emp_id,
                "class_name" : class_info.course_id + "_" + class_info.class_id,
                "class":class_info.class_id
            }
            preassign_learners_array.append(string)


    course_registration_list = Course_Registration.query.filter_by(course_id = course_id, pre_assigned = 0).all()
    if(len(course_registration_list)):
        for  course_reg in course_registration_list:
            employee = Employee.query.filter_by(emp_id = course_reg.emp_id).first()
            class_info = Classes.query.filter_by(class_id = course_reg.class_id).first()

            string = {
                "name": employee.emp_name,
                "emp_id": course_reg.emp_id,
                "class_name" : class_info.course_id + "_" + class_info.class_id,
                "class":class_info.class_id
            }
            registered_learners_array.append(string)

    learners_lists = Learners.query.filter_by(course_id = course_id, completed = 0).all()
    if(len(learners_lists)):
        for  learner in learners_lists:
            employee = Employee.query.filter_by(emp_id = learner.emp_id).first()
            class_info = Classes.query.filter_by(class_id = learner.class_id).first()

            string = {
                "name": employee.emp_name,
                "emp_id": learner.emp_id,
                "class_name" : class_info.course_id + "_" + class_info.class_id,
                "class_id":class_info.class_id
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



@app.route("/assign_course", methods=['POST','PUT','DELETE'])
def assign_to_course():
    try:
        data = request.get_json()
        print(data)
        print(data['emp_id'])
        print(data['course_id'])
        print(data['class_id'])

        #def __init__(self,learner_id,emp_id,course_id,class_id,completed):
        learner = Learners(
            learner_id= "random",
            emp_id=data['emp_id'],
            course_id=data['course_id'],
            class_id=data['class_id'],
            completed= 0 

        )
        print(learner)

        try:
            db.session.add(learner)
            db.session.commit()

        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while creating the order. " + str(e)
                }
            ), 500

        #need to reduce the class 
        try:
            class_info = Classes.query.filter_by(class_id = data['class_id'], course_id = data['course_id']).first()
            update_slot_available = Classes.compute_slot_available('Assign',class_info.slots_available)
            class_info.slots_available = update_slot_available
            db.session.commit()

        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occur when update the slot " + str(e)
                }
            ), 500



        #############need to do deletion fo this guy in the other compoenent
        emp_id = data["emp_id"]
        course_id = data["course_id"]
        #delete based on emp_id and course_id from front end, assuming this 2 can be a composite key
        course_registration = Course_Registration.query.filter_by(emp_id=emp_id,course_id = course_id,class_id = data['class_id']).first()
        if learner:
            try:
                db.session.delete(course_registration)
                db.session.commit()
            except Exception as e:
                return jsonify(
                {
                    "code": 500,
                    "message": "An error occur when deleting the from course_registration " + str(e)
                }
            ), 500

        return jsonify(
        {
            "code": 201,
            "result":"successfully assign",
            "data_insert": learner.json(),
            # "data_deleted": course_registration.json()
        }
    ), 201

    except Exception as e:
        jsonify(
            {
                "code": 500,
                "message": "An error occurred while assigning. " + str(e)
            }
        ), 500




@app.route("/withdraw_course", methods=['PUT','DELETE'])
def withdraw_course():
    data = request.get_json()
    emp_id = data["emp_id"]
    course_id = data["course_id"]
    class_id = data["class_id"]
    #delete based on emp_id and course_id from front end, assuming this 2 can be a composite key
    learner = Learners.query.filter_by(emp_id=emp_id,course_id = course_id,class_id = class_id).first()
    if learner:
        try:
            db.session.delete(learner)
            db.session.commit()

            class_info = Classes.query.filter_by(class_id = data['class_id'], course_id = data['course_id']).first()
            update_slot_available = Classes.compute_slot_available('Withdraw',class_info.slots_available)
            class_info.slots_available = update_slot_available
            db.session.commit()
        except Exception as e:
            return jsonify(
            {
                "code": 500,
                "message": "There is an error withdrawing from the course" + str(e)
            }
        ), 500
    
        #do update hereto increase slot available to 1
        
        return jsonify(
            {
                "code": 200,
                "data": {
                    "message": "successful delete"
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "message": "error"
            },
            "message": "learner not found."
        }
    ), 404

    







    



if __name__ == '__main__':
    print("RUNNING TEST LETS GO")
    app.run(host='0.0.0.0', port=5000, debug=True)