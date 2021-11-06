//initialise localStorage
const storage = window.localStorage;

//hardcoded learner_id because learner login is not implemented yet
// const learner_id = "LNR8";  

// USE LOCALSTORAGE AFTER LEARNER LOGIN IS IMPLEMENTED
// storage.setItem("learner_id", "LNR8");
const learner_id = storage.getItem("learner_id");


//initialise global variables to store api keys
var getCoursesforRegistration;
var getCourseDetails;
var getClassesByEnrollmentStatus;
var getEnrollmentStatus;
var register_POST;
var withdraw_POST;

document.getElementById("learner-id").innerHTML = learner_id;


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


function getCourseCards () {
    getAPIkeys();

    document.getElementById("cards").innerHTML = "";

    var html_content = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var course_list = JSON.parse(this.response).course_list;
            console.log(course_list);


            for (course of course_list) {
                console.log(course);
                var course_id = course.course_id;
                var course_name = course.course_name;
                var course_desc = course.course_desc;
                var prereq_courses = course.prereq_courses;  // string   
                
                if (prereq_courses == "") {
                    prereq_courses = "None";
                }
                
                html_content += 
                `<div class="col">
                    <div class="card">
                        <img src="https://source.unsplash.com/user/thisisengineering/daily" class="card-img-top img-fluid" alt="${course_name}">
                        <div class="card-body">
                            <h4 class="card-title">${course_name}</h4>
                            <h5 class="card-title">${course_id}</h5>
                            <p class="card-text">${course_desc}</p>
                            <h6 class="card-subtitle fw-bold">Pre-requisites: ${prereq_courses}</h6><br>
                            <button onclick="redirect_to_classRegistration('${course_id}', '${learner_id}')" class="btn btn-outline-primary float-end">Learn More</button>
                        </div>
                    </div>
                </div>`;
            }
            
            document.getElementById("cards").innerHTML = html_content;
        }
    };

    var url = getCoursesforRegistration;
    request.open("GET", url, true);
    request.send();
}

function redirect_to_classRegistration(course_id) {
    storage.setItem("course_id",course_id);

    setTimeout(function () { 
        const courseid = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseid);
        window.location.replace("class_registration.html");  // redirect to class_registration.html 
    }, 1000);
}

function logout () {
    storage.clear();

    window.location.replace("../login.html");
}