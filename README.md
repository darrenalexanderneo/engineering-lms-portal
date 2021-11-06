# Learning Management System (LMS)
<Summarize what your software does in the introductory paragraph>

## Getting Started
<Include a detailed spin-up process with instructions for installing any software the application is dependent on (such as wkhtmlopdf, PostgreSQL, XQuartz). Give instructions on running the app. Finally, include information about subdomains in the app (e.g., api.myapp.dev/), other tools configuration (e.g. Stripe, Amazon), and test data info. This way you will let the developer start working with on your project faster.>
<br><br><br>


## Assumption
- Trainer cannot create quiz after the class start date
- Trainer can only create chapter 2 if chapter 1 is already created
- Preassignment will be done manually, normally before the registration date [Piazza @136](https://piazza.com/class/kqq5xowd6cj3ov?cid=136)

<br><br><br>

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
| Take Final Quiz for Course                              | insert                                                   |
| Take Quizzes for Course Sections                        | insert                                                   |
| View Course Materials by different chapters             | insert                                                   |
| Engineers can view the status of the registered courses | insert                                                   |
<br>

insert insert steps
<br><br><br>

### C. Human Resource
| Title                | User Story                                                                                                    |
| -----------          | -----------                                                                                                   |
| Assign Learners | As a HR, I want to be able to enroll and withdraw the trainers to classes based on their availability so that the trainers can start preparing their course materials.                                                                                   |
| Preassign Learners   | As a HR, I want to be able to preassign learners into prerequisite courses so that I can prioritise their enrollments into the course.                                                                                                           |
<br>

Log into your account through the [Login Page](http://localhost/is212-spm-team4/frontend/templates/learner/login.html). 
Please use