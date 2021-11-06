import unittest
from datetime import datetime
# from app import Employee, Senior_Engineer, Engineer, Trainer, Completion_Record, Course, Course_Prerequisite, Class_Run, Trainer_Record, Class_Record, Registration
from app import *


"""
Auyong Tingting led this testing
"""
class TestEmployee(unittest.TestCase):
    def test_json(self):
        emp1 = Employee(emp_id="EMP6", emp_name="Tom Poskitt")

        self.assertEqual(emp1.json(), {
            "emp_id": "EMP6",
            "emp_name": "Tom Poskitt"
        })

class TestSeniorEngineer(unittest.TestCase):
    def test_json(self):
        senior_eng_1 = Senior_Engineer(emp_id="EMP6", emp_name="Tom Poskitt")

        # This object should inherit emp_name from Employee class
        self.assertEqual(senior_eng_1.json(), {
            "emp_id": "EMP6",
            "emp_name": "Tom Poskitt"
        })

class TestEngineer(unittest.TestCase):
    def test_json(self):
        eng_1 = Senior_Engineer(emp_id="EMP8", emp_name="Tongkat Ali")

        # This object should inherit emp_name from Employee class
        self.assertEqual(eng_1.json(), {
            "emp_id": "EMP8",
            "emp_name": "Tongkat Ali"
        })

class TestCourse(unittest.TestCase):

    def test_json(self):
        course_1 = Course(course_id="BEM460", course_name="Basic Engineering Management", course_desc="Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.", prerequisite=0)

        self.assertEqual(course_1.json(), {
            'course_id': "BEM460", 
            'course_name': "Basic Engineering Management",
            'course_desc': "Learning the basic concepts of engineering. In addition, real life concepts will be introduced as well.",
            'prerequisite': 0
            })

"""
Teoh Jiaxing led this testing
"""
class TestClassRun(unittest.TestCase):

    def test_check_available_end_date_true(self):
    # Test with dt_string > reg_end_date, since it is using the current date_time, we will just play with reg_end_date accordingly.
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2030-05-31", slots_available=50)
            
        status = class_run_1.check_available_date()
        self.assertEqual(True, status)

    def test_check_available_end_date_false(self):
        # Test with dt_string > reg_end_date, since it is using the current date_time, we will just play with reg_end_date accordingly.
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-05-31", slots_available=50)

        status = class_run_1.check_available_date()
        self.assertEqual(False, status)

    # For trainers
    def test_check_available_date_true(self):
        # Test with dt_string > reg_end_date, since it is using the current date_time, we will just play with reg_end_date accordingly.
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2030-05-31", slots_available=50)

        status = class_run_1.check_available_date()
        self.assertEqual(True, status)

    def test_check_available_date_false(self):
        # Test with dt_string > reg_end_date, since it is using the current date_time, we will just play with reg_end_date accordingly.
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2030-04-07", reg_end_date="2030-05-31", slots_available=50)

        status = class_run_1.check_available_date()
        self.assertEqual(False, status)

    # Jiaxing might change this code cause the logic not the best.
    def test_compute_total_slot_available(self):
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-04-30", slots_available=50)

        total_slot_available = class_run_1.compute_total_slot_available(10)
        self.assertEqual(60, total_slot_available)

    def test_compute_slot_available_assign(self):
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-04-30", slots_available=50)

        class_run_1.compute_slot_available("Assign")
        self.assertEqual(49, class_run_1.slots_available)

    def test_compute_slot_available_withdraw(self):
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-04-30", slots_available=48)

        class_run_1.compute_slot_available("Withdraw")
        self.assertEqual(49, class_run_1.slots_available)


    def test_json(self):
        class_run_1 = Class_Run(class_id="BEM460_C1", course_id="BEM460", class_start_date="2021-05-30", class_end_date="2021-11-30", reg_start_date="2021-02-07", reg_end_date="2021-04-30", slots_available=50)

        self.assertEqual(class_run_1.json(), {
            'class_id': "BEM460_C1", 
            'course_id': "BEM460",
            'class_start_date': "2021-05-30",
            'class_end_date': "2021-11-30",
            'reg_start_date': "2021-02-07",
            'reg_end_date': "2021-04-30",
            'slots_available' : 50
        })


