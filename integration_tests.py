import unittest
import flask_testing
import json
from decouple import config
import requests


from app import *

# Environment Variable

class TestApp(flask_testing.TestCase):
    # app.config['SQLALCHEMY_DATABASE_URI'] = config('testURL') or environ.get('testURL')
    #Testing
    app.config['SQLALCHEMY_DATABASE_URI'] = config('testURLRDS') or environ.get('testURLRDS')
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
        course_2 = Course(course_id="EE200", course_name="Electricity & Electronics", course_desc="Develop and build analog electronics circuits. You will build multiple circuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles", prerequisite=1)

        # Solely for testing, real DB don't have this prereq
        course_prereq_1 = Course_Prerequisite(course_id="EE200", prereq_course_id="BEM460")
        
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=50)

        class_run_2 = Class_Run(class_id="EE200_C1", course_id="EE200", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=50)

        # For 0 slots available test
        class_run_3 = Class_Run(class_id="BEM460_C2", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=0)

        class_record_1 = Class_Record(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR16")

        reg_2 = Registration(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR17", reg_date="2021-12-30")

        completion_record_1 = Completion_Record(course_id="BEM460", learner_id="LNR15")

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
        db.session.add(course_2)
        db.session.commit()

        db.session.add(course_prereq_1)
        db.session.commit()

        db.session.add(class_run_1)
        db.session.commit()

        db.session.add(class_run_2)
        db.session.commit()

        db.session.add(class_run_3)
        db.session.commit()

        db.session.add(class_record_1)
        db.session.commit()

        db.session.add(reg_2)
        db.session.commit()

        db.session.add(completion_record_1)
        db.session.commit()


    def tearDown(self):
        db.session.remove() 
        db.drop_all()


class Test_Enrollment_Endpoint(TestApp):
    def test_retrieve_course_class(self):
        course_id = "BEM460"
        endpoint = "enroll_course_details/" + course_id

        response = self.client.get(endpoint)

        self.assertEqual(response.json, {'BEM460': [{'class_end_date': '2021-11-30', 'class_id': 'BEM460_C1', 'class_start_date': '2021-05-30', 'course_id': 'BEM460', 'reg_end_date': '2021-12-30', 'reg_start_date': '2021-02-07'}, {'class_end_date': '2021-11-30', 'class_id': 'BEM460_C2', 'class_start_date': '2021-05-30', 'course_id': 'BEM460', 'reg_end_date': '2021-12-30', 'reg_start_date': '2021-02-07'}], 'code': 200})

class TestCourseInfo(TestApp):
    def test_retrieve_all_courses(self):
        endpoint = "/enrollment_course_list" 
        response = self.client.get(endpoint)

        self.assertEqual(response.json,{'code': 200, 'data': {'courses': [{'course_description': 'Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.', 'course_id': 'BEM460', 'course_name': 'Basic Engineering Management', 'num_of_class': 2, 'total_slot_available': 50}, {'course_description': 'Develop and build analog electronics circuits. You will build multiple circuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles', 'course_id': 'EE200', 'course_name': 'Electricity & Electronics', 'num_of_class': 1, 'total_slot_available': 50}]}})
    
    def test_get_course_list_pass(self):
        pass

    def test_get_course_list_fail(self):
        pass

class Test_LearnerByCourseId_Endpoint(TestApp):
    def test_retrieve_course_learners(self):
        self.maxDiff = None
        course_id = "BEM460"
        endpoint = "learner_list/" + course_id
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {'BEM460': {'enrolled_learners': [{'class_id': 'BEM460_C1', 'emp_id': 'EMP16', 'learner_id': 'LNR16', 'name': 'Peter Parker'}], 'preassign_learners': [], 'registered_learners': [{'class_id': 'BEM460_C1', 'emp_id': 'EMP17', 'learner_id': 'LNR17', 'name': 'Mary Rose Jane'}]}, 'code': 200})


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
            "learner_id": "LNR17"
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
            "learner_id": "LNR17"
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

class Test_AssignLearner_Endpoint(TestApp):
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

class Test_DeleteClassRecord(TestApp):
    def test_delete_class_record_pass(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }
        status = delete_class_record(data)
        self.assertEqual(status, 200)

    def test_delete_class_record_fail(self):
        data = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR17"
        }
        status = delete_class_record(data)
        self.assertEqual(status, 502)

