// var course_id;

// api keys
var getCourseList_HR;
var getCourseDetails_HR;
var getLearnerList_HR;
var assignLearner_POST_HR;
var withdrawLearner_POST_HR;

const storage = window.localStorage;

function getAPIkeys () {

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {

            var apikeys = JSON.parse(this.response);

            getCourseList_HR = apikeys.getCourseList_HR;
            getCourseDetails_HR = apikeys.getCourseDetails_HR;
            getLearnerList_HR = apikeys.getLearnerList_HR;
            assignLearner_POST_HR = apikeys.assignLearner_POST_HR;
            withdrawLearner_POST_HR = apikeys.withdrawLearner_POST_HR;

        }


    }
    url = "../../apikey_development.json"; 
    request.open("GET", url, false);
    request.send();
}

function getAllCourses() { 

    getAPIkeys();

    document.getElementById("course_list").innerHTML = "";
    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            // get course data
            const course_ls = JSON.parse(this.response).data.courses;
            console.log("course_ls: ", course_ls);

            var record = '';
            for (var i = 0; i < course_ls.length; i++) {

                // declare variables

                var course_name = course_ls[i].course_name;
                var course_id = course_ls[i].course_id;
                var num_of_classes = course_ls[i].num_of_class;
                var total_slot_avail = course_ls[i].total_slot_available;
        
                console.log(course_name);
                console.log(course_id);
        
        
                // input row details
                record += `<tr onclick="redirect_to_LearnersListPage('${course_id}')" id="${course_id}"><a href="#">
        
                    <td class="text-center align-middle">${course_id}</td>
                    <td class="text-center align-middle">${course_name}</td>
                    <td class="text-center align-middle">${num_of_classes}</td>
                    <td class="text-center align-middle">${total_slot_avail}</td>
        
                    <td><i class="fa bi bi-chevron-double-right" ></i></td>
                    
                </a></tr>`;
            }
            
            // update table with data
            document.getElementById("course_list").innerHTML = record;

        }
    };

    url = getCourseList_HR;  // api endpoint example:  flask --> localhost:5000/learners/course/ENG101 OR AWS RDS --> some URL
    request.open("GET", url, true);
    request.send();
}

function redirect_to_LearnersListPage(course_id) {
    storage.setItem('course_id', course_id);
    
    setTimeout( function() { 
        const course_selected = storage.getItem('course_id');
        console.log(course_selected);
        if (course_selected == course_id) {
            location.href = "viewLearnersList.html";
        }
    }, 2000);
    
}