class TestQuestion(unittest.TestCase):
    def test_json(self):
        question_1 = Question(quiz_id="BEM460_C1_Chapt1q", question_id="Q1", question="does BEM stand for Basic Engineering Management?", question_type="T/F", option =  "True,False", question_mark= "2", answer="True")
        self.assertEqual(question_1.json(), {
            'quiz_id': "BEM460_C1_Chapt1q", 
            'question_id': "Q1",
            'question': "does BEM stand for Basic Engineering Management?",
            'question_type': "T/F",
            'option': "True,False",
            'question_mark': "2",
            'answer': "True"
            })

    def test_compute_marks_correct(self):
        question_1 = Question(quiz_id="BEM460_C1_Chapt1q", question_id="Q1", question="does BEM stand for Basic Engineering Management?", question_type="T/F", option =  "True,False", question_mark= "2", answer="True")

        marks = question_1.compute_marks("True")
        self.assertEqual(marks, 2)

    def test_compute_marks_wrong(self):
        question_1 = Question(quiz_id="BEM460_C1_Chapt1q", question_id="Q1", question="does BEM stand for Basic Engineering Management?", question_type="T/F", option =  "True,False", question_mark= "2", answer="True")

        marks = question_1.compute_marks("False")
        self.assertEqual(marks, 0)


"""
Neo Yong Yi, Darren led this testing
"""
class TestChapter_Quiz_Result(unittest.TestCase):
    def test_update_mark_existing_chapter_quiz_result(self):
        learner_marks = 5
        chapter_quiz_result = Chapter_Quiz_Result(
            quiz_id ="BEM460_C1_Chapt1q",
            learner_id = "LNR16",
            marks="4"
        )
        chapter_quiz_result.update_mark_existing_chapter_quiz_result(learner_marks)
        self.assertEqual(chapter_quiz_result.marks,learner_marks)


class TestFinal_Quiz_Result(unittest.TestCase):
    def test_update_mark_existing_chapter_quiz_result(self):
        learner_marks = 5
        chapter_quiz_result = Final_Quiz_Result(
            quiz_id ="BEM460_C1_FinalQuizq",
            learner_id = "LNR16",
            marks="4"
        )
        chapter_quiz_result.update_mark_existing_final_quiz_result(learner_marks)
        self.assertEqual(chapter_quiz_result.marks,learner_marks)


"""
Lewanna Erh led this testing
"""
class TestFinal_quiz(unittest.TestCase):
    def test_final_check_pass_failure(self):
        learner_marks = 20
        result = Final_Quiz(
             quiz_id = "BEM460_C1_FinalQuizq",
             course_id = "LNR16",
             total_marks = "30"
        )
        is_pass = result.final_check_pass(learner_marks)
        self.assertEqual(is_pass,0)

    def test_final_check_pass_success(self):
        learner_marks = 29
        result = Final_Quiz(
             quiz_id = "BEM460_C1_FinalQuizq",
             course_id = "LNR16",
             total_marks = "30"
        )
        is_pass = result.final_check_pass(learner_marks)
        self.assertEqual(is_pass,1)

class TestChapter_Quiz(unittest.TestCase):
    def test_check_pass_pass(self):
        chapter_quiz_1 = Chapter_Quiz(
            quiz_id="BEM460_C1_Chapt1q",
            chapter_id="BEM460_C1_Chapt1",
            total_marks = "10"
        )
        result = chapter_quiz_1.check_pass(9)
        self.assertEqual(result,1)
    
    def test_check_pass_fail(self):
        chapter_quiz_1 = Chapter_Quiz(
            quiz_id="BEM460_C1_Chapt1q",
            chapter_id="BEM460_C1_Chapt1",
            total_marks = "10"
        )
        result = chapter_quiz_1.check_pass(4)
        self.assertEqual(result,0)

"""
Veronica Teng led this testing
"""
class TestChapter_Learner(unittest.TestCase):
    def test_json_completion_test_case_1(self):
        chapter_learner_1 = Chapter_Learner(chapter_id="BEM460_C1_Chapt1", learner_id="LNR17",
        completion=1)
        self.assertEqual(chapter_learner_1.json(), {
            'chapter_id' : "BEM460_C1_Chapt1",
            "learner_id" : "LNR17",
            "completion": 1
            })

    def test_json_completion_test_case_2(self):
        chapter_learner_1 = Chapter_Learner(chapter_id="BEM460_C1_Chapt1", learner_id="LNR17",
        completion=0)
        self.assertEqual(chapter_learner_1.json(), {
            'chapter_id' : "BEM460_C1_Chapt1",
            "learner_id" : "LNR17",
            "completion": 0
            })

    def test_update_completion(self):
        chapter_learner_1 = Chapter_Learner(
            chapter_id = "BEM460_C1_Chapt1",
            learner_id = "LNR17",
            completion = "0"
        )
        chapter_learner_1.update_completion()
        ###can see that completion from 0 become 1
        self.assertEqual(chapter_learner_1.completion,1)

class TestChapter(unittest.TestCase):
    def test_json(self):
        chapter_1 = Chapter(course_id="BEM460", chapter_id="BEM460_C1_Chapt1")
        self.assertEqual(chapter_1.json(), {
            'course_id' : "BEM460",
            "chapter_id" : "BEM460_C1_Chapt1"
            })
    

if __name__ == "__main__":
    unittest.main()

