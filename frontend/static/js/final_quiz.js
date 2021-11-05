const storage = window.localStorage;

const learner_id = storage.getItem("learner_id");
const quiz_id = storage.getItem("finalQuiz_id");
const class_id = storage.getItem("class_id");
const chapter_id = storage.getItem("chapter_id");

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');
var learners_Answers = {};
var question_list = [];
var course_id;

//initialise global variables to store api keys
var getQuizQuestions;
var submitQuiz_POST;
var getFinalQuizScore;


document.getElementById("learner-id").innerHTML = learner_id;


$('#submit').modal({ show: false});


// to retrieve api keys without exposing
function getAPIkeys () {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getQuizQuestions = api_keys.getQuizQuestions;
            submitQuiz_POST = api_keys.submitQuiz_POST;
            getFinalQuizScore = api_keys.getFinalQuizScore
        }
    }
    request.open("GET", "../../apikey.json", false);
    request.send();
}

function renderPage () {
    getAPIkeys();
    displayFinalQuizTitle();
    displayFinalQuiz(quiz_id);
}

function displayFinalQuizTitle () {
     course_id = class_id.split("_")[0];
    var class_name = "Class " + class_id.split("_")[1].replace("C","");

    document.getElementById("quiz-title").innerHTML = `${course_id} ${class_name} - Final Quiz`;
}

function displayFinalQuizTimer (duration) {
    var minutes = duration.split(":")[0];
    var seconds = duration.split(":")[1];

    // Set the date we're counting down to
    var countDownDate = new Date((new Date().getTime() + minutes * 60000 + seconds * 360000));

    // Update the count down every 1 second
    var countdown = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    // var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    // var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element with id="demo"
    document.getElementById("timer").innerHTML = `Time Left: &nbsp; ${minutes} m ${seconds} s`;

    // If the count down is finished, write some text
    if (distance < 0) {
        clearInterval(countdown);
        document.getElementById("timer").innerHTML = "EXPIRED";
        location.reload();
    }
    }, 1000);

}

function displayFinalQuiz (quiz_id) {

    // console.log(quiz_id);

    document.getElementById("quiz").innerHTML = "";

    var html_content = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var result = JSON.parse(this.response);
            console.log(result);

            if (result.code == 500) {
                console.log("Quiz Questions Have Not Been Set By Your Trainer Yet.");
                document.getElementById("quiz").innerHTML = `<h5 class="text-center text-muted">Quiz Questions Have Not Been Set By Your Trainer Yet.</h5>`;
                document.getElementById("submit-btn").hidden = true;

            } else if (result.code == 200) {
                var quiz_duration = result.duration;
                displayFinalQuizTimer(quiz_duration);

                question_list = result.question_records;
                // console.log(question_list);

                for (qn of question_list) {
                    // console.log(qn);
                    var question = qn.question;
                    var question_id = qn.question_id;
                    var question_mark = qn.question_mark;
                    var question_type = qn.question_type; 
                    var qn_options = qn.option; 

                    options_array = qn_options.split(","); //array of questions  
                    
                    html_content += `<form><div id="${question_id}" class="mb-5 px-auto">
                    <h5><b>${question_id}.  ${question}</b> (${question_type})</h5>
                    <h6 class='float-end'>${question_mark} Marks</h6><br>`;

                    for (var option of options_array) {  // find out how to get selected value of radio buttons
                        html_content +=  `<div class="form-check"> 
                        <input class="form-check-input ms-3" type="radio" onclick="radioChecked('${question_id}','${option}')" name="${question_id}" id="${question_id}-${option}" required>
                        <label class="form-check-label ms-3 fs-5" for="${question_id}-${option}">
                            ${option}
                        </label>
                        </div>`;
                    }

                    html_content += `<div class="invalid-feedback">Please attempt the question.</div></div></form>`;
                }
                
                document.getElementById("quiz").innerHTML = html_content;
            }
            
        }
    };

    var url = `${getQuizQuestions}${quiz_id}`;
    console.log(url);
    request.open("GET", url, true);
    request.send();
}
// document.querySelector(input[name="${question_id}-options"]:checked).value;

function radioChecked (question_id, selected_option) {
    console.log(selected_option);

    learners_Answers[`${question_id}`] = selected_option;

}

