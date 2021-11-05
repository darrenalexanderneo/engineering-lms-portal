//initialise localStorage
const storage = window.localStorage;

const learner_id = storage.getItem("learner_id");
const course_id = storage.getItem("course_id");
const chapter_id = storage.getItem("chapter_id");
const viewOnly = storage.getItem("view-only");

document.getElementById("learner-id").innerHTML = learner_id;


// $(window).on('scroll', function() {
//     if($(window).scrollTop() >= $('body').offset().top + $('body').outerHeight() - window.innerHeight) {
//     //   alert('Bottom');
//       loadQuizButton(chapter_id);
//     }
// });

function renderPage() {
    chapterTitle();
    getPDFlink(course_id, chapter_id);
    loadQuizButton(chapter_id);
}

function chapterTitle () {
    const chapter_name = "Chapter " + (chapter_id.split("_")[2]).replace("Chapt","");
    document.getElementById("chapter-title").innerHTML = `${chapter_name} - Readings`;
}

function renderPDFinAdobe (pdfUrl, adobeAPI) {
    console.log(pdfUrl);

    var adobeDCView = new AdobeDC.View({clientId:  `${adobeAPI}`, divId: "pdfviewer"});
    adobeDCView.previewFile(
        {
            content:{location: {url: `${pdfUrl}/preview`,headers:[{key: "Access-Control-Allow-Origin", value: "*"}]},promise: ""},
            metaData:{fileName: `${chapter_id}.pdf`},
        }, 
        {
            defaultViewMode: "FIT_WIDTH", showLeftHandPanel: false, dockPageControls: false, 
            showDownloadPDF: false, showPrintPDF: false
        },
    );
}

// retrieve PDF link using pdf_database.json based on given course_id and chapter_id
function getPDFlink (course_id, chapter_id) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var pdf_database = JSON.parse(this.response);
            var pdfUrl = pdf_database[`${course_id}`][`${chapter_id}`];

            // ---- if using adobe pdf viewer ----
            // var adobeAPI = pdf_database.adobe_api;
            // document.addEventListener("adobe_dc_view_sdk.ready", renderPDFinAdobe(pdfUrl, adobeAPI));

            renderPDF(pdfUrl);
        }
    }
    request.open("GET", "../../pdf_database.json", false);
    request.send();
}

// render PDF link from google drive
function renderPDF (pdfUrl) {

    console.log(pdfUrl);
    // var pdfUrl = "https://drive.google.com/file/d/1JgUvVSkrhFSrj9lWxX1CIO0gkLUD2KE0";
    // var html = `<iframe src="${pdfUrl}/preview" scrolling="no" style="overflow: hidden;" width="1000" height="16000" frameborder="0" allow="autoplay"></iframe>`;
    var html = `<iframe id="pdf_doc" src="${pdfUrl}/preview#view=fitV&view=fitH" title="Chapter Content" scrolling="no" style="overflow: hidden;" height="100%" width="100%"  frameborder="0" allow="autoplay" />`;
    document.getElementById("pdfviewer").innerHTML = html;
}

var obj = document.getElementById("pdfviewer");
var obj = document.getElementById("pdf_doc");


// function chk_scroll(e) {
//     console.log(e);
//     var elem = $(e.currentTarget);
//     console.log(elem);
//     if (elem[0].scrollHeight - elem.scrollTop() == elem.outerHeight()) 
//     {
//         console.log("bottom");
//         loadQuizButton;

//     }
// }

// if ( obj.scrollTop === (obj.scrollHeight - obj.offsetHeight)) {
//     console.log("Quiz button is out!");
//     loadQuizButton;
// }

function loadQuizButton (chapter_id) {
    console.log(viewOnly);
    if (viewOnly == "true") {
        console.log(`view-only = true`);
        document.getElementById("take-quiz-button");
    } else {
        document.getElementById("take-quiz-button").innerHTML = `<br><br><button class="btn btn-outline-primary btn-lg text-center mx-auto" onclick="redirect_to_QuizPage('${chapter_id}')">Take Quiz</button><br><br><br>`;
    }
}

// stores quiz_id to localStorage for retrieval before redirecting to quiz_page.html
function redirect_to_QuizPage (chapter_id) {
    var quiz_id = `${chapter_id}q`;
    storage.setItem("quiz_id", quiz_id);

    setTimeout(function () { 
        const quizID = storage.getItem("quiz_id"); 
        console.log("localStorage.getItem('quiz_id'):" + quizID);
        window.location.replace("quiz_page.html");  
    }, 1000);
}

function goBackTo (prev_page) {
    console.log(prev_page);

    var current_location_arr = window.location.href.split("/");
    var current_location = current_location_arr[current_location_arr.length - 1];
    console.log(current_location);

    if (prev_page == "viewEnrolledCourses" && current_location == "chapter_contents.html") {
        console.log(prev_page);
        window.location.replace("enrolled_courses.html");
    } 
}

function logout () {
    storage.clear();

    window.location.replace("./login.html");
}