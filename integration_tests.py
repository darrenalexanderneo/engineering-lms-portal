import unittest
import flask_testing
import json
from decouple import config
import requests

from app import *

# Environment Variable

class TestApp(flask_testing.TestCase):
    # app.config['SQLALCHEMY_DATABASE_URI'] = config('testURL') or environ.get('testURL')
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
        emp_7 = Employee(emp_id="EMP18", emp_name="mary jx")

        emp_4 = Employee(emp_id="EMP20", emp_name="Peter John")
        emp_5 = Employee(emp_id="EMP21", emp_name="Harry Larry")
        emp_6 = Employee(emp_id="EMP22", emp_name="Mary Goh")

        learner_1 = Learner(emp_id="EMP16", learner_id="LNR16")
        learner_2 = Learner(emp_id="EMP15", learner_id="LNR15")
        learner_3 = Learner(emp_id="EMP17", learner_id="LNR17")
        learner_4 = Learner(emp_id="EMP18", learner_id="LNR18")

        trainer_1 = Trainer(emp_id="EMP20", trainer_id="TNR20")
        trainer_2 = Trainer(emp_id="EMP21", trainer_id="TNR21")
        trainer_3 = Trainer(emp_id="EMP22", trainer_id="TNR22")

        course_1 = Course(course_id="BEM460", course_name="Basic Engineering Management", course_desc="Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.", prerequisite=0)
        course_2 = Course(course_id="EE200", course_name="Electricity & Electronics", course_desc="Develop and build analog electronics circuits. You will build multiple circuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles", prerequisite=1)

        # Solely for testing, real DB don't have this prereq
        course_prereq_1 = Course_Prerequisite(course_id="EE200", prereq_course_id="BEM460")
        
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=50)

        class_run_2 = Class_Run(class_id="EE200_C1", course_id="EE200", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=50)

        # For 0 slots available test
        class_run_3 = Class_Run(class_id="BEM460_C2", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-12-30", slots_available=0)

        class_run_4 = Class_Run(class_id="BEM460_C4", course_id="BEM460", class_start_date="2022-05-30", class_end_date="2022-11-30", reg_start_date="2021-12-07", reg_end_date="2021-12-30", slots_available=10)

        class_record_1 = Class_Record(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR16")

        reg_2 = Registration(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR17", reg_date="2021-12-30")

        completion_record_1 = Completion_Record(course_id="BEM460", learner_id="LNR15")



        chapter_1 = Chapter(course_id="BEM460", chapter_id ="BEM460_C1_Chapt1")
        chapter_2 = Chapter(course_id="BEM460", chapter_id ="BEM460_C1_Chapt2")
        chapter_3 = Chapter(course_id="BEM460", chapter_id ="BEM460_C1_Chapt3")

        chapter_learner_1 = Chapter_Learner(chapter_id ="BEM460_C1_Chapt1",learner_id="LNR17",completion = 1)
        db.session.add(emp_1)
        db.session.commit()

        db.session.add(emp_2)
        db.session.commit()

        db.session.add(emp_3)
        db.session.commit()

        db.session.add(emp_4)
        db.session.commit()

        db.session.add(emp_5)
        db.session.commit()

        db.session.add(emp_6)
        db.session.commit()

        db.session.add(emp_7)
        db.session.commit()

        db.session.add(learner_1)
        db.session.commit()

        db.session.add(learner_2)
        db.session.commit()

        db.session.add(learner_3)
        db.session.commit()
        db.session.add(learner_4)
        db.session.commit()

        db.session.add(trainer_1)
        db.session.commit()
        db.session.add(trainer_2)
        db.session.commit()
        db.session.add(trainer_3)
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

        db.session.add(class_run_4)
        db.session.commit()
        db.session.add(class_record_1)
        db.session.commit()

        db.session.add(reg_2)
        db.session.commit()


        db.session.add(completion_record_1)
        db.session.commit()

        chapter_quiz_1 = Chapter_Quiz(quiz_id="BEM460_C1_Chapt1q" , chapter_id="BEM460_C1_Chapt1" ,total_marks="2",timing="10:00")
        chapter_quiz_2 = Chapter_Quiz(quiz_id="BEM460_C2_Chapt1q" , chapter_id="BEM460_C2_Chapt1" ,total_marks="3",timing="10:00")
        #final_quiz
        final_quiz_1 = Final_Quiz(quiz_id="BEM460_C1_finalQuizq" , course_id="BEM460" ,total_marks="2",timing="30:00")
        final_quiz_2= Final_Quiz(quiz_id="BEM460_C2_finalQuizq" , course_id="BEM460" ,total_marks="2",timing="30:00")
        db.session.add(chapter_quiz_1)
        db.session.commit()
        db.session.add(chapter_quiz_2)
        db.session.commit()
        db.session.add(final_quiz_1)
        db.session.commit()
        db.session.add(final_quiz_2)
        db.session.commit()


        #question for chapter_quiz and final_quiz
        chap_question_1 = Question(quiz_id="BEM460_C1_Chapt1q", question_id="Q1" , question="What SPM means" , question_type ="MCQ", option="S,P,M,A",question_mark="2",answer="S")

        final_question_1 = Question(quiz_id="BEM460_C1_finalQuizq", question_id="Q1" , question="What final es means" , question_type ="MCQ", option="V,A,L,O",question_mark="2",answer="L")

        db.session.add(chap_question_1)
        db.session.commit()
 
        db.session.add(final_question_1)
        db.session.commit()

        chapter_quiz_result_1 = Chapter_Quiz_Result(quiz_id = 'BEM460_C1_Chapt1q' , learner_id="LNR16", marks='0')
        db.session.add(chapter_quiz_result_1)
        db.session.commit()


        db.session.add(chapter_1)
        db.session.commit()
        db.session.add(chapter_2)
        db.session.commit()
        db.session.add(chapter_3)
        db.session.commit()


        db.session.add(chapter_learner_1)
        db.session.commit()

        trainer_record_1 = Trainer_Record(class_id ="BEM460_C1" , course_id ="BEM460", trainer_id = "TNR20")

        db.session.add(trainer_record_1)
        db.session.commit()


    def tearDown(self):
        db.session.remove() 
        db.drop_all()


"""
Teoh Jiaxing led this testing
"""
class Test_Enrollment_Endpoint(TestApp):
    def test_retrieve_course_class(self):
        course_id = "BEM460"
        endpoint = "enroll_course_details/" + course_id

        response = self.client.get(endpoint)
        print('test_retrieve_course_class')
        print(response.json)
        self.assertEqual(response.json,{'BEM460': [{'class_end_date': '2021-11-30', 'class_id': 'BEM460_C1', 'class_start_date': '2021-05-30', 'course_id': 'BEM460', 'reg_end_date': '2021-12-30', 'reg_start_date': '2021-02-07'}, {'class_end_date': '2021-11-30', 'class_id': 'BEM460_C2', 'class_start_date': '2021-05-30', 'course_id': 'BEM460', 'reg_end_date': '2021-12-30', 'reg_start_date': '2021-02-07'}, {'class_end_date': '2022-11-30', 'class_id': 'BEM460_C4', 'class_start_date': '2022-05-30', 'course_id': 'BEM460', 'reg_end_date': '2021-12-30', 'reg_start_date': '2021-12-07'}], 'code': 200})

class TestCourseInfo(TestApp):
    def test_retrieve_all_courses(self):
        endpoint = "/enrollment_course_list" 
        response = self.client.get(endpoint)
        print('test_retrieve_all_courses')
        print(response.json)

        self.assertEqual(response.json,{'code': 200, 'data': {'courses': [{'course_description': 'Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.', 'course_id': 'BEM460', 'course_name': 'Basic Engineering Management', 'num_of_class': 3, 'total_slot_available': 60}, {'course_description': 'Develop and build analog electronics circuits. You will build multiple circuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles', 'course_id': 'EE200', 'course_name': 'Electricity & Electronics', 'num_of_class': 1, 'total_slot_available': 50}]}})
    
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
        result = Class_Run(
            class_id="BEM460_C2", 
            course_id="BEM460",
             class_start_date="2021-05-30",
              class_end_date="2021-11-30", 
              reg_start_date="2021-02-07", 
              reg_end_date="2021-12-30", 
              slots_available=1
            
        )

        action = "Assign"

        status = result.compute_slot_available(action)
        # print("test_update_slot_available_for_class_assign_pass is " , status)
        self.assertEqual(status, 200)

    def test_update_slot_available_for_class_assign_fail(self):
        # data = {
        #     "class_id":"BM460_C5",
        #     "course_id": "BEM460",
        #     "learner_id": "LNR14"
        # }
        result = Class_Run(
            class_id="BEM460_C2", 
            course_id="BEM460",
             class_start_date="2021-05-30",
              class_end_date="2021-11-30", 
              reg_start_date="2021-02-07", 
              reg_end_date="2021-12-30", 
              slots_available=0
            
        )
        action = 'Assign'
        # print('test_update_slot_available_for_class_assign_fail' )
        # This will reduce the slots_available which will affect other test cases above (dependant, thus should change this.)
        # status = update_slot_available_for_class(data['class_id'], 'Assign')
        status = result.compute_slot_available(action)
        # print('status is ', status)
        self.assertEqual(status, 400)


"""
Veronica Teng led this testing
"""
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
        reg_3 = Registration(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR18", reg_date="2021-12-30")
        db.session.add(reg_3)
        db.session.commit()
        status = reg_3.delete_registration_db() 
        self.assertEqual(status, 200)

    def test_delete_registration_failure(self):
        registration_record = Registration(
            class_id ="BEM46SSS0_C4",
            course_id = "BEMSDS460",
            learner_id= "LNR1SD4"
        ) 
        status = registration_record.delete_registration_db() 
        self.assertEqual(status, 502)

class Test_InsertClassRecord(TestApp):
    def test_insert_class_record_success(self):
        class_record = Class_Record(
            class_id ="BEM460_C1",
            course_id = "BEM460",
            learner_id= "LNR15"
        )

        status = class_record.insert_class_record()
        self.assertEqual(status, 200)

    def test_insert_class_record_failure(self):
        class_record = Class_Record(
            class_id="BEM460_C1",
            course_id= "BEM460"
        )

        status = class_record.insert_class_record()
        self.assertEqual(status, 502)

class Test_InsertRegistration(TestApp):
    def test_insert_registration_success(self):

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")


        result = Registration(
            class_id = "BEM460_C1",
            course_id = "BEM460",
            learner_id =  "LNR15",
            reg_date = current_date


        )
        status = result.insert_registration()
        self.assertEqual(status, 200)

    
    ##########
    def test_insert_registration_failure(self):

        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")


        result = Registration(
            class_id = "BEM460_C4",
            course_id = "BEM460",
            learner_id =  "LNR14",
            reg_date = current_date


        )
        status = result.insert_registration()
        self.assertEqual(status, 500)

"""
Neo Yong Yi, Darren led this testing
"""
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
        class_record_1 = Class_Record(class_id="BEM460_C1", course_id="BEM460", learner_id="LNR18")
        db.session.add(class_record_1)
        db.session.commit()
        status = class_record_1.delete_class_record()
        self.assertEqual(status, 200)

    def test_delete_class_record_fail(self):
        data = Class_Record(
            class_id="BEM460_C1",
            course_id= "BEM460",
            learner_id= "LNR17"
        )

        status = data.delete_class_record()
        # print("test_delete_class_record_fails", status)
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
        # print("response is")
        # print(response.json)
        self.assertEqual(response.json, {'code': 500, 'message': 'learner cannot be found in class record'})


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
        print("test_register_slots_filled")
        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C2",
            "course_id": "BEM460",
            "learner_id": "LNR15"
        }

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")
        print('test_register_slots_filled message')
        print(response.json)
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

        self.assertEqual(response.json['message'], 'You already registered for the course')

    def test_insertion_issue_date(self):
        endpoint = "register"
        request_body = {
            "class_id": "BEM460_C4",
            "course_id": "BEM460",
            "learner_id": "LNR17"
        }
        
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")
        # print("test_insertion_issue_date")
        # print(response.json)
        self.assertEqual(response.json['message'], 'The course is not available yet.')
    
    def test_register_success(self):
        endpoint = "register"
        print('test_register_success')
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
        # print("test_withdraw_learner_registration_fail")
        # print(response.json)
        self.assertEqual(response.json, {'code': 500, 'message': 'learner cannot be found in class record'})
    

######### sprint 6

"""
Lewanna Erh led this testing
"""
class Test_Question_Endpoint(TestApp):
    def test_retrieve_question_by_course_class_chapter_code_200(self):

        quiz_id = "BEM460_C1_Chapt1q"
        endpoint = "retrieve_question/" + quiz_id

        response = self.client.get(endpoint)
        self.assertEqual(response.json, {'code': 200, 'duration': '10:00', 'question_records': [{'answer': 'S', 'option': 'S,P,M,A', 'question': 'What SPM means', 'question_id': 'Q1', 'question_mark': '2', 'question_type': 'MCQ', 'quiz_id': 'BEM460_C1_Chapt1q'}]})


    def test_retrieve_question_by_course_class_chapter_code_500(self):
  
        quiz_id = "BEM460_C1_Chapt1qunknown"
        endpoint = "retrieve_question/" + quiz_id

        response = self.client.get(endpoint)
        # print(response.json)
        self.assertEqual(response.json, {'code': 500, 'message': 'question not found'})

class Test_auto_compute_quiz_Endpoint(TestApp):
    def test_compute_quiz_wrong(self):
        # print('test compute quiz')
        data = {
                "type" : "chapter_quiz",
                "quiz_id" : "BEM460_C1_Chapt1q",
                "learner_id" : "LNR16",
                "question": "Q1",
                "answer": "M" 
                }
        marks = auto_compute_grade(data)
        # print(marks)
        self.assertEqual(marks, 0)

    def test_compute_quiz_wrong(self):
        # print('test compute quiz')
        data = {
                "type" : "chapter_quiz",
                "quiz_id" : "BEM460_C1_Chapt1q",
                "Learner_id" : "LNR16",
                "question": "Q1",
                "answer": "S" 
                }
        marks = auto_compute_grade(data)
        # print(marks)
        self.assertEqual(marks, 2)

class Test_insert_update_chapter_quiz_db(TestApp):
    def test_insert_chapter_quiz_db(self):
        data = {
            "type" : "chapter_quiz",
            "quiz_id" : "BEM460_C1_Chapt1q",
            "learner_id" : "LNR17",
            "question": "Q1",
            "answer": "M" 
            }
        learner_marks = 2
        record = None
        code = insert_update_into_quiz_result_db(data,learner_marks,record)
        self.assertEqual(code, 200)

    def test_update_chapter_quiz_db(self):
        data = {
            "type" : "chapter_quiz",
            "quiz_id" : "BEM460_C1_Chapt1q",
            "learner_id" : "LNR16",
            "question": "Q1",
            "answer": "M" 
            }
        learner_marks = 2
        record = Chapter_Quiz_Result(
            quiz_id="BEM460_C1_Chapt1q",
            learner_id ="LNR16",
            marks= "0"


        )
        code = insert_update_into_quiz_result_db(data,learner_marks,record)
        self.assertEqual(code, 200)


class Test_insert_update_final_quiz_db(TestApp):
    def test_insert_chapter_quiz_db(self):
        data = {
            "type" : "final_quiz",
            "quiz_id" : "BEM460_C1_finalQuizq",
            "learner_id" : "LNR17",
            "question": "Q1",
            "answer": "M" 
            }
        learner_marks = 2
        record = None
        code = insert_update_into_quiz_result_db(data,learner_marks,record)
        self.assertEqual(code, 200)

    def test_update_chapter_quiz_db(self):
        data = {
            "type" : "final_quiz",
            "quiz_id" : "BEM460_C1_finalQuizq",
            "learner_id" : "LNR16",
            "question": "Q1",
            "answer": "M" 
            }
        learner_marks = 2
        record = Final_Quiz_Result(
            quiz_id="BEM460_C1_Chapt1q",
            learner_id ="LNR16",
            marks= "0"


        )
        code = insert_update_into_quiz_result_db(data,learner_marks,record)
        self.assertEqual(code, 200)

class test_submit_quiz(TestApp):
    def test_submit_quiz(self):
        request_body = {
            "type": "chapter_quiz",
            "quiz_id" : "BEM460_C1_Chapt1q",
            "learner_id" : "LNR17",
            "question": "Q1",
            "answer": "S" 
        }
        endpoint = "submit_quiz"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

    def test_submit_quiz_final(self):
        request_body = {
            "type": "final_quiz",
            "quiz_id" : "BEM460_C1_finalQuizq",
            "learner_id" : "LNR17",
            "question": "Q1",
            "answer": "S" 
        }
        endpoint = "submit_quiz"

        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")

        self.assertEqual(response.status_code, 200)

class test_progress_learner(TestApp):
    def test_progress_learner_id(self):
        class_id = "BEM460_C1"
        learner_id = "LNR16"
        result = retrieve_progress_learner_id(class_id,learner_id)
        # print(result.json)
        self.assertEqual(result.json , {'code': 200, 'progress_percentage': 0.0})


"""
Auyong Tingting led this testing
"""
class Test_retrieve_chapter_details_for_learner(TestApp):
    def test_retrieve_chapter(self):
        # print("COME IN")
        # print('HERHERHEHHER')
        course_id = "BEM460_C1"
        endpoint = "retrieve_chapter/" + course_id
        response = self.client.get(endpoint)
        # print(response.json)
        self.assertEqual(response.json, {'code': 200, 'results': [{'chapter_id': 'BEM460_C1_Chapt1', 'course_id': 'BEM460'}, {'chapter_id': 'BEM460_C1_Chapt2', 'course_id': 'BEM460'}, {'chapter_id': 'BEM460_C1_Chapt3', 'course_id': 'BEM460'}]})
    
    def test_retrieve_chapter_learner_by_learner_id(self):
        course_id = "BEM460_C1"
        learner_id = "LNR17"
        endpoint = "retrieve_chapter_learner_by_learner_id/" + course_id + "/" + learner_id + "/"
        response = self.client.get(endpoint)
        # print(response.json)
        self.assertEqual(response.json, {'code': 200, 'results': [{'chapter_id': 'BEM460_C1_Chapt1', 'completion': 1, 'learner_id': 'LNR17'}]})

    def test_is_complete_all_chapters(self):
        course_class_id = "BEM460_C1"
        learner_id = "LNR17"
        endpoint = "is_complete_all_chapters/" + course_class_id + "/" + learner_id + "/"
        response = self.client.get(endpoint)
        # print("test_is_complete_all_chapters")
        # print(response.json)
        self.assertEqual(response.json, {'code': 200, 'number_of_completion': '1/3', 'results': 0})

    def test_is_complete_all_chapters_empty(self):
        course_class_id = "BEM460_C2"
        learner_id = "LNR17"
        endpoint = "is_complete_all_chapters/" + course_class_id + "/" + learner_id + "/"
        response = self.client.get(endpoint)
        # print("test_is_complete_all_chapters")
        # print(response.json)
        self.assertEqual(response.json, {'code': 404, 'number_of_completion': 0, 'results': 'no results found'})

class Test_Trainer_Chapter_Endpoint(TestApp):
    def test_retrieve_all_course_details_by_trainer_id_success(self):
        trainer_id = "TNR20"
        endpoint = "retrieve_all_course_details_by_trainer_id/" + trainer_id +"/"
        response = self.client.get(endpoint)
        self.assertEqual(response.json, {'code': 200, 'results': [{'class_id': 'BEM460_C1', 'course_name': 'Basic Engineering Management', 'num_of_chapter': 3}]})


    def test_retrieve_all_course_details_by_trainer_id_failure(self):
        trainer_id = "TNR21"
        endpoint = "retrieve_all_course_details_by_trainer_id/" + trainer_id +"/"
        response = self.client.get(endpoint)
        self.assertEqual(response.json,{'code': 404, 'data': {'message': 'This trainer are unable to find in trainer record'}} )
    
    def test_retrieve_chapter_detail(self):
        class_id = "BEM460_C1"
        array_list = retrieve_chapter_detail(class_id)
        # print("test_retrieve_chapter_detail")
        # print(array_list)
        self.assertEqual(array_list, [{'type': 'chapter_quiz', 'chapter_id': 'BEM460_C1_Chapt1', 'chapter_name': 'Chapter 1', 'is_created': 1, 'quiz_id': 'BEM460_C1_Chapt1q'}, {'type': 'chapter_quiz', 'chapter_id': 'BEM460_C1_Chapt2', 'chapter_name': 'Chapter 2', 'is_created': 0, 'quiz_id': 'BEM460_C1_Chapt2q'}, {'type': 'chapter_quiz', 'chapter_id': 'BEM460_C1_Chapt3', 'chapter_name': 'Chapter 3', 'is_created': 0, 'quiz_id': 'BEM460_C1_Chapt3q'}])
    
    def test_retrieve_quiz_chapter_detail(self):
        class_id = "BEM460_C1"
        array_list = retrieve_quiz_chapter_detail(class_id)
        # print("test_retrieve_quiz_chapter_detail")
        # print(array_list)
        self.assertEqual(array_list,[{'type': 'final_quiz', 'chapter_name': 'Finals', 'is_created': 1, 'quiz_id': 'BEM460_C1_finalQuizq'}])

    def test_retrieve_course_details_by_class_id(self):
        class_id = "BEM460_C1"
        endpoint = "retrieve_course_details_by_class_id/" + class_id +"/"
        response = self.client.get(endpoint)
        # print("test_retrieve_course_details_by_class_id")
        # print(response.json)
        self.assertEqual(response.json,{'code': 200, 'results': [{'chapter_id': 'BEM460_C1_Chapt1', 'chapter_name': 'Chapter 1', 'is_created': 1, 'quiz_id': 'BEM460_C1_Chapt1q', 'type': 'chapter_quiz'}, {'chapter_id': 'BEM460_C1_Chapt2', 'chapter_name': 'Chapter 2', 'is_created': 0, 'quiz_id': 'BEM460_C1_Chapt2q', 'type': 'chapter_quiz'}, {'chapter_id': 'BEM460_C1_Chapt3', 'chapter_name': 'Chapter 3', 'is_created': 0, 'quiz_id': 'BEM460_C1_Chapt3q', 'type': 'chapter_quiz'}, {'chapter_name': 'Finals', 'is_created': 1, 'quiz_id': 'BEM460_C1_finalQuizq', 'type': 'final_quiz'}]})


class Test_Trainer_Question_Endpoint(TestApp):
    ## to let this work, need create object for chapter_quiz 
    def test_create_question_chapter_success(self):

        question_record = Question(
                quiz_id="BEM460_C2_Chapt1q",
                question_id="Q1",
                question="How many ggghashira are there in demon slayer?",
                question_type="MCQ",
                option="11,12,13,14",
                question_mark="2",
                answer="13")

        code = question_record.create_question()
        # print("test_create_question is " , code)
        self.assertEqual(code,200)

    def test_create_question_final_success(self):
        question_record = Question(
                quiz_id="BEM460_C2_FinalQuizq",
                question_id="Q1",
                question="How many ggghashira are there in demon slayer?",
                question_type="MCQ",
                option="11,12,13,14",
                question_mark="2",
                answer="13")

        code = question_record.create_question()
        # print("test_create_question_final_success is " , code)
        self.assertEqual(code,200)

    def test_create_question_chapter_failure(self):

        question_record = Question(
                quiz_id="BEM460_C2_Chapt1q",
                question_id="Q1",
                question="How many ggghashira are there in demon slayer?",
                question_mark="2",
                answer="13")

        code = question_record.create_question()
        # print("test_create_question_chapter_failure is " , code)
        self.assertEqual(code,500)

    def test_create_question_final_failure(self):
        question_record = Question(
                quiz_id="BEM460_C2_FinalQuizq",
                question_id="Q1",
                question="How many ggghashira are there in demon slayer?",
                question_mark="2",
                answer="13")

        code = question_record.create_question()
        # print("test_create_question_final_failure is " , code)
        self.assertEqual(code,500)
    def test_insert_chapter_quiz_success(self):

        result = Chapter_Quiz(
            quiz_id ="BEM460_C2_chapt2q",
            total_marks = 2,
            chapter_id = "BEM460_C2_chapt2",
            timing = "30:00"
        )

        code = result.insert_chapter_quiz()
        self.assertEqual(code, 200)

    # def test_insert_chapter_quiz_failure(self):
    #     quiz_id =""
    #     total_marks = 2
    #     chapter_id = ""
    #     timing = "30:00"
    #     code = insert_chapter_quiz(quiz_id,chapter_id,total_marks,timing)
    #     self.assertEqual(code, 500)

    def test_insert_final_quiz_success(self):


        result = Final_Quiz(
            quiz_id ="BEM460_C3_FinalQuizq",
            total_marks = 2,
            course_id = "BEM460",
            timing = "30:00"
        )

        code = result.insert_final_quiz()
        self.assertEqual(code, 200)

    def test_insert_final_quiz_failure(self):

        result = Final_Quiz(
            quiz_id ="BEM460_C3_FinalQuizq",
            total_marks = 2,
            course_id = "",
            timing = "30:00"
        )

        code = result.insert_final_quiz()
        # print("test_insert_final_quiz_failure", code)
        self.assertEqual(code, 500)


    def test_create_quiz_sucess(self):
        request_body = {
            "type" : "final_quiz",
            "quiz_id": "BEM460_C3_FinalQuizq",
            "question_id" : ["Q1","Q2","Q3"],
            "question": ["How many ggghashira are there in demon slayer?","who is the villian in DS" ,"Is Rengoku a flameeeee hashira?"],
            "question_type" : ["MCQ","MCQ","T/F"],
            "option": ["11,12,13,14","Reeengoku,Muzzzzan,Nbnbbezeko,Zezzzntisu","True,False"],
            "question_mark": ["2","2","2"],
            "answer": ["13","Muzan","True"],
            "total_marks" : 6,
            "timing" : "50:00",
            "num_of_questions":3
            }
        endpoint = "create_quiz"
        # print("go into create quiz")
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")
        # print("output")
        # print(response.json)
        self.assertEqual(response.json, {'code': 200, 'results': 'Successfully create the quiz'})


    def test_create_quiz_created(self):
        request_body = {
            "type" : "final_quiz",
            "quiz_id": "BEM460_C2_FinalQuizq",
            "question_id" : ["Q1","Q2","Q3"],
            "question": ["How many ggghashira are there in demon slayer?","who is the villian in DS" ,"Is Rengoku a flameeeee hashira?"],
            "question_type" : ["MCQ","MCQ","T/F"],
            "option": ["11,12,13,14","Reeengoku,Muzzzzan,Nbnbbezeko,Zezzzntisu","True,False"],
            "question_mark": ["2","2","2"],
            "answer": ["13","Muzan","True"],
            "total_marks" : 6,
            "timing" : "50:00",
            "num_of_questions":3
            }
        endpoint = "create_quiz"
        # print("go into create quiz")
        response = self.client.post(endpoint,
        data=json.dumps(request_body),
        content_type="application/json")
        # print("output")
        # print(response.json)
        self.assertEqual(response.json, {'code': 201, 'results': 'Final Quiz have already been created. You are not allow to have multiple entry'})

class Test_Trainer_View_Quiz_Endpoint(TestApp):
    def test_view_quiz(self):
        quiz_id = "BEM460_C1_Chapt1q"
        endpoint = "view_quiz/" + quiz_id + "/"

        response = self.client.get(endpoint)
        # print("test_view_quiz")
        # print(response.json)
        self.assertEqual(response.json,{'code': 200, 'results': {'quiz_id': 'BEM460_C1_Chapt1q', 'results': [{'answer': 'S', 'option': 'S,P,M,A', 'question': 'What SPM means', 'question_id': 'Q1', 'question_mark': '2', 'question_type': 'MCQ', 'quiz_id': 'BEM460_C1_Chapt1q'}], 'timing': '10:00', 'total_marks': '2'}})

    def test_view_final_quiz(self):
        quiz_id = "BEM460_C1_finalQuizq"
        endpoint = "view_quiz/" + quiz_id + "/"

        response = self.client.get(endpoint)
        # print("test_view_quiz")
        # print(response.json)
        self.assertEqual(response.json,{'code': 200, 'results': {'quiz_id': 'BEM460_C1_finalQuizq', 'results': [{'answer': 'L', 'option': 'V,A,L,O', 'question': 'What final es means', 'question_id': 'Q1', 'question_mark': '2', 'question_type': 'MCQ', 'quiz_id': 'BEM460_C1_finalQuizq'}], 'timing': '30:00', 'total_marks': '2'}})



class Test_date_enroll_course_Endpoint(TestApp):
    def test_date_enroll_course_available(self):
        class_id = "BEM460_C1"
        endpoint = "display_course_material_date/" + class_id
        response = self.client.get(endpoint)
        print("test_date_enroll_course_available")
        print(response.json)
        self.assertEqual(response.json,{'code': 200, 'is_commence': 1})

    def test_date_enroll_course_not_available(self):
        #not yet
        class_id = "BEM460_C4"
        endpoint = "display_course_material_date/" + class_id
        response = self.client.get(endpoint)
        print("test_date_enroll_course_not_available")
        print(response.json)
        self.assertEqual(response.json,{'code': 200, 'is_commence': 0})

class Test_is_completed_course_Endpoint(TestApp):
    def test_is_completed_course_true(self):
        course_id = "BEM460"
        learner_id = "LNR15"
        endpoint = "check_completion_course/" + course_id + "/" + learner_id
        response = self.client.get(endpoint)
        print("test_is_completed_course_true")
        print(response.json)
        self.assertEqual(response.json,{'code': 200, 'is_completed': 1})

    def test_is_completed_course_false(self):
        course_id = "BEM460"
        learner_id = "LNR16"
        endpoint = "check_completion_course/" + course_id + "/" + learner_id
        response = self.client.get(endpoint)
        print("test_is_completed_course_false")
        print(response.json)
        self.assertEqual(response.json,{'code': 200, 'is_completed': 0})

###### put AC onto the methods to refer


if __name__ == '__main__':
    unittest.main()