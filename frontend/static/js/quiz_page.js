const storage = window.localStorage;

const learner_id = storage.getItem("learner_id");
const quiz_id = storage.getItem("quiz_id");

const quizContainer = document.getElementById('quiz');
const resultsContainer = document.getElementById('results');
const submitButton = document.getElementById('submit');
var learners_Answers = {};
var question_list = [];

//initialise global variables to store api keys
var getQuizQuestions;
var submitQuiz_POST;

// to retrieve api keys without exposing
function getAPIkeys () {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getQuizQuestions = api_keys.getQuizQuestions;
            submitQuiz_POST = api_keys.submitQuiz_POST;

            console.log(getQuizQuestions);
            console.log(submitQuiz_POST);
        }
    }
    request.open("GET", "../../apikey.json", false);
    request.send();
}

function renderPage () {
    getAPIkeys();
    displayQuizTitle(quiz_id);
    displayQuiz(quiz_id);
}

function displayQuizTitle (quiz_id) {
    var array = quiz_id.split("_");
    var course_id = array[0];
    var class_name = "Class " + array[1].replace("C","");
    var chapter_name = "Chapter " + array[2].replace("q","").replace("Chapt","");
    var html = `<h2>Quiz - ${course_id} - ${class_name} - ${chapter_name}</h2>`;
    document.getElementById("quiz-title").innerHTML = html;
}


function displayQuiz (quiz_id) {

    document.getElementById("quiz").innerHTML = "";

    var html_content = "";

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            question_list = JSON.parse(this.response).question_records;
            // console.log(question_list);

            for (qn of question_list) {
                // console.log(qn);
                var question = qn.question;
                var question_id = qn.question_id;
                var question_mark = qn.question_mark;
                var question_type = qn.question_type; 
                var qn_options = qn.option; 

                options_array = qn_options.split(","); //array of questions  
                
                html_content += `<div id="${question_id}" class="mb-5 px-auto">
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

                html_content += `<div class="invalid-feedback">Please attempt the question</div></div>`;
            }
            
            document.getElementById("quiz").innerHTML = html_content;
        }
    };

    var url = `${getQuizQuestions}${quiz_id}`;
    request.open("GET", url, true);
    request.send();
}
// document.querySelector(input[name="${question_id}-options"]:checked).value;

function radioChecked (question_id, selected_option) {
    console.log(selected_option);

    learners_Answers[`${question_id}`] = selected_option;

}

submitButton.addEventListener('click', submitQuiz)

function submitQuiz () {

    if (Object.keys(learners_Answers).length == question_list.length) {
        console.log("validation - all questions are answered!");

        var answers_obj = learners_Answers;
        answers_obj["quiz_id"] = quiz_id;
        answers_obj["Learner_id"] = learner_id;

        console.log(answers_obj);

        // var request = new XMLHttpRequest();
        // request.onreadystatechange = function () {
        //     if (this.readyState == 4 && this.status == 200) {
        //         var result = JSON.parse(this.response);

        //         console.log(result);
        //         displayQuizScore();

        //     }
        // }
        // request.open("POST", submitQuiz_POST, true);
        // request.setRequestHeader("Content-Type", "application/json");
        // request.send(learners_Answers);

    } else {
        console.log("validation - NOT all questions are answered!");
        alert("Please Attempt All The Questions!");
    }


}

function displayQuizScore () {
    var html_content = `<!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
      Launch static backdrop modal
    </button>
    
    <!-- Modal -->
    <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">Modal title</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            ...
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Understood</button>
          </div>
        </div>
      </div>
    </div>`

    document.getElementById("results")

}

function redirect_to_classRegistration(course_id) {
    storage.setItem("course_id",course_id);

    setTimeout(function () { 
        const courseid = storage.getItem("course_id"); 
        console.log("localStorage.getItem():" + courseid);
        window.location.replace("class_registration.html");  // redirect to class_registration.html 
    }, 1000);
}

function goBackTo (prev_page) {

    var current_location_arr = window.location.href.split("/");
    var current_location = current_location_arr[current_location_arr.length - 1];
    console.log(current_location);

    if (prev_page == "chapter_contents" && current_location == "quiz_page.html") {
        console.log(prev_page);
        window.location.replace("chapter_contents.html");
    } 
}

function logout () {
    storage.removeItem("learner_id");

    window.location.replace("./login.html");
}