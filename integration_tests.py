import unittest
import flask_testing
import json
from decouple import config
import requests


from app import *

# Environment Variable

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = config('testURL') or environ.get('testURL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app 
    
    def setUp(self):
        db.create_all()

        # Create 'insert' data here to mock up stuff for testing

        emp_1 = Employee(emp_id="EMP16", emp_name="Peter Parker")
        emp_2 = Employee(emp_id="EMP15", emp_name="Mark Lim")
        emp_3 = Employee(emp_id="EMP17", emp_name="Mary Rose Jane")

        learner_1 = Learner(emp_id="EMP16", learner_id="LNR16")
        learner_2 = Learner(emp_id="EMP15", learner_id="LNR15")
        learner_3 = Learner(emp_id="EMP17", learner_id="LNR17")

        course_1 = Course(course_id="BEM460", course_name="Basic Engineering Management", course_desc="Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.", prerequisite=0)
        
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=50)

        class_record_1 = Class_Record(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR16")

        reg_1 = Registration(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR16", reg_date="2021-12-30")

        reg_2 = Registration(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR17", reg_date="2021-12-30")


        db.session.add(emp_1)
        db.session.commit()

        db.session.add(emp_2)
        db.session.commit()

        db.session.add(emp_3)
        db.session.commit()

        db.session.add(learner_1)
        db.session.commit()

        db.session.add(learner_2)
        db.session.commit()

        db.session.add(learner_3)
        db.session.commit()
        
        db.session.add(course_1)
        db.session.commit()

        db.session.add(class_run_1)
        db.session.commit()

        db.session.add(class_record_1)
        db.session.commit()

        db.session.add(reg_1)
        db.session.commit()

        db.session.add(reg_2)
        db.session.commit()


    def tearDown(self):
        db.session.remove() 
        db.drop_all()


class TestEnrollment(TestApp):
    def test_retrieve_course_class(self):
        course_id = "BEM460"
        endpoint = "enroll_course_details/" + course_id

        response = self.client.get(endpoint)

        self.assertEqual(response.json, {
            "BEM460": [
                {
                    "class_end_date": "2021-11-30",
                    "class_id": "BEM460_C1",
                    "class_start_date": "2021-05-30",
                    "course_id": "BEM460",
                    "reg_end_date": "2021-12-30",
                    "reg_start_date": "2021-02-07"
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
                        "course_description": "Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.",
                        "course_id": "BEM460",
                        "course_name": "Basic Engineering Management",
                        "num_of_class": 1,
                        "total_slot_available": 50
                    }
                ]
            }
        })
    
    def test_get_course_list_pass(self):
        pass

    def test_get_course_list_fail(self):
        pass

class TestLearnerByCourseId(TestApp):
    def test_retrieve_course_learners(self):
        self.maxDiff = None
        course_id = "BEM460"
        endpoint = "learner_list/" + course_id
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {'BEM460': {'enrolled_learners': [{'class_id': 'BEM460_C1', 'emp_id': 'EMP16', 'learner_id': 'LNR16', 'name': 'Peter Parker'}], 'preassign_learners': [], 'registered_learners': [{'class_id': 'BEM460_C1', 'emp_id': 'EMP16','learner_id': 'LNR16','name': 'Peter Parker'}, {'class_id': 'BEM460_C1', 'emp_id': 'EMP17','learner_id': 'LNR17','name': 'Mary Rose Jane'}]}, 'code': 200})


class Test_UpdateSlotAvailableForClass(TestApp):
    def test_update_slot_available_for_class_assign_pass(self):
        data = { 
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }

        action = "Assign"

        status = update_slot_available_for_class(data['class_id'], 'Assign')
        self.assertEqual(status, 200)

    def test_update_slot_available_for_class_assign_fail(self):
        data = {
            "class_id":"BM460_C5",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }
        action = 'Assign'

        # This will reduce the slots_available which will affect other test cases above (dependant, thus should change this.)
        status = update_slot_available_for_class(data['class_id'], 'Assign')
        self.assertEqual(status, 501)

class Test_RemoveClassRunByLearner(TestApp):
    def test_remove_class_run_by_learner_id_success(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }

        status = remove_class_run_by_learner_id(data)
        self.assertEqual(status, 200)

    def test_remove_class_run_by_learner_id_failure(self):
        data = {
            "class_id":"BE0_C4",
            "course_id": "BECC0",
            "learner_id": "LNE14"
        }

        status = remove_class_run_by_learner_id(data)
        self.assertEqual(status, 502)

class Test_DeleteRegistration(TestApp):
    def test_delete_registration_success(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }   

        status = delete_registration(data) 
        self.assertEqual(status, 200)

    def test_delete_registration_failure(self):
        data = {
            "class_id":"BEM46SSS0_C4",
            "course_id": "BEMSDS460",
            "learner_id": "LNR1SD4"
        }   
        status = delete_registration(data) 
        self.assertEqual(status, 502)

class Test_InsertClassRecord(TestApp):
    def test_insert_class_record_success(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR15"
        }  

        status = insert_class_record(data)
        self.assertEqual(status, 200)

    def test_insert_class_record_failure(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460"
        }  

        status = insert_class_record(data)
        self.assertEqual(status, 500)

class Test_InsertRegistration(TestApp):
    def test_insert_registration_success(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR15"
        }  

        status = insert_registration(data)
        self.assertEqual(status, 200)

    def test_insert_registration_failure(self):
        data = {
            "class_id":"BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR14"
        }  

        status = insert_registration(data)
        self.assertEqual(status, 500)

class TestAssignLearner(TestApp):
    def test_assign_to_course_success(self):
        request_body = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR17"
        }

        endpoint = "assign_learner"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_assign_to_course_invalid_input(self):
        request_body = {
            "class_id":"BEM460ZZ_C4"
        }  

        endpoint = "assign_learner"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 500)



if __name__ == '__main__':
    unittest.main()