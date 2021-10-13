import unittest
import flask_testing
import json
from decouple import config
import requests


from app import *

# Environment Variable
backend_endpoint = config("localBackendURL") or environ.get("localBackendURL")

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('localURL') or environ.get('localURL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app 
    
    def setUp(self):
        # db.create_all()
        # print("Stimulating creating db from setUp...")
        pass

    def tearDown(self):
        db.session.remove() 
        # db.drop_all()
        # print("Stimulating db session drop all.....")


class TestEnrollment(TestApp):
    def test_retrieve_course_class(self):
        course_id = "BEM460"
        endpoint = "enroll_course_details/" + course_id

        response = self.client.get(endpoint)

        self.assertEqual(response.json, {
            "BEM460": [
                {
                    "class_end_date": "2022-03-30",
                    "class_id": "BEM460_C3",
                    "class_start_date": "2021-12-30",
                    "course_id": "BEM460",
                    "reg_end_date": "2021-12-07",
                    "reg_start_date": "2021-10-07"
                },
                {
                    "class_end_date": "2022-03-30",
                    "class_id": "BEM460_C4",
                    "class_start_date": "2021-12-30",
                    "course_id": "BEM460",
                    "reg_end_date": "2021-12-07",
                    "reg_start_date": "2021-10-07"
                }
            ],
            "code": 200
        })
    

class TestCourseInfo(TestApp):
    def test_retrieve_all_courses(self):

        endpoint = "/enrollment_course_list" 
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {
        "code": 200,
        "data": {
            "courses": [
            {
                "course_description": "Learning the basic concepts of engineering. In addition, \nreal life concepts will be introduced as well.",
                "course_id": "BEM460",
                "course_name": "Basic Engineering Management",
                "num_of_class": 2,
                "total_slot_available": 70
            },
            {
                "course_description": "You will also be prepared for internationally recognised industry certification examinations such as those from National Instruments, UI Path, Microsoft and Unity3D\n",
                "course_id": "CE100",
                "course_name": "Computer Engineering",
                "num_of_class": 1,
                "total_slot_available": 30
            },
            {
                "course_description": "Develop and build analog electronics circuits. You will build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n",
                "course_id": "EE200",
                "course_name": "Electricity & Electronics",
                "num_of_class": 1,
                "total_slot_available": 40
            },
            {
                "course_description": "Develop and build analog electronics circuits. You awill build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n",
                "course_id": "EM140",
                "course_name": "Engineering Management",
                "num_of_class": 1,
                "total_slot_available": 30
            },
            {
                "course_description": "The unique ES course prepares you well for a wide range of degrees and careers in fields such as artificial intelligence and machine learning, as well as computer, electrical, electronic, and mechanical engineering, material and even medical science.",
                "course_id": "ES222",
                "course_name": "Engineering Science",
                "num_of_class": 1,
                "total_slot_available": 20
            },
            {
                "course_description": "Mechanical engineering touches virtually every aspect of modern life. Imagine an autonomous car powered by renewable energy and a robotic exoskeleton that can help seniors improve their range of motions.",
                "course_id": "ME111",
                "course_name": "Mechanical Engineering",
                "num_of_class": 1,
                "total_slot_available": 20
            }
            ]
        }
    })

    def test_get_course_list_pass(self):
        endpoint = "courses"
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {
        "code": 200,
        "data": {
            "courses": [
                {
                    "course_desc": "Learning the basic concepts of engineering. In addition, \nreal life concepts will be introduced as well.",
                    "course_id": "BEM460",
                    "course_name": "Basic Engineering Management",
                    "prerequisite": 0
                },
                {
                    "course_desc": "You will also be prepared for internationally recognised industry certification examinations such as those from National Instruments, UI Path, Microsoft and Unity3D\n",
                    "course_id": "CE100",
                    "course_name": "Computer Engineering",
                    "prerequisite": 1
                },
                {
                    "course_desc": "Develop and build analog electronics circuits. You will build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n",
                    "course_id": "EE200",
                    "course_name": "Electricity & Electronics",
                    "prerequisite": 1
                },
                {
                    "course_desc": "Develop and build analog electronics circuits. You awill build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n",
                    "course_id": "EM140",
                    "course_name": "Engineering Management",
                    "prerequisite": 0
                },
                {
                    "course_desc": "The unique ES course prepares you well for a wide range of degrees and careers in fields such as artificial intelligence and machine learning, as well as computer, electrical, electronic, and mechanical engineering, material and even medical science.",
                    "course_id": "ES222",
                    "course_name": "Engineering Science",
                    "prerequisite": 1
                },
                {
                    "course_desc": "Mechanical engineering touches virtually every aspect of modern life. Imagine an autonomous car powered by renewable energy and a robotic exoskeleton that can help seniors improve their range of motions.",
                    "course_id": "ME111",
                    "course_name": "Mechanical Engineering",
                    "prerequisite": 1
                }
            ]
            }
        })

    # Need to figure out how to drop the entire table in order for this code to work
    # Current idea is... you drop the entire table, and then you put the entire table back... by inserting everything else.
    def test_get_course_list_fail(self):
        pass
        # Assuming we call the endpoint and retrieve results
        # endpoint = "courses"
        # response = self.client.get(endpoint)

        # self.assertEqual(response.json, {
        # "code": 404,
        #   "message": "There are no course."
        # })

