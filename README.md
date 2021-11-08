# G6T4 - Learning Management System (LMS)
<Summarize what your software does in the introductory paragraph>

## Getting Started
<!-- <Include a detailed spin-up process with instructions for installing any software the application is dependent on (such as wkhtmlopdf, PostgreSQL, XQuartz). Give instructions on running the app. Finally, include information about subdomains in the app (e.g., api.myapp.dev), other tools configuration (e.g. Stripe, Amazon), and test data info. This way you will let the developer start working with on your project faster.> -->
1. Go to our [Website](https://spm-lms-team4.s3.amazonaws.com/templates/login.html)
2. Follow the instructions in the <b>User Journey</b> below
<br><br>

## ONLY IF: want to review from our local database, to establish connection to local database: 
1. Create a .env file in same directory as README
2. Import spm_lms_finaldb.sql file into local database 
3. Paste "dbURL=mysql+mysqlconnector://root:root@localhost:8888/spm_lms" ,database for our main application data
4. Paste "testURLRDS =mysql+mysqlconnector://root:root@localhost:8888/testdb" ,database use for integration testing.

## IF YOU WISH to connect to your own local database 
1. Do ensure that the following are installed on your device. 
  - wamp
  - mysql/workbench (Ensure your sql port is 8888)
2. Ensure wamp is switched on and mysql is working fine 
3. Download spm_lms_finaldb.sql file 
4. Run requirements.txt
5. Import spm_lms_finaldb.sql file into mysql 
6. Create .env and paste the following inside the file 
  - xx
  - xx
7. Proceed to backend folder to change dburl to ___ and run app.py

## Assumption
- Trainer cannot create quiz after the class start date
- Trainer can only create chapter 2 if chapter 1 is already created
- Pre-assignment will be done manually, normally before the registration date [Piazza @136](https://piazza.com/class/kqq5xowd6cj3ov?cid=136)
- Trainers are assigned before the registration date.
- Trainers can to upload the course material before the registration start date.
- All classes have total registration slots of 50

<br>

## Targeted Users
Our LMS targets 3 different users and allows user to do the below actions.
| Employee Type       | Description                                                            |
| -----------         | -----------                                                            |
| Trainer             | Able to create assessments. Consist of senior engineer.                |
| Learner             | Able to enroll themselves into eligible courses and attend the classes online. Consist of both engineers and senior engineers.                                        |
| Human Resource      | Able to assign engineers to created classes.                           |


<br><br><br>

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

    **Successful Attempt**
    - Click on "PREASSIGN LEARNERS" tab
    - Press "Preassign" without any inputs. An unsuccessful alert will pop up
    - Input "18" as the Learner ID
      - A success alert will pop up
      - The learner will appear under "ENROLLED LEARNERS" tab
      
    **Unsuccessful Attempt**
    - Press "Preassign" again with 18 as the Learner ID
      - An unsuccessful alert will pop up
    

    B. Assign Learner
    - Click on "REGISTERED LEARNERS" tab
    - Press "Approve" for any learner
      - The number of slots left will be updated
      - The learner will appear under "ENROLLED LEARNERS" tab

    C. Withdraw Learner
    - Click on "ENROLLED LEARNERS" tab
    - Press "Approve" for any learner.
      - The number of slots left will be updated
      - The learner will no longer be enrolled in the course

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

   A. View Quiz
   - Click on EM140 Class 1
   - Click on "View Quiz" button. You will see the questions created for the selected chapter
  

    B. Create Quiz
    - Click on the "View Course" button for BEM460 Basic Engineering Management Class 4
    - Click on the "Create Quiz" button
    - You are able to do the following when creating a quiz:
      - Modify the duration of the quiz
      - Modify the number of questions: Click on "Add a Question" or "Delete" button
      - Modify the question type
      - Modify the number of options for MCQ questions
      - Modify the marks for each question

<br><br><br>

## 3. Learner
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
