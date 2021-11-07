# G6T4 - Learning Management System (LMS)
<Summarize what your software does in the introductory paragraph>

## Getting Started
<!-- <Include a detailed spin-up process with instructions for installing any software the application is dependent on (such as wkhtmlopdf, PostgreSQL, XQuartz). Give instructions on running the app. Finally, include information about subdomains in the app (e.g., api.myapp.dev), other tools configuration (e.g. Stripe, Amazon), and test data info. This way you will let the developer start working with on your project faster.> -->
1. Go to our [Website](https://spm-lms-team4.s3.amazonaws.com/templates/login.html)
2. Follow the instructions in the <b>User Journey</b> below
<br><br>

## Assumption
- Trainer cannot create quiz after the class start date
- Trainer can only create chapter 2 if chapter 1 is already created
- Pre-assignment will be done manually, normally before the registration date [Piazza @136](https://piazza.com/class/kqq5xowd6cj3ov?cid=136)
- Trainers are assigned before the registration date.
- Trainers can to upload the course material before the registration start date.
- All classes have total registration slots of 50

<br>

## User Journey
Our LMS targets 3 different users and allows user to do the below actions.
| Employee Type       | Description                                                            |
| -----------         | -----------                                                            |
| Trainer             | Able to create assessments. Consist of senior engineer.                |
| Learner             | Able to enroll themselves into eligible courses and attend the classes online. Consist of both engineers and senior engineers.                                        |
| Human Resource      | Able to assign engineers to created classes.                           |
<br><br><br>

### A. Trainer
| Title                | User Story                                                          |
| -----------          | -----------                                                            |
| Create Ungraded Quiz | As a Trainer, I want to be able to set the format of each question for each quiz, so that I can choose the settings best suited for each individual question. online. Consist of both engineers and senior engineers.                                                 |
| Create Final Quiz    | As a Learner, I want to be able to take the final quiz for a course, so that I can successfully complete the course.                                                    |
| Auto Grade Quiz      | As a trainer, I want each quiz to be auto-graded, so that I save time from cross-checking through every question.                                                     |
<br>

Log into your account through the [Login Page](http://localhost/is212-spm-team4/frontend/templates/learner/login.html). Please use TNR1, TNR? and TNR? for testing purposes.
<p align="center">
  <img src="frontend\static\img\markdown\login_page.png" width="700"/>
</p>

Choose any of the courses listed.
<p align="center">
  <img src="frontend\static\img\markdown\tnr_homepage.png" width="700"/>
</p>

You will be able to create quizzes for your classes. Once the quiz is created, you can view the quizzes you have created. You can no longer modify the quiz once it is created. The pages will look like the below.
View Quiz            |  Create Quiz
:-------------------------:|:-------------------------:
![](frontend\static\img\markdown\tnr_view_quiz.png)  |  ![](frontend\static\img\markdown\tnr_create_quiz.png)
<br><br><br>

### B. Learner
| Title                | User Story                                                                                  |
| -----------          | -----------                                                                                 |
|Engineers can view all courses                             | As an engineer, I would want to view all available courses with descriptions, so I can decide which are the courses I am interested in.                                                  |
Engineers can register for interested courses|   As an engineer, I want to be able to register for the courses by entering the necessary registration details, so I can attend the courses.           |
| Engineers can view the status of the registered courses | As an engineer, I want to view the status of my registered courses, so I can register for other classes of the same course if my registration(s) is/are unsuccessful.                                            |  
| Engineers can withdraw from the classes they have registered for |     As an engineer, I want to be able to withdraw from the classes I have registered for previously, so I do not have to worry about signing up for the wrong class accidentally.                   |
| View Course Materials by different chapters             | As a Learner, I want to be able to access course details that I have enrolled under, in order to be able to track my personal progress.                                           |   
| Take Quizzes for Course Sections     |As a Learner, I want to be able to take the quizzes as many times as possible so that I can pass it.                                             |
| Take Final Quiz for Courses     |As a Learner, I want to be able to take the final quiz for a course, so that I can successfully complete the course.                         |

                                                                                                                               
<br>

#### Step 1:<br>
Log into your account through the [Login Page](https://spm-lms-team4.s3.amazonaws.com/templates/login.html). Please use LNR8, LNR9, LNR10, LNR11, LNR12 as the Learner ID for testing purposes.
<p align="center">
  <img src="frontend\static\img\markdown\login_page.png" width="700"/>
</p>

#### Step 2: <br>
You will be directed to the Browse Courses tab on the page. You will be able to see the courses that are currently available for registration. Click on  <b>Learn More</b> for any of the courses below to view the relevant course details as well as your eligibility to register for the course as a particular learner.

<p align="center">
  <img src="frontend\static\img\markdown\lnr_browse_courses.png" width="700"/>
</p>

#### Step 3a: <br>
If you are eligible to register for the course, a list of classes will be shown to you. You will be able to register for multiple classes of the same course as well. Simply click on the <b>Register</b> button to register.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_register_class.png" width="700"/>
</p>
 
##### * If you have registered or if the class is already full, you will not be able to register.
<br>

#### Step 3b:<br>
There are some cases which may not allow you to register for a class. If you encounter any one of these, click on the <b>back button icon</b> on the screen and choose another course that you are eligible to register for.

Uncompleted Prerequisites | Already Enrolled | Already Completed |
:-------------------------:|:-------------------------:|:-------------------------:|
![](frontend\static\img\markdown\lnr_register_prereq.png)  |  ![](frontend\static\img\markdown\lnr_register_enrolled.png) |  ![](frontend\static\img\markdown\lnr_register_completed.png) |
|

#### Step 4:

In order to check the status of your registrations, click on the <b>View/Change Status</b> tab on the navigation bar. You can see your approved or pending registrations here.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_viewstatus.png" width="700"/>
</p>

#### Step 5:

Next, you can also withdraw your registrations if you want to cancel them. Simply click on the <b>Withdraw</b> button beside any registration record you want to cancel. Click on <b>Withdraw</b> again to confirm.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_withdraw_reg.png" width="700"/>
</p>


#### Step 6:

Moving on, we want to view the course materials of our successfully enrolled courses. Click on the <b>Enrolled Courses</b> tab on the navigation bar. Next, click on the <b>Select a Course</b> Dropdown Bar and select "BEM460 - Basic Engineering Management".
<p align="center">
  <img src="frontend\static\img\markdown\lnr_viewenrolledcourses.png" width="700"/>
</p>

There are multiple versions of this Course Materials page based on each Learner's course progress as shown below. 
Quizzes Not Attempted | Quizzes Attempted
:-------------------------:|:-------------------------:|
![](frontend\static\img\markdown\lnr_unattemptedChapters.png)  |  ![](frontend\static\img\markdown\lnr_attemptedAll.png)|
|   Click on <b>Learn</b> button to start learning (Have to attempt current quiz to unlock the next chapter)| Click on <b>View</b> to revise chapter materials| 
|       -   |    Click on <b>Practise</b> to reattempt chapter quizzes  |
|     

#### Step 7: View & Learn Course Materials

 When you click on <b>View</b> or <b>Learn</b> from the previous page, you will see a PDF containing the chapter materials.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_viewmaterials.png" width="700"/>
</p>

#### Step 8: Attempt/Practise Quizzes (This applies to Final Quizzes as well)

If you clicked on <b>Learn</b> previously, scroll down all the way and click the <b>Take Quiz</b> button to attempt the quiz.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_takequizbtn.png" width="700"/>
</p>
This is an example of what a quiz looks like. In order to submit the quiz, you have to attempt all the questions.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_quiz.png" width="700"/>
</p>
Once you finish the quiz, scroll down all the way and click on the <b>Submit Quiz</b> button.
<p align="center">
  <img src="frontend\static\img\markdown\lnr_submitquiz.png" width="700"/>
</p>

<br><br><br>
<br><br><br>

### C. Human Resource
| Title                | User Story                                                                                                    |
| -----------          | -----------                                                                                                   |
| Assign Learners | As a HR, I want to be able to enroll and withdraw the trainers to classes based on their availability so that the trainers can start preparing their course materials.                                                                                   |
| Preassign Learners   | As a HR, I want to be able to preassign learners into prerequisite courses so that I can prioritise their enrollments into the course.                                                                                                           |
<br>

Log into your account through the [Login Page](http://localhost/is212-spm-team4/frontend/templates/learner/login.html). 
Please use