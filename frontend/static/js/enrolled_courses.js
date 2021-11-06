//initialise localStorage
const storage = window.localStorage;

const learner_id = storage.getItem("learner_id");
const continued_course_id = storage.getItem("course_id");
// const learner_id = 'LNR12';
//initialise global variables to store api keys
var getCourseProgress;
var getAllChapters;
var getCourseCompletionStatus;
var getCompletedChapters;
var getEnrollmentStatus;
var getFinalQuizScore;
var getCourseCompletion;
var getCourseCommencementPeriod;

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
            getFinalQuizScore = api_keys.getFinalQuizScore;
            getCourseCompletion = api_keys.getCourseCompletion;
            getCourseCommencementPeriod = api_keys.getCourseCommencementPeriod;
            // console.log(getCourseProgress);
            // console.log(getAllChapters);
            // console.log(getCourseCompletionStatus);
            // console.log(getCompletedChapters);
            // console.log(getEnrollmentStatus);

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
                            
                            if (continued_course_id != undefined && course_id == continued_course_id) {
                                html_content += `<option value="${class_id}" selected>${course_id} - ${course_name}</option>`;
                                displayAllChapters(class_id);
                            } else {
                                html_content += `<option value="${class_id}">${course_id} - ${course_name}</option>`;
                            }
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

var completed;

function checkCourseCompletion (class_id) {
    var final_quiz_id = `${class_id}_FinalQuizq`;
    var course_id = class_id.split("_")[0];
    console.log(final_quiz_id);

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            completed = JSON.parse(this.response).is_completed;
        }
    }
    request.open("GET", `${getCourseCompletion}${course_id}/${learner_id}`, false);
    console.log(`${getCourseCompletion}${course_id}/${learner_id}`);
    request.send();

    return completed;  // pass = 1, fail or no attempt = 0
}

var quiz_score;
function getFinalQuizResults (final_quiz_id) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var results = JSON.parse(this.response).data;
            console.log(results);
            quiz_score = (parseInt(results.marks) / parseInt(results.total_marks)) * 100;

            console.log(quiz_score);
        }
    }
    request.open("GET", `${getFinalQuizScore}${final_quiz_id}/${learner_id}`, true);
    request.send();

    return quiz_score;
}

var commenced;
function getCourseCommencementDates (class_id) {
    // console.log(class_id);
    // const is_commenced;
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            commenced = JSON.parse(this.response).is_commence;  // 0 or 1
            console.log(commenced);
        }
    }
    // console.log(`${getCourseCommencementPeriod}${class_id}`);
    request.open("GET", `${getCourseCommencementPeriod}${class_id}`, false);
    request.send();

    // console.log(commenced);
    return commenced;
}

