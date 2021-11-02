//initialise localStorage
const storage = window.localStorage;

// const learner_id = storage.getItem("learner_id");
const learner_id = 'LNR12';
//initialise global variables to store api keys
var getCourseProgress;
var getAllChapters;
var getCourseCompletionStatus;
var getCompletedChapters;
var getEnrollmentStatus;

document.getElementById("learner-id").innerHTML = learner_id;

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
    request.open("GET", "../../apikey_development.json", false);
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

            } else {       // course_list.length > 0 but need to check if there are any ENROLLED courses (not pending)
                var enrolled = false;
                for (var course of course_list) {
                    if (course.is_approved == 1) {
                        enrolled = true;
                    }
                }
                if (enrolled == false) {
                    document.getElementById("message-container").innerHTML = "<h5>You Do Not Have Any Enrolled Courses Currently.</h5>";
                }
                else { // enrolled == true
                    for (var eachCourse of course_list) {
                        if (eachCourse.is_approved == 1) {
                            console.log(eachCourse);
                            var course_id = eachCourse.course_id;
                            var course_name = eachCourse.course_name;
                            var class_id = eachCourse.class_id;
                            
                            html_content += 
                            `<option value="${class_id}">${course_id} - ${course_name}</option>`;
                        }
                    }
                
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
    showCourseProgressBar(class_id);

    document.getElementById("chapter-list").innerHTML = `<div class="text-center mt-5">
                                        <img src="../../static/img/loading_spinner.gif"  height="50px" width="50px" alt="loading gif">
                                    </div>`;
    document.getElementById("message-container").innerHTML = "";

    var html_content = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var results = JSON.parse(this.response);
            // if (results.code == 500) {
            //     console.log(chapter_list);
            //     document.getElementById("chapter-list").innerHTML = "<h5>No Chapter Materials Found</h5>";

            // } else {
                var chapter_list = results.results;
                console.log(chapter_list);

                var checkforFirst = 0;
                var num_completedChapters = 0;
    
                for (chapter of chapter_list) {
                    // console.log(chapter);
                    var chapter_id = chapter.chapter_id;
                    var chapter_name = "Chapter " + chapter_id.split("_")[2].replace("Chapt","");
                    
                    //invoke function to check if chapter is completed or not
                    var status_html = ``;
                    num_completedChapters += checkforCompletedChapters(class_id, chapter_id);
                    console.log(num_completedChapters);

                    if (num_completedChapters > 0) {
                        // chapter is completed
                        console.log(`${chapter_id} IS COMPLETED!`);
                        status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-primary rounded-pill">View</button>
                                        <span style="margin-bottom: 0px;" class="badge bg-success rounded-pill px-2 py-2">Completed</span>`;
    
                    } else { //chapter is not completed yet
                        if (checkforFirst == 0) { //only enable "Learn" button for first uncompleted chapter
                            status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-primary rounded-pill">Learn</button>`;
                            checkforFirst = 1;
                        } else { //disable the other "Learn" buttons
                            status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-primary rounded-pill disabled">Learn</button>`;
                        }   
                    }
        
                    html_content += 
                    `<li class="list-group-item d-flex py-3 align-items-center">
                        <div class="ms-2 me-auto"><h5>${chapter_name}</h5></div>
                        ${status_html}
                    </li>`;
                }
                if (num_completedChapters == chapter_list.length) {
                    disabled = "";  // final quiz button ENABLED
                } else {
                    disabled = "disabled";  // final quiz button DISABLED
                }
                var final_quiz_id = `${course_id}_FinalQuizq`;
                html_content += `<li class="list-group-item d-flex py-3 align-items-center">
                                <div class="ms-2 me-auto"><h5>Final Quiz</h5></div>
                                <button onclick="redirect_to_FinalQuiz('${final_quiz_id}','${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-primary rounded-pill ${disabled}">Take Quiz</button>
                                </li>`;

                document.getElementById("chapter-list").innerHTML = html_content;
            // }
        }
    };

    var url = `${getAllChapters}${class_id}`;
    request.open("GET", url, true);
    request.send();
    
}

function checkforCompletedChapters (class_id, chapter_id) {

    var chapter_completed = 0;

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var chapter_list = JSON.parse(this.response).results;
            console.log(chapter_list);


            for (var chapter of chapter_list) {
                // console.log(chapter);
                var completion_status = chapter.completion;
                var chapterID = chapter.chapter_id;
                // console.log(completion_status);
                // console.log(chapterID);

                if (completion_status == 1 && chapterID == chapter_id) {
                    // console.log("chapter is completed!");
                    chapter_completed += 1;
                }
            }
        }
    };

    var url = `${getCompletedChapters}${class_id}/${learner_id}`;
    request.open("GET", url, false);
    request.send();

    // console.log(chapter_completed);
    return chapter_completed; // count of completed chapters
}

function showCourseProgressBar(class_id) {

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var course_progress = JSON.parse(this.response).progress_percentage;
            course_progress = Math.round(course_progress);
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

    var url = `${getCourseProgress}${class_id}/${learner_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();


}

function redirect_to_chapterContents(course_id,chapter_id, class_id) {
    storage.setItem("chapter_id",chapter_id);
    storage.setItem("course_id",course_id);
    storage.setItem("class_id",class_id);


    setTimeout(function () { 
        var chapterID = storage.getItem("chapter_id"); 
        console.log("localStorage.getItem():" + chapterID);

        var courseID = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseID);

        var classID = storage.getItem("class_id"); 
        console.log("localStorage.getItem():" + classID);

        window.location.replace("chapter_contents.html");  // redirect to chapter_contents.html 
    }, 1000);
}
function redirect_to_FinalQuiz(final_quiz_id,course_id,chapter_id, class_id) {
    storage.setItem("chapter_id",chapter_id);
    storage.setItem("course_id",course_id);
    storage.setItem("class_id",class_id);
    storage.setItem("finalQuiz_id", final_quiz_id);

    setTimeout(function () { 
        var finalQuizID = storage.getItem("finalQuiz_id"); 
        console.log("localStorage.getItem():" + finalQuizID);

        var chapterID = storage.getItem("chapter_id"); 
        console.log("localStorage.getItem():" + chapterID);

        var courseID = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseID);

        var classID = storage.getItem("class_id"); 
        console.log("localStorage.getItem():" + classID);

        window.location.replace("final_quiz.html");  // redirect to final_quiz.html 
    }, 1000);
}

function logout () {
    storage.clear(); //clear local storage session
    
    window.location.replace("./login.html");
}