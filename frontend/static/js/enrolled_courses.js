//initialise localStorage
const storage = window.localStorage;

const learner_id = storage.getItem("learner_id");

//initialise global variables to store api keys
var getCourseProgress;
var getAllChapters;
var getCourseCompletionStatus;
var getCompletedChapters;
var getEnrollmentStatus;

function renderPage () {
    getAPIkeys();
    displayCourseDropdown();
}

// to retrieve api keys without exposing
function getAPIkeys () {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getCourseProgress = api_keys.getCourseProgress;
            getAllChapters = api_keys.getAllChapters;
            getCourseCompletionStatus = api_keys.getCourseCompletionStatus;
            getCompletedChapters = api_keys.getCompletedChapters;
            getEnrollmentStatus = api_keys.getEnrollmentStatus;

            console.log(getCourseProgress);
            console.log(getAllChapters);
            console.log(getCourseCompletionStatus);
            console.log(getCompletedChapters);
            console.log(getEnrollmentStatus);

        }
    }
    request.open("GET", "../../apikey.json", false);
    request.send();
}

function displayCourseDropdown () {
    document.getElementById("course-dropdown").innerHTML = "";
    var html_content = `<option value="none" selected disabled>Select a Course</option>`;

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var course_list = JSON.parse(this.response).results;
            console.log(course_list);
            
            if (course_list.length == 0) {
                document.getElementById("message-container").innerHTML = "<h5>You Do Not Have Any Enrolled Courses Currently.</h5>";
            } else {
                for (course of course_list) {
                    console.log(course);
                    var course_id = course.course_id;
                    var course_name = course.course_name;
                    var class_id = course.class_id;
                    
                    html_content += 
                    `<option value="${class_id}">${course_id} - ${course_name}</option>`;
                }
                
                document.getElementById("course-dropdown").innerHTML = html_content;
            }
        }
    };

    var url = `${getEnrollmentStatus}${learner_id}`;
    request.open("GET", url, true);
    request.send();
}

function displayAllChapters (class_id) {

    var course_id = class_id.split("_")[0];
    console.log(course_id);
    showCourseProgressBar(course_id);

    document.getElementById("chapter-list").innerHTML = "";
    document.getElementById("message-container").innerHTML = "";

    var html_content = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var chapter_list = JSON.parse(this.response).results;
            console.log(chapter_list);

            var checkforFirst = 0;

            for (chapter of chapter_list) {
                console.log(chapter);
                var chapter_id = chapter.chapter_id;
                var chapter_name = "Chapter " + chapter_id.split("_")[2].replace("Chapt","");
                
                //invoke function to check if chapter is completed or not
                var status_html = ``;
                if (checkforCompletedChapters(class_id, chapter_id)) {
                    // chapter is completed
                    status_html = `<span style="margin-bottom: 0px;" class="badge bg-success rounded-pill px-2 py-2">Completed</span>`;

                } else { //chapter is not completed yet
                    if (checkforFirst == 0) { //only enable "Learn" button for first uncompleted chapter
                        status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}')" class="btn btn-outline-primary rounded-pill">Learn</button>`;
                        checkforFirst = 1;
                    } else { //disable the other "Learn" buttons
                        status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}')" class="btn btn-outline-primary rounded-pill disabled">Learn</button>`;
                    }   
                }
    
                html_content += 
                `<li class="list-group-item d-flex py-3 align-items-center">
                    <div class="ms-2 me-auto"><h5 class="">${chapter_name}</h5></div>
                    ${status_html}
                </li>`;
            }
            
            document.getElementById("chapter-list").innerHTML = html_content;
        }
    };

    var url = `${getAllChapters}${class_id}`;
    request.open("GET", url, true);
    request.send();
    
}

function checkforCompletedChapters (class_id, chapter_id) {

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var chapter_list = JSON.parse(this.response).results;
            console.log(chapter_list);

            var chapter_completed = false;

            for (var chapter of chapter_list) {
                console.log(chapter);
                var completion_status = chapter.completion;
                var chapterID = chapter.course_id;

                if (completion_status == 1 && chapterID == chapter_id) {
                    chapter_completed =  true;
                }
            }
            
            return chapter_completed; // true or false
        }
    };

    var url = `${getCompletedChapters}${class_id}/${learner_id}`;
    request.open("GET", url, true);
    request.send();
}

function showCourseProgressBar(course_id) {

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var course_progress = JSON.parse(this.response).progress_percentage;
            console.log(course_progress);

            document.getElementById("course-progress-label").innerHTML = `Course Progress:`;
            if (course_progress == 0) {
                document.getElementById("course-progress-bar").innerHTML = `<div class="progress rounded-pill bg-grey text-center" style="height: 30px; width: 35%;">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: ${course_progress}%;" aria-valuenow=" ${course_progress}" aria-valuemin="0" aria-valuemax="100"></div>
                <h6 class="mx-auto my-auto">${course_progress}%</h6></div>`;
            } else {
                document.getElementById("course-progress-bar").innerHTML = `<div class="progress rounded-pill bg-grey" style="height: 30px; width: 35%;">
                                        <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: ${course_progress}%;" aria-valuenow=" ${course_progress}" aria-valuemin="0" aria-valuemax="100"> ${course_progress}%</div>
                                        </div>`;
            }

            document.getElementById("course-progress-label").className -= `invisible`;
            document.getElementById("course-progress-bar").className -= `invisible`;
        }
    };

    var url = `${getCourseProgress}${course_id}/${learner_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();


}

function redirect_to_chapterContents(course_id,chapter_id) {
    storage.setItem("chapter_id",chapter_id);
    storage.setItem("course_id",course_id);

    setTimeout(function () { 
        const chapterID = storage.getItem("chapter_id"); 
        console.log("localStorage.getItem():" + chapterID);
        const courseID = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseID);

        window.location.replace("chapter_contents.html");  // redirect to chapter_contents.html 
    }, 1000);
}

function logout () {
    storage.clear(); //clear local storage session
    
    window.location.replace("./login.html");
}