# Learning Management System (LMS)
<Summarize what your software does in the introductory paragraph>

## Getting Started
<Include a detailed spin-up process with instructions for installing any software the application is dependent on (such as wkhtmlopdf, PostgreSQL, XQuartz). Give instructions on running the app. Finally, include information about subdomains in the app (e.g., api.myapp.dev/), other tools configuration (e.g. Stripe, Amazon), and test data info. This way you will let the developer start working with on your project faster.>
<br><br><br>


## Assumption
- Trainer cannot create quiz after the class start date
- Trainer can only create chapter 2 if chapter 1 is already created
- Pre-assignment will be done manually, normally before the registration date [Piazza @136](https://piazza.com/class/kqq5xowd6cj3ov?cid=136)
- Trainers are assigned before the registration date.
- Trainers can to upload the course material before the registration start date.


<br><br><br>

## Targeted Users
Our LMS targets 3 different users and allows user to do the below actions.
| Employee Type       | Description                                                            |
| -----------         | -----------                                                            |
| Trainer             | Able to create assessments. Consist of senior engineer.                |
| Learner             | Able to enroll themselves into eligible courses and attend the classes online. Consist of both engineers and senior engineers.                                        |
| Human Resource      | Able to assign engineers to created classes.                           |
<br><br>

## 1. Human Resource (HR)
<p align="center">
  <img src="frontend\static\img\markdown/hr_sitemap.png" width="700"/> <br>
  <i>HR's Sitemap</i>
</p>
<br>

### Steps
1. Log into your account through the [Login Page](https://spm-lms-team4.s3.amazonaws.com/templates/login.html).
    - Click on "Log in as HR"
2. View a course.
    - Click on the "View Course" button for **BEM460** or **EM140**. These courses have classes that are within the registration period
3. View a class.
    - Click on "View Class" button
4. Please click on the following tabs based on your decided action.

    A. Preassign Learner
    - Click on "PREASSIGN LEARNERS" tab
    - Press "Preassign" without any inputs. An unsuccessful alert will pop up
    - Input "18" as the Learner ID. A success alert will pop up.

    B. Assign Learner
    - Click on "REGISTERED LEARNERS" tab
    - Press "Approve" for any learner. The number of slots left will be updated and the learner will appear under "ENROLLED LEARNERS" tab

    C. Withdraw Learner
    - Click on "ENROLLED LEARNERS" tab
    - Press "Approve" for any learner. The number of slots left will be updated and learner will no longer be enrolled in the course

<br><br><br>

## 2. Trainer
<p align="center">
  <img src="frontend\static\img\markdown/tnr_sitemap.png" width="700"/> <br>
  <i>Trainer's Sitemap</i>
</p>
<br>



### Steps
1. Log into your account through the [Login Page](https://spm-lms-team4.s3.amazonaws.com/templates/login.html).
    - Trainer ID: TNR4 <br><br>
2. Your homepage displays the classes that you are currently teaching. You can either view or create a quiz.
3. Please click on the following classes based on your decided action.
   - View Quiz: EM140 Basic Engineering Management > View Quiz
   - Create Quiz: BEM460 Basic Engineering Management > Create Quiz



<br><br><br>

## 3. Learner
| Title                | User Story                                                                                  |
| -----------          | -----------                                                                                 |
| Take Final Quiz for Course                              | insert                                                   |
| Take Quizzes for Course Sections                        | insert                                                   |
| View Course Materials by different chapters             | insert                                                   |
| Engineers can view the status of the registered courses | insert                                                   |
<br>

insert insert steps
<br><br><br>
