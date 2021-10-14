//hardcoded learner_id because learner login is not implemented yet
const learner_id = "LNR15"  

var course_id;

//initialise localStorage
const storage = window.localStorage;

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

document.addEventListener("DOMContentLoaded", function renderCourseDetailsPage () {
    getAPIkeys();

    course_id = storage.getItem("course_id"); 
    console.log(course_id);

    viewCourseDetails(course_id);
    showClassesforRegistration(course_id, learner_id);

}) 

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
    // document.getElementById("prereq_courses").innerHTML = "";
    
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
                                
                var html_content = "";

                var class_id = classes.results.class_id;
                var class_start_date = classes.results.class_start_date;
                var class_end_date = classes.results.class_end_date;
                var num_of_slots = classes.results.num_of_slots;  
                var reg_start_date = classes.results.reg_start_date;  
                var reg_end_date = classes.results.reg_end_date;  
                var is_registered = classes.results.is_registered;  // boolean value

                var class_name = class_id.split("_")[1];  // output = C1
                var class_num = class_name.replace('C', '');

                
                for (eachClass of classes.results) {
                    html_content += 
                    `<div class="row">
                        <!-- left -->
                        <div class="col-9">
                            <h5>Class ${class_num}</h5>
                            <!-- class details -->
                            <div class="row">
                                <div class="col-3">
                                    <span>Professor: PROFESSOR</span> <br>
                                    <span>Registration: ${reg_start_date} - ${reg_end_date} </span> <br>
                                    <span>Class: ${class_start_date} - ${class_end_date}</span> <br>
                                </div>
                                <div class="col-9">
                                    <span>Chris Poskitt</span> <br>
                                    <span>12 Aug 2021 - 14 Oct 2021</span> <br>
                                    <span>0 Jan 2022 - 28 Mar 2022</span> <br>
                                </div>
                            </div>
                        </div>
                        
                        <!-- right -->
                        <div class="col-3 d-flex flex-column" >
                            <span class="d-flex text-center" style="justify-content: flex-end;">${num_of_slots} out of 50 taken</span>`;
                    if (is_registered == 0) {
                        html_content +=`<button class="btn btn-outline-primary text-center align-self-end" style="margin-top:auto">Register</button>`;
                    }  else { //disable button
                        html_content +=`<button class="btn btn-outline-primary text-center align-self-end" disabled style="margin-top:auto">Register</button>`;
                    }    

                    html_content += `</div></div>`;
                }
            } 
            if (classes.is_approved == 0) {
                document.getElementById("classes-container").innerHTML = html_content;
            } else {
                document.getElementById("message").innerHTML = message;
            } 
        }


    }

    var url = `${getClassesByEnrollmentStatus}${course_id}/${learner_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();
}

function goBackTo (prev_page) {
    // console.log(prev_page);
    // console.log(window.location.href);
    var current_location_arr = window.location.href.split("/");
    var current_location = current_location_arr[current_location_arr.length - 1];
    // console.log(current_location);
    if (prev_page == "viewcourses" && current_location == "class_registration.html") {
        console.log(prev_page);
        window.location.replace("view_reg_courses.html");
    } 
}