const development = 'apikey_development.json';
const production = 'apikey.json';

/*** CHANGE ACCORDINGLY ***/
const apikey_url = production;

/*** RETRIEVE API KEYS ***/
function getAPIkeys_TNR() {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getCourseList_TNR = api_keys.getCourseList_TNR;
            getCourseDetails_TNR = api_keys.getCourseDetails_TNR;
            viewQuiz_TNR = api_keys.viewQuiz_TNR;
            createQuiz_POST_TNR = api_keys.createQuiz_POST_TNR;

            // console.log(getCourseList_TNR);
            // console.log(getCourseDetails_TNR);
            // console.log(viewQuiz_TNR);
            // console.log(createQuiz_POST_TNR);
        }
    }
    request.open("GET", `../../${apikey_url}`, false);
    request.send();
}

function getAPIkeys_HR() {  
    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var api_keys = JSON.parse(this.response);
            getCourseList_HR = api_keys.getCourseList_HR;
            getCourseDetails_HR = api_keys.getCourseDetails_HR;
            getLearnerList_HR = api_keys.getLearnerList_HR;
            assignLearner_POST_HR = api_keys.assignLearner_POST_HR;
            withdrawLearner_POST_HR = api_keys.withdrawLearner_POST_HR;

            // console.log(getCourseList_TNR);
            // console.log(getCourseDetails_TNR);
            // console.log(viewQuiz_TNR);
            // console.log(createQuiz_POST_TNR);
        }
    }
    request.open("GET", `../../${apikey_url}`, false);
    request.send();
}

/*** REDIRECT TO PAGE ***/
function redirectToPage(given_page) {
    setTimeout(function () { 
        window.location.replace(`${given_page}.html`);
    }, 700);
}

function backToPrevPage(given_page) {
    window.location.replace(`${given_page}.html`);
    // storage.clear();
}