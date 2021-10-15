//initialise localStorage
const storage = window.localStorage;

//hardcoded learner_id because learner login is not implemented yet
const learner_id = "LNR8";

// USE LOCALSTORAGE AFTER LEARNER LOGIN IS IMPLEMENTED
// storage.setItem("learner_id", "LNR8");
// const learner_id = storage.getItem("learner_id");


var course_id;


//initialise global variables to store api keys
var getCoursesforRegistration;
var getCourseDetails;
var getClassesByEnrollmentStatus;
var getEnrollmentStatus;
var register_POST;
var withdraw_POST;

// to retrieve api keys without exposing
function getAPIkeys () {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getCoursesforRegistration = api_keys.getCoursesforRegistration;
            getCourseDetails = api_keys.getCourseDetails;
            getClassesByEnrollmentStatus = api_keys.getClassesByEnrollmentStatus;
            getEnrollmentStatus = api_keys.getEnrollmentStatus;
            register_POST = api_keys.register_POST;
            withdraw_POST = api_keys.withdraw_POST;

            console.log(getCoursesforRegistration);
            console.log(getCourseDetails);
            console.log(getClassesByEnrollmentStatus);
            console.log(getEnrollmentStatus);
            console.log(register_POST);
            console.log(withdraw_POST);
        }
    }
    request.open("GET", "../../apikey.json", false);
    request.send();
}

function renderCourseDetailsPage () {
    getAPIkeys();

    course_id = storage.getItem("course_id"); 
    console.log(course_id);

    viewCourseDetails(course_id);
    showClassesforRegistration(course_id, learner_id);

}

document.addEventListener("DOMContentLoaded", renderCourseDetailsPage()); 

function viewCourseDetails (course_id) {

    document.getElementById("course_name").innerHTML = "";
    document.getElementById("course_desc").innerHTML = "";
    document.getElementById("prereq_courses").innerHTML = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var course_details = JSON.parse(this.response).data;
            console.log(course_details);
            var prereq_content = "";

            var course_description = course_details.course_description;
            var course_name = course_details.course_name;
            var num_of_slots = course_details.num_of_slots;
            var prereq_courses = course_details.prereq_courses;  // string  
            
            if (prereq_courses == "") {
                prereq_content = "None";
            } else {
                var prereq_array = prereq_courses.split(",");
                for (course of prereq_array) {
                    prereq_content += `<li>${course}: Prerequisite Course Name</li>`;
                }
            }

            document.getElementById("course_name").innerHTML = course_name;
            document.getElementById("course_desc").innerHTML = course_description;
            document.getElementById("prereq_courses").innerHTML = prereq_content;

        }
    };

    var url = getCourseDetails + course_id;
    console.log(url);
    request.open("GET", url, true);
    request.send();
}

function showClassesforRegistration (course_id, learner_id) {
    
    document.getElementById("message").innerHTML = "";
    document.getElementById("classes-container").innerHTML = "";
    
    var message = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var classes = JSON.parse(this.response);
            console.log(classes);

            if (classes.is_approved == 1) {
                //already enrolled
                message += `<li>${classes.message}</li>`;
            } if (classes.is_approved == 2) {
                // already completed
                message += `<li>${classes.message}</li>`;

            } if (classes.is_approved == 3) {
                //have not completed prerequisites yet
                message += `<li>${classes.message}</li>`;

            } else {
                console.log(classes.message);

                var html_content = "";

                for (eachClass of classes.results) {

                    var class_id = eachClass.class_id;
                    var class_start_date = eachClass.class_start_date;
                    var class_end_date = eachClass.class_end_date;
                    var num_of_slots = eachClass.num_of_slots;  
                    var reg_start_date = eachClass.reg_start_date;  
                    var reg_end_date = eachClass.reg_end_date;  
                    var is_registered = eachClass.is_registered;  // boolean value
                    console.log(class_id);
                    console.log(is_registered);

                    var class_name = class_id.split("_")[1];  //output = C1
                    var class_num = class_name.replace('C', '');

                    html_content += 
                    `<div class="row">
                        <!-- left -->
                        <div class="col-9">
                            <h5>Class ${class_num}</h5>
                            <!-- class details -->
                            <div class="row">
                                <div class="col-3">
                                    <span>Professor:</span> <br>
                                    <span>Registration Period:</span> <br>
                                    <span>Class Period: </span> <br>
                                </div>
                                <div class="col-9">
                                    <span>Chris Poskitt</span> <br>
                                    <span> ${reg_start_date} to ${reg_end_date} </span> <br>
                                    <span> ${class_start_date} to ${class_end_date}</span> <br>
                                </div>
                            </div>
                        </div>
                        <!-- right -->
                        <div class="col-3 d-flex flex-column" >
                            <span class="d-flex text-center" style="justify-content: flex-end;">${num_of_slots} out of 50 taken</span>`;

                    if (is_registered == 0) {
                        html_content +=`<button onclick="register('${class_id}','${course_id}','${learner_id}', '${class_num}')" class="btn btn-outline-primary text-center align-self-end" style="margin-top:auto">Register</button>`;  
                    }  
                    else { //disable button
                        html_content +=`<button class="btn btn-outline-primary text-center align-self-end" disabled style="margin-top:auto">Registered</button>`;
                    }    

                    html_content += `</div></div>`;

                    if (eachClass !== classes.results[classes.results.length - 1]) {
                        html_content += `<hr>`;
                    }

                }
            } 
            if (classes.is_approved == 0) {
                document.getElementById("classes-container").innerHTML = html_content;
                document.getElementById("message-container").style.display = "none";
            } else {
                document.getElementById("message").innerHTML = message;
                document.getElementById("classes-container").style.display = "none";

            } 
        }


    }

    var url = `${getClassesByEnrollmentStatus}${course_id}/${learner_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();
}

function register (class_id, course_id, learner_id, class_num) {
    console.log(class_id);
    console.log(course_id);
    console.log(learner_id);
    console.log(class_num);

    // creating JSON Object to do POST HTTP request 
    var post_obj = {
                    class_id: class_id,
                    course_id: course_id,
                    learner_id: learner_id
                };
    var json_string = JSON.stringify(post_obj); // stringify json object into a string
    console.log(json_string);

    // create POST HTTP request
    var request = new XMLHttpRequest();
            
    request.onreadystatechange = function () {

        var message = "";
        var html_content = "";

        if (this.readyState == 4 && this.status == 200) {

            message = JSON.parse(this.response).message;
            console.log(message);
            html_content = `<br><div class="alert alert-success alert-dismissible fade show" role="alert">
                            You have successfully registered for ${course_id} - Class ${class_num}!
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div><br>`;
            
        } else if (this.readyState == 4 && this.status == 201) {
            message = JSON.parse(this.response).message;
            console.log(message);
            html_content = `<br><div class="alert alert-danger alert-dismissible fade show" role="alert">
                            ${course_id} - Class ${class_num} is currently full. <br>
                            Try registering for other available classes.
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                            </div><br>`;
        } else {
            console.log("code: 500 - code is not 200 or 201")
        }
        document.getElementById("registration-alert").innerHTML = html_content;
        renderCourseDetailsPage();

    }

    var url = register_POST;
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(json_string);
}

function goBackTo (prev_page) {

    var current_location_arr = window.location.href.split("/");
    var current_location = current_location_arr[current_location_arr.length - 1];

    if (prev_page == "viewcourses" && current_location == "class_registration.html") {
        console.log(prev_page);
        window.location.replace("view_reg_courses.html");
    } 
}