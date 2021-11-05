# Learning Management System (LMS)
<Summarize what your software does in the introductory paragraph>

## Getting Started
<Include a detailed spin-up process with instructions for installing any software the application is dependent on (such as wkhtmlopdf, PostgreSQL, XQuartz). Give instructions on running the app. Finally, include information about subdomains in the app (e.g., api.myapp.dev/), other tools configuration (e.g. Stripe, Amazon), and test data info. This way you will let the developer start working with on your project faster.>

## User Journey
Our LMS targets 3 different users and allows user to do the below actions.
| Employee Type       | Description                                                            |
| -----------         | -----------                                                            |
| Learner             | Able to enroll themselves into eligible courses and attend the classes online. Consist of both engineers and senior engineers.                                        |
| Trainer             | Able to create assessments. Consist of senior engineer.                |
| Human Resource      | Able to assign engineers to created classes.                           |

### A. Learner
some paragraph

### B. Trainer
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