import unittest
from datetime import datetime
# from app import Employee, Senior_Engineer, Engineer, Trainer, Completion_Record, Course, Course_Prerequisite, Class_Run, Trainer_Record, Class_Record, Registration
from app import *


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
            'reg_end_date': "2021-04-30"
        })




if __name__ == "__main__":
    unittest.main()