function displayAllChapters (class_id) {


    document.getElementById("message-container").innerHTML = "";
    
    var is_commenced = getCourseCommencementDates(class_id);
    console.log(is_commenced);
    // console.log(commenced);

    var course_id = class_id.split("_")[0];
    console.log(course_id);
    var completed = checkCourseCompletion(class_id);
    console.log(completed);

    var final_quiz_id = `${class_id}_FinalQuizq`;

    if (is_commenced == 0) {

        document.getElementById("course-progress-label").innerHTML = "";
        document.getElementById("course-progress-bar").innerHTML = "";

        console.log("HAS NOT COMMENCED");
        document.getElementById("chapter-list").innerHTML = `<br><br><h4 class='text-center fw-bold'>This Course Has Not Commenced Yet.</h4>`;

    } else {
        console.log("COURSE HAS COMMENCED");
        if (completed == 1) { //course completed!

            console.log("COURSE IS COMPLETED");

            var current_date = new Date().toDateString();
    
            var quiz_score = getFinalQuizResults(final_quiz_id);
    
            document.getElementById("chapter-list").innerHTML = `<br><br><h4 class='text-center fw-bold'>You have already completed this course!</h4>
            <br><br>
            <div style="width:100%; height:100%; padding:20px; text-align:center; border: 10px solid #787878">
            <div style="width:98%; height:98%; padding:20px; text-align:center; border: 5px solid #787878" class="mx-auto">
                <span style="font-size:50px; font-weight:bold">Certificate of Completion</span>
                <br><br>
                <span style="font-size:25px"><i>This is to certify that</i></span>
                <br><br>
                <span style="font-size:30px"><b>${learner_id}</b></span><br/><br/>
                <span style="font-size:25px"><i>has completed the course</i></span> <br/><br/>
                <span style="font-size:30px">${course_id}</span> <br/><br/>
                <span style="font-size:20px">with score of <b>${quiz_score}%</b></span> <br/><br/><br/><br/>
                <span style="font-size:30px"><i>dated</i></span><br>
                <span style="font-size:30px">${current_date}</span>
            </div>
            </div>
            `;
        } else {
            console.log("COURSE IS NOT COMPLETED");

            showCourseProgressBar(class_id);
        
            document.getElementById("chapter-list").innerHTML = `<div class="text-center mt-5">
                                                <img src="../../static/img/loading_spinner.gif"  height="50px" width="50px" alt="loading gif">
                                            </div>`;
        
            var html_content = "";
        
            var request = new XMLHttpRequest();
            request.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {
                    var results = JSON.parse(this.response);
        
                    var chapter_list = results.results;
                    console.log(chapter_list);
        
                    var checkforFirst = 0;
                    var num_completedChapters = 0;
                    var num_passedChapters = 0;
        
                    for (chapter of chapter_list) {
                        // console.log(chapter);
                        var chapter_id = chapter.chapter_id;
                        var chapter_name = "Chapter " + chapter_id.split("_")[2].replace("Chapt","");
                        var quiz_id = `${chapter_id}q`;
        
                        
                        //invoke function to check if chapter is completed or not
                        var status_html = ``;
                        // console.log(checkforCompletedChapters(class_id, chapter_id));                    
                        var completedChapter = checkforCompletedChapters(class_id, chapter_id)[0];
                        var passedChapter = checkforCompletedChapters(class_id, chapter_id)[1];
        
                        num_completedChapters += completedChapter;
                        num_passedChapters += passedChapter;
                        console.log(`completed chapter:${completedChapter} for ${chapter_id}`);
                        console.log(`passed chapter:${passedChapter} for ${chapter_id}`);
        
                        // console.log(num_completedChapters);
        
                        if (passedChapter == 1) {
                            // chapter is passed
                            console.log(`${chapter_id} IS PASSED!`);
                            status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}', true)" class="btn btn-outline-primary rounded-pill me-2">View</button>
                                            <button onclick="redirect_to_QuizPage('${quiz_id}', '${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-secondary rounded-pill me-2 disabled">Practise</button>
                                            <span style="margin-bottom: 0px;" class="badge bg-success rounded-pill px-2 py-2">Completed</span>`;
                        
                        } else if (completedChapter == 1) {
                            // chapter is completed by attempt of quiz
                            console.log(`${chapter_id} IS COMPLETED!`);
                            status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}',true)" class="btn btn-outline-primary rounded-pill me-2">View</button>
                                            <button onclick="redirect_to_QuizPage('${quiz_id}', '${course_id}','${chapter_id}','${class_id}')" class="btn btn-outline-primary rounded-pill me-2">Practise</button>
                                            <span style="margin-bottom: 0px;" class="badge bg-success rounded-pill px-2 py-2">Completed</span>`;
        
                        } else { //chapter is not completed yet (not attempted)
                            if (checkforFirst == 0) { //only enable "Learn" button for first uncompleted chapter
                                status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}',false)" class="btn btn-outline-primary rounded-pill">Learn</button>`;
                                checkforFirst = 1;
                            } else { //disable the other "Learn" buttons
                                status_html = `<button onclick="redirect_to_chapterContents('${course_id}','${chapter_id}','${class_id}',false)" class="btn btn-outline-secondary rounded-pill disabled">Learn</button>`;
                            }   
                        }
            
                        html_content += 
                        `<li class="list-group-item d-flex py-3 align-items-center">
                            <div class="ms-2 me-auto"><h5>${chapter_name}</h5></div>
                            ${status_html}
                        </li>`;
                    }
                    var disabled;
                    var button_style;
                    if (num_completedChapters + num_passedChapters == chapter_list.length) {
                        disabled = "";  // final quiz button ENABLED
                        button_style = "btn-outline-primary";
                    } else {
                        disabled = "disabled";  // final quiz button DISABLED
                        button_style = "btn-outline-secondary";
                    }
                    html_content += `<li class="list-group-item d-flex py-3 align-items-center">
                                    <div class="ms-2 me-auto"><h5>Final Quiz</h5></div>
                                    <button onclick="redirect_to_FinalQuiz('${final_quiz_id}','${course_id}','${chapter_id}','${class_id}')" class="btn ${button_style} rounded-pill ${disabled}">Take Quiz</button>
                                    </li>`;
        
                    document.getElementById("chapter-list").innerHTML = html_content;
                    
                }
            };
        
            var url = `${getAllChapters}${class_id}`;
            request.open("GET", url, true);
            request.send();
        }    
    }  
}