class Test_WithdrawEnrolledLearner_Endpoint(TestApp):
    def test_withdraw_course_pass(self):
        request_body = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16"
        }
        endpoint = "withdraw_enrolled_learner"
        response = self.client.put(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_withdraw_course_fail(self):
        request_body = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR17"
        }
        endpoint = "withdraw_enrolled_learner"
        response = self.client.put(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 500)

class Test_RegistrationCourseList_Endpoint(TestApp):
    def test_registration_course_list(self):
        endpoint = "registration_course_list"
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {'code': 200, 'course_list': [{'course_desc': 'Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.', 'course_id': 'BEM460', 'course_name': 'Basic Engineering Management', 'prereq_courses': ''}, {'course_desc': 'Develop and build analog electronics circuits. You will build multiple circuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles', 'course_id': 'EE200', 'course_name': 'Electricity & Electronics', 'prereq_courses': 'BEM460'}]})
    
    def test_reg_course_details(self):
        endpoint = "reg_course_details/BEM460"
        response = self.client.get(endpoint)
        self.assertEqual(response.json, {'code': 200, 'data': {'course_description': 'Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.', 'course_id': 'BEM460', 'course_name': 'Basic Engineering Management', 'num_of_slots': 50, 'prereq_courses': ''}})

class Test_EnrollmentByCourseIDAndLearnerID(TestApp):
    def test_enrollment_existing_record(self):
        endpoint = "enrollment_status/BEM460/LNR16"
        response = self.client.get(endpoint)
        self.assertEqual(response.json['message'], "You have already enrolled in this course.")
    
    def test_enrollment_completion_record(self):
        endpoint = "enrollment_status/BEM460/LNR15"
        response = self.client.get(endpoint)
        self.assertEqual(response.json['message'], "You have already completed in this course.")

    def test_enrollment_prereq(self):
        endpoint = "enrollment_status/EE200/LNR16"
        response = self.client.get(endpoint)
        self.assertEqual(response.json['message'], "You have not complete the pre-requisite yet.")

    def test_enrollment_success(self):
        endpoint = "enrollment_status/BEM460/LNR17"
        response = self.client.get(endpoint)
        self.assertEqual(response.json['message'], "Retrieve successfully.")

class Test_Registration_Endpoint(TestApp):
    def test_register_slots_filled(self):

        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C2",
            "course_id": "BEM460",
            "learner_id": "LNR15"
        }

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.json['message'], f"{request_body['class_id']} is currently full.")

    def test_insertion_issue(self):
        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR17"
        }
        
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.json['message'], "There is an problem performing the execution")
    
    def test_register_success(self):
        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR15"
        }
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.json['message'], f"Successfully register for {request_body['class_id']}.")

    def test_register_exception_error(self):
        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C1",
        }
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 500)

    def test_registration_details_by_learner_id(self):
        endpoint = "registration_details/LNR17"
        response = self.client.get(endpoint)

        self.assertEqual(response.json, {'code': 200, 'results': [{'class_id': 'BEM460_C1', 'course_id': 'BEM460', 'course_name': 'Basic Engineering Management', 'is_approved': 0}]})

    def test_withdraw_learner_registration_success(self):
        request_body = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR16",
            "is_approved": 1
        }

        endpoint = "withdraw_learner_registration"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.json['message'], "Successfully withdraw from the class.")

    def test_withdraw_learner_registration_fail(self):
        request_body = {
            "class_id":"BEM460_C1",
            "course_id": "BEM460",
            "learner_id": "LNR15",
            "is_approved": 1
        }

        endpoint = "withdraw_learner_registration"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 500)
    



    

    





if __name__ == '__main__':
    unittest.main()