// submitButton.addEventListener('click', submitQuiz)

function submitQuiz () {
    console.log(learners_Answers);
    console.log(question_list);

    if (Object.keys(learners_Answers).length == question_list.length) {
        console.log("validation - all questions are answered!");

        var questions_array = [];
        var answers_array = [];
        var questions_str = "";
        var answers_str = "";

        for (var key in learners_Answers) {
            console.log(key);
            questions_array.push(key);
            answers_array.push(learners_Answers[`${key}`]);
        }

        questions_str = questions_array.join(",");
        answers_str = answers_array.join(",");

        var answers_obj = {};
        answers_obj["quiz_id"] = quiz_id;
        answers_obj["learner_id"] = learner_id;
        answers_obj["question"] = questions_str;
        answers_obj["answer"] = answers_str;
        answers_obj["type"] = "final_quiz";

        answers_json = JSON.stringify(answers_obj);

        console.log(answers_json);

        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                var result = JSON.parse(this.response);

                console.log(result);
                if (result.code == 200) {
                    displayFinalQuizScore();
                } else {
                    alert("Quiz Submission is Unsuccessful.");
                }
            }
        }
        request.open("POST", submitQuiz_POST, true);
        request.setRequestHeader("Content-Type", "application/json");
        request.send(answers_json);

    } else {
        console.log("validation - NOT all questions are answered!");
        alert("Please Attempt All The Questions!");
    }
}

function displayFinalQuizScore () {

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var results = JSON.parse(this.response).data;
            var quiz_score = (parseInt(results.marks) / parseInt(results.total_marks)) * 100;

            console.log(quiz_score);


            var message = "";
            var buttons = "";

            if (quiz_score < 50) {
                message = "You failed the quiz. You have to retake it until you pass in order to complete this course.";
                buttons = `<button type="button" class="btn btn-primary" data-bs-dismiss="modal" onclick="location.href='final_quiz.html'">Retake Quiz</button>`;

            } else {
                var current_date = new Date().toDateString();
                console.log(current_date);
                message  = `You passed the quiz! Congratulations, you have been awarded a completion certificate for ${course_id}!
                <div style="width:100%; height:100%; padding:20px; text-align:center; border: 10px solid #787878">
                <div style="width:98%; height:98%; padding:20px; text-align:center; border: 5px solid #787878" class="mx-auto">
                    <span style="font-size:16px; font-weight:bold">Certificate of Completion</span>
                    <br><br>
                    <span style="font-size:8px"><i>This is to certify that</i></span>
                    <br><br>
                    <span style="font-size:12px"><b>${learner_id}</b></span><br/><br/>
                    <span style="font-size:8px"><i>has completed the course</i></span> <br/><br/>
                    <span style="font-size:12px">${course_id}</span> <br/><br/>
                    <span style="font-size:10px">with score of <b>${quiz_score}%</b></span> <br/><br/><br/><br/>
                    <span style="font-size:12px"><i>dated</i></span><br>
                    <span style="font-size:12px">${current_date}</span>
                </div>
                </div>`;
                buttons = `<button type="button" class="btn btn-primary" onclick="redirect_to_BrowseCourses()">Browse More Courses</button>`;
            }


            document.getElementsByClassName("modal-body")[0].innerHTML = message;
            document.getElementsByClassName("modal-footer")[0].innerHTML = buttons;

            $('#submit').modal('show');
        }
    }
    request.open("GET", `${getFinalQuizScore}${quiz_id}/${learner_id}`, true);
    request.send();
}

function redirect_to_BrowseCourses() {
    // storage.setItem("course_id",course_id);

    // setTimeout(function () { 
    //     const courseid = storage.getItem("course_id"); 
    //     console.log("localStorage.getItem():" + courseid);
    window.location.replace("view_reg_courses.html");  // redirect to enrolled_courses.html 
    // }, 1000);
}

function goBackTo (prev_page) {

    var current_location_arr = window.location.href.split("/");
    var current_location = current_location_arr[current_location_arr.length - 1];
    console.log(current_location);

    if (prev_page == "viewcourses" && current_location == "final_quiz.html") {
        console.log(prev_page);
        window.location.replace("enrolled_courses.html");
    } 
}

function logout () {
    storage.clear();

    window.location.replace("./login.html");
}