class TestLearnerByCourse(TestApp):
    def test_retrieve_course_learners(self):
        course_id = "BEM460"
        endpoint = "learner_list/" + course_id
        response = self.client.get(endpoint)

        self.assertEqual(response.json,
        {
            "BEM460": {
                "enrolled_learners": [
                    {
                        "class_id": "BEM460_C3",
                        "emp_id": "EMP12",
                        "learner_id": "LNR12",
                        "name": "Hong Hock Seng"
                    },
                    {
                        "class_id": "BEM460_C3",
                        "emp_id": "EMP13",
                        "learner_id": "LNR13",
                        "name": "Muhammad Ali"
                    }
                ],
                "preassign_learners": [],
                "registered_learners": [
                    {
                        "class_id": "BEM460_C4",
                        "emp_id": "EMP14",
                        "learner_id": "LNR14",
                        "name": "Vanessa Ng"
                    },
                    {
                        "class_id": "BEM460_C4",
                        "emp_id": "EMP15",
                        "learner_id": "LNR15",
                        "name": "Mark Lim"
                    }
                ]
            },
            "code": 200
        })

class TestAssignLearner(TestApp):
    def test_update_slot_available_for_class_pass(self):
    # You have to make sure when you change the db, you reset it to the original state.
    # Like for e.g. slots_available must be added back up.
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }
        action = 'Assign'

        status = update_slot_available_for_class(data['class_id'], 'Assign')
        self.assertEqual(status, 200)


        # Very important Step to reset, if not all tests will fail
        class_info = Class_Run.query.filter_by(class_id = data['class_id']).first()
        
        # Reset count 
        class_info.slots_available += 1
        db.session.commit()


    # BM460_C5 don't exist
    def test_update_slot_available_for_class_fail(self):
        data = {
            "class_id":"BM460_C5",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }
        action = 'Assign'

        # This will reduce the slots_available which will affect other test cases above (dependant, thus should change this.)
        status = update_slot_available_for_class(data['class_id'], 'Assign')
        self.assertEqual(status, 501)
    
class TestRemoveClassRunByLearner(TestApp):
    def test_remove_class_run_by_learner_id_success(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }

        # Get a copy to reset later
        registration_list = Registration.query.filter_by(course_id = data['course_id'],learner_id = data['learner_id']).all()

        status = remove_class_run_by_learner_id(data)
        self.assertEqual(status, 200)

        # Reset back the deletion
        for reg in registration_list:
            registration = Registration(class_id=reg.class_id, course_id=reg.course_id, learner_id=reg.learner_id, reg_date=reg.reg_date)
            db.session.add(registration)

        db.session.commit()

    def test_remove_class_run_by_learner_id_failure(self):
        data = {
            "class_id":"BE0_C4",
            "course_id": "BECC0",
            "learner_id": "LNE14"
        }

        status = remove_class_run_by_learner_id(data)
        self.assertEqual(status, 502)

class TestDeleteRegistration(TestApp):
    def test_delete_registration_success(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }   

        # Get a copy to reset later
        registration_list = Registration.query.filter_by(class_id=data['class_id'],course_id = data['course_id'],learner_id = data['learner_id']).first()

        status = delete_registration(data) 
        self.assertEqual(status, 200)

        # Reset the table row
        registration = Registration(class_id=registration_list.class_id, course_id=registration_list.course_id, learner_id=registration_list.learner_id, reg_date=registration_list.reg_date)

        db.session.add(registration)
        db.session.commit()

    def test_delete_registration_failure(self):
        data = {
            "class_id":"BEM46SSS0_C4",
            "course_id": "BEMSDS460",
            "learner_id": "LNR1SD4"
        }   
        status = delete_registration(data) 
        self.assertEqual(status, 502)

class TestInsertClassRecord(TestApp):
    def test_insert_class_record_success(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }  

        status = insert_class_record(data)
        self.assertEqual(status, 200)

        #  Delete person off table
        class_record = Class_Record.query.filter_by(class_id=data['class_id'], course_id=data['course_id'], learner_id=data['learner_id']).first()
        db.session.delete(class_record)
        db.session.commit()
    
    # We leave out learner_id
    def test_insert_class_record_failure(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460"
        }  

        status = insert_class_record(data)
        self.assertEqual(status, 500)
    
class TestInsertRegistration(TestApp):
    def test_insert_registration_success(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }  

        status = insert_registration(data)
        self.assertEqual(status, 200)

        # Reset the table
        reg = Registration.query.filter_by(class_id=data['class_id'], course_id=data['course_id'], learner_id=data['learner_id']).first()
        db.session.delete(reg)
        db.session.commit()

    def test_insert_registration_failure(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }  

        status = insert_registration(data)
        self.assertEqual(status, 500)


if __name__ == '__main__':
    unittest.main()