function checkforCompletedChapters (class_id, chapter_id) {

    var chapter_completed = 0;
    var chapter_passed = 0;
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var chapter_list = JSON.parse(this.response).results;
            // console.log(chapter_list);


            for (var chapter of chapter_list) {
                // console.log(chapter);
                var completion_status = chapter.completion;
                var chapterID = chapter.chapter_id;
                // console.log(completion_status);
                // console.log(chapterID);

                if (completion_status == 1 && chapterID == chapter_id) {
                    // console.log("chapter is completed & passed! - NO MORE TAKING QUIZ - DISABLE QUIZ BUTTON");
                    chapter_passed = 1;
                } else if (completion_status == 0 && chapterID == chapter_id) {
                    //chapter completed but quiz not passed yet - quiz button still avail
                    chapter_completed = 1
                }
            }
        }
    };

    var url = `${getCompletedChapters}${class_id}/${learner_id}`;
    request.open("GET", url, false);
    request.send();
    console.log([chapter_completed, chapter_passed]);
    return [chapter_completed, chapter_passed]; 
}

function showCourseProgressBar(class_id) {

    document.getElementById("course-progress-label").innerHTML = "";
    document.getElementById("course-progress-bar").innerHTML = "";

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

            // document.getElementById("course-progress-label").className -= `invisible`;
            // document.getElementById("course-progress-bar").className -= `invisible`;
        }
    };

    var url = `${getCourseProgress}${class_id}/${learner_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();
}

function redirect_to_chapterContents(course_id,chapter_id, class_id, view_only) {

    storage.setItem("chapter_id",chapter_id);
    storage.setItem("course_id",course_id);
    storage.setItem("class_id",class_id);
    storage.setItem("view_only", view_only)


    setTimeout(function () { 
        var chapterID = storage.getItem("chapter_id"); 
        console.log("localStorage.getItem():" + chapterID);

        var courseID = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseID);

        var classID = storage.getItem("class_id"); 
        console.log("localStorage.getItem():" + classID);

        var viewOnly = storage.getItem("view-only"); 
        console.log("localStorage.getItem():" + viewOnly);

        window.location.replace("chapter_contents.html");  // redirect to chapter_contents.html 
    }, 1000);
}

function redirect_to_QuizPage (quiz_id, course_id,chapter_id, class_id) {
    alert(class_id);
    storage.setItem("quiz_id", quiz_id);
    storage.setItem("chapter_id",chapter_id);
    storage.setItem("course_id",course_id);
    storage.setItem("class_id",class_id);

    setTimeout(function () { 
        var quizID = storage.getItem("quiz_id"); 
        console.log("localStorage.getItem():" + quizID);

        var chapterID = storage.getItem("chapter_id"); 
        console.log("localStorage.getItem():" + chapterID);

        var courseID = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseID);

        var classID = storage.getItem("class_id"); 
        console.log("localStorage.getItem():" + classID);
        alert(classID);

        window.location.replace("quiz_page.html");  // redirect to quiz_page.html 
    }, 8000);
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
    
    window.location.replace("../login.html");
}