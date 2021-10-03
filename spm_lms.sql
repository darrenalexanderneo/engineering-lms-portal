CREATE TABLE role (
    role_id int(11) NOT NULL,
    role_desc varchar(50) NOT NULL,
    PRIMARY KEY (role_id)
);




CREATE TABLE employee (
  emp_id char(10) NOT NULL,
  emp_name varchar(50) NOT NULL,
  role_id varchar(50) NOT NULL,
  PRIMARY KEY(emp_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE trainers (
  emp_id char(10) NOT NULL,
  course_id char(10) NOT NULL,
  class_id char(10) NOT NULL,
  completed int(3) NOT NULL,
  PRIMARY KEY(emp_id, course_id, class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE learners (
  emp_id char(10) NOT NULL,
  course_id char(10) NOT NULL,
  class_id char(10) NOT NULL,
  completed int(3) NOT NULL,
  PRIMARY KEY(emp_id, course_id, class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE classes (
  class_id char(10) NOT NULL,
    course_id char(10) NOT NULL,
    start_date varchar(50) NOT NULL,
    end_date varchar(50) NOT NULL,
    slots_available int(10) NOT NULL,
    class_size int(10) NOT NULL,
    PRIMARY KEY(class_id, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE courses (
    course_id char(10) NOT NULL,
    course_name varchar(50) NOT NULL,
    course_desc varchar(255) NOT NULL,
    prerequisite int(3) NOT NULL,
    PRIMARY KEY(course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




CREATE TABLE course_registration (
    course_id char(10) NOT NULL,
    class_id char(10) NOT NULL,
    emp_id char(10) NOT NULL,
    pre_assigned int(3) NOT NULL,
    PRIMARY KEY(course_id, class_id, emp_id)
);



CREATE TABLE registration (
    course_id char(10) NOT NULL,
    reg_start_date varchar(50) NOT NULL,
    reg_end_date varchar(50) NOT NULL,
    class_id char(10) NOT NULL,
    PRIMARY KEY(course_id, class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE course_prerequisite (
    course_id char(10) NOT NULL,
    prereq_course_id char(10) NOT NULL,
    PRIMARY KEY(course_id, prereq_course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE trainers_course (
    course_id char(10) NOT NULL,
  class_id char(10) NOT NULL,
    emp_id char(10) NOT NULL,
    PRIMARY KEY(course_id, class_id, emp_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO role (`role_id`, `role_desc`) VALUES
(1, 'Human Resource'),
(2, 'Senior Engineer'),
(3, 'Engineer');

INSERT INTO employee (`emp_id`, emp_name, `role_id`) VALUES
('EMP1', 'Veronica Teng', '1'),
('EMP2', 'Darren Neo Yong Yi', '2'),
('EMP3', 'Teoh Jia Xing', '3'),
('EMP4', 'Erh Qin Yu Lewanna', '3'),
('EMP5', 'Au Yong Ting Ting', '3'),
('EMP6', 'Tom Poskitt', '2'),
('EMP7', 'Jay Kay', '3'),
('EMP8', 'Tongkat Ali', '2'),
('EMP9', 'Karen Ong', '3'),
('EMP10', 'Vanessa Lee', '3'),
('EMP11', 'Johnson Lee', '3'),
('EMP12', 'Hong Hock Seng', '3'),
('EMP13', 'Muhammad Ali', '3');

INSERT INTO learners (emp_id, course_id, class_id, `completed`) VALUES
('EMP4', 'BEM460', 'C1', 1),
('EMP4', 'EM140', 'C1', 1),
('EMP5', 'BEM460', 'C3', 0),
('EMP9', 'BEM460', 'C3', 0);

INSERT INTO classes (`class_id`, course_id, start_date, end_date, slots_available, `class_size`) VALUES
('C1', 'BEM460', '2021-02-07', '2021-04-30', 0, 50),
('C2', 'BEM460', '2021-03-07', '2021-05-30', 0, 50),
('C3', 'BEM460', '2021-09-09', '2021-11-11', 0, 50),
('C4', 'BEM460', '2021-10-30', '2021-12-30', 50, 50),
('C1', 'EM140', '2021-04-01', '2021-06-01', 0, 50),
('C2', 'EM140', '2021-05-01', '2021-07-01', 0, 50),
('C3', 'EM140', '2021-10-10', '2021-12-01', 50, 50),
('C1', 'EE200', '2021-11-01', '2022-01-30', 50, 50),
('C1', 'CE100', '2021-10-30', '2021-12-30', 50, 50);

INSERT INTO courses (`course_id`, course_name, course_desc, `prerequisite`) VALUES
('BEM460', 'Basic Engineering Management', 'Learning the basic concepts of engineering. In addition, \nreal life concepts will be introduced as well.', 0),
('EM140', 'Engineering Management', 'Develop and build analog electronics circuits. You awill build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n', 0),
('EE200', 'Electricity & Electronics', 'Develop and build analog electronics circuits. You will build multiple \ncircuits from sound buzzers to bionics where we actually control a servo motor by reading signals from your muscles\n', 1),
('CE100', 'Computer Engineering', 'You will also be prepared for internationally recognised industry certification examinations such as those from National Instruments, UI Path, Microsoft and Unity3D\n', 1);

INSERT INTO course_registration (`course_id`, class_id, emp_id, `pre_assigned`) VALUES
('BEM460', 'C4', 'EMP11', 0),
('BEM460', 'C4', 'EMP12', 0),
('BEM460', 'C4', 'EMP13', 1),
('EM140', 'C3', 'EMP7', 0),
('EM140', 'C3', 'EMP10', 0),
('EM140', 'C3', 'EMP13', 0),
('CE100', 'C1', 'EMP4', 1),
('EE200', 'C1', 'EMP4', 0);

INSERT INTO registration (`course_id`, reg_start_date, reg_end_date, `class_id`) VALUES
('BEM460', '2021-09-30','2021-10-20', 'C4'),
('EM140', '2021-09-01','2021-09-15', 'C3'),
('EE200', '2021-09-30','2021-10-30', 'C1'),
('CE100', '2021-10-01','2021-10-20', 'C1');

INSERT INTO course_prerequisite (`course_id`, `prereq_course_id`) VALUES
('EE200', 'EM140'),
('EE200', 'BEM460'),
('CE100', 'EM140');


INSERT INTO `trainers_course` (`course_id`, `class_id`, `emp_id`) VALUES
('EE200', 'C1', 'EMP8');

INSERT INTO `trainers` (`emp_id`, `course_id`, `class_id`, `completed`) VALUES
('EMP1', 'EM140', 'C1', 1),
('EMP3', 'BEM460', 'C1', 0),
('EMP2', 'BEM460', 'C2', 0);
