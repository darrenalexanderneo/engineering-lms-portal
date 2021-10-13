
const storage = window.localStorage;
        
// get the course selected
const course_selected = storage.getItem('course_selected');
console.log('course selected: ' + course_selected);
// var course_json = [];
// var class_json = [];
// var learners_json = [];
// var course_ls = [];
// var class_ls = [];
// var learner_ls = [];
var alert_msg = '';

var class_filter = 'all';
var learner_type = 'preassign';
// var curr_num_of_learners = 0;

const learnerTypeDict = {
    "preassign": { 
        'num_of_learners': 0,
        'button_text': "Assign",
        'elem_class': "btn-success btn rounded-pill align-middle my-auto",
        'id': "preassign_learners",
        'func': 'assign'
    },
    "registered": { 
        'num_of_learners': 0,
        'button_text': "Approve",
        'elem_class': "btn-success btn rounded-pill align-middle my-auto",
        'id': "registered_learners",
        'func': 'assign'
    },
    "enrolled": { 
        'num_of_learners': 0,
        'button_text': "Withdraw",
        'elem_class': "btn-danger btn rounded-pill align-middle my-auto",
        'id': "enrolled_learners",
        'func': 'withdraw'
    }
}

// function to load json files
// var loadFile = function (filePath, done) {
//     var xhr = new XMLHttpRequest();
//     xhr.withCredentials = false;
//     xhr.onload = function () { return done(this.response) }
//     xhr.open("GET", filePath, true);
//     xhr.send();
// }





// var course_ls;
// var class_ls;
// var learner_ls;

// function waitForLocalStorage(key, cb, timer) {
//         if (!storage.getItem(key)) {
//             console.log(storage.getItem(key));
//             return (timer = setTimeout(waitForLocalStorage.bind(null, key, cb), 800));
//             }

//         clearTimeout(timer);

//         if (typeof(cb) !== 'function') {
//             return storage.getItem(key);
//             }   
//         console.log(storage.getItem(key));
//         return cb(storage.getItem(key));
//     } //set timeout to wait for Local Storage Session to be ready to "getItem()"

export const asyncLocalStorage = {
    setItem: async function (key, value) {
        await null;
        return storage.setItem(key, value);
    },
    getItem: async function (key) {
        await null;
        return storage.getItem(key);
    }
};

// function waitForLocalStorage(key) {
//     const storage = window.localStorage;
//     while (storage.getItem(key) == null) {

//     }
// }

export function getData() {
     // get course, class data
        
        //set timeout to wait for Local Storage Session to be ready to "getItem()"  
    const learner_ls = JSON.parse(asyncLocalStorage.getItem("learners_json"))[`${course_selected}`];
    console.log("learners_ls: ", learner_ls);

    const course_ls = JSON.parse(asyncLocalStorage.getItem("course_json"))["courses"];
     console.log("course_ls: ", course_ls);

    const class_ls = JSON.parse(asyncLocalStorage.getItem("class_json"))[`${course_selected}`];
     console.log("class_ls: ", class_ls);

     learnerTypeDict['preassign']['num_of_learners'] = learner_ls.preassign_learners.length;
     learnerTypeDict['registered']['num_of_learners'] = learner_ls.registered_learners.length;
     learnerTypeDict['enrolled']['num_of_learners'] = learner_ls.enrolled_learners.length;
     curr_num_of_learners = learner_ls.preassign_learners.length;
    
     if (course_ls && class_ls && learner_ls) {
         console.log("hello");
        getCourseDetails();
     }

}

export function getCourseDetails() {
    // console.log("course_ls: ", course_ls);
    // console.log("class_ls: ", class_ls);
    console.log("learner_ls: ", learner_ls);

    for (var j = 0; j < course_ls.length; j++) { 
        var c_id = course_ls[j].course_id;
        if (course_selected == c_id) { 
            // console.log("c_id", c_id)
            var c_name = course_ls[j].course_name;
            var c_desc = course_ls[j].course_description;
            break
        }
    }

    // console.log('check', c_name, c_id, c_desc);
    document.getElementById("course_title").innerHTML = `${c_id} - ${c_name}`;
    document.getElementById("course_description").innerHTML = `${c_desc}`;
}

export function getClassFilter() { 
    console.log(`=== getClassFilter called ===`);
    console.log(`number of classes: ${class_ls.length}`);

    var class_dropdown = `<option selected value="All">All</option>`;
    for(var i = 0; i < class_ls.length; i++) {
        var class_id = class_ls[i].class_id;
        var class_name = `${class_id.slice(0, 1)}lass ${class_id.slice(1, 2)}`;
        // console.log(`test: ${class_id}, ${class_name}`)
        class_dropdown += `<option value="${class_id}">${class_name}</option>`;
    }

    document.getElementsByClassName("form-select")[0].innerHTML = class_dropdown;
}

export function changeTabActive(curr_tab) { 
    var tab_list = ['preassign', 'registered', 'enrolled'];

    for(var i = 0; i < tab_list.length; i++) {
        // console.log(tab_list[i]);
        document.getElementById(`${tab_list[i]}`).setAttribute('class', 'page-item');

    }
    // console.log(`selected tab: ${curr_tab}`);
    document.getElementById(`${curr_tab}`).setAttribute('class', 'page-item active');

}

export function displayLearnersOfClass(class_id) {
    class_filter = class_id; // update filter
    var type_id = learnerTypeDict[`${learner_type}`]['id'];
    var curr_class_type_list = learner_ls[`${type_id}`]; // type_id == 'enrolled_learners'

    console.log(`=== displayLearnersOfClass called ===`);
    console.log(`class_id: ${class_id}, learners_type: ${learner_type}`)
    
    document.getElementById("learners_list").innerHTML = "";

    if (class_filter.toLowerCase() == 'all') { 
        console.log(`in all ->`);
        var record = getHTMLofAllRecords(curr_class_type_list);
    } else {
        console.log(`in others ->`);
        var record = getHTMLofRecord(curr_class_type_list);
    }
    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}


export function displayLearnersByType(curr_learner_type) { 
    learner_type = curr_learner_type; // update filter
    var type_id = learnerTypeDict[`${curr_learner_type}`]['id'];
    // console.log('type_id', type_id)
    var curr_list = learner_ls[`${type_id}`]; // type_id == 'enrolled_learners'

    console.log(`=== displayLearnersByType called ===`);
    console.log(`class_filter: ${class_filter}, learners_type: ${learner_type}`);

    console.log('number of learners for tab:', learnerTypeDict[`${curr_learner_type}`]['num_of_learners'])
    
    if (class_filter.toLowerCase() == 'all') { 
        console.log(`in all ->`);
        var record = getHTMLofAllRecords(curr_list);
    } else {
        var record = getHTMLofRecord(curr_list);
    }

    // update table with data
    document.getElementById("learners_list").innerHTML = record;

}

export function displayLearnerDetails(class_filter, learner_type) { 
    // number of learners
    console.log(`# of learners: preassign: ${learnerTypeDict['preassign']['num_of_learners']} | registered: ${learnerTypeDict['registered']['num_of_learners']} | enrolled: ${learnerTypeDict['enrolled']['num_of_learners']}`);
    var preassigned_ls = learner_ls['preassign_learners'];
    // console.log("preassigned_ls: ", preassigned_ls);

    var record = getHTMLofAllRecords(preassigned_ls);

    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}


export function getHTMLofRecord(curr_list) { 
    // console.log(`learner type:`, learnerTypeDict[`${learner_type}`]['num_of_learners']);
    var record = "";
    var num_of_learners = learnerTypeDict[`${learner_type}`]['num_of_learners'];
    var btn_class = learnerTypeDict[`${learner_type}`]['elem_class'];
    var func_type = learnerTypeDict[`${learner_type}`]['func'];
    var curr_learner_count = 0;

    if (num_of_learners == 0) {
        record = `There are currently no preassigned learners in for ${class_filter} classes`;
    } else { 
        
        for (var i = 0; i < curr_list.length; i++) {
            var class_id = curr_list[i].class_id;
    
            if (class_id.toLowerCase() == class_filter.toLowerCase()) {
                var emp_name = curr_list[i].name;
                var emp_id = curr_list[i].emp_id; 
                // console.log(`hehe: ${emp_name}, ${emp_id}, ${class_id}`)
                record += `<tr>

                    <td class="text-center align-middle">${emp_id}</td>
                    <td class="text-center align-middle">${emp_name}</td>
                    <td class="text-center align-middle">${class_id}</td>
                    <td class="text-center align-middle my-auto"><p class= "${btn_class}" onclick="updateLearners('${func_type}', '${emp_id}', '${class_id}')" id="${emp_id}">${learnerTypeDict[`${learner_type}`]['button_text']}</p></td>

                    </tr>`;

                curr_learner_count++;
            }
           
        }
    }

    if (curr_learner_count == 0) { 
        record = `There are currently no preassigned learners in for ${class_filter} classes`;
    }
    console.log('number of learners for class+tab: ', curr_learner_count);
    // console.log(record);

    return record;
}

export function getHTMLofAllRecords(curr_list) { 
    var record = "";
    var btn_text = learnerTypeDict[`${learner_type}`]['button_text'];
    var btn_class = learnerTypeDict[`${learner_type}`]['elem_class'];
    var func_type = learnerTypeDict[`${learner_type}`]['func'];
    
    if (learnerTypeDict[`${learner_type}`]['num_of_learners'] == 0) {
        record = `There are currently no preassigned learners in for ${class_filter} classes`;
    } else { 
        for (var i = 0; i < curr_list.length; i++) {
            var class_id = curr_list[i].class_id;
            // console.log(class_id);
            var emp_name = curr_list[i].name;
            var emp_id = curr_list[i].emp_id; 
            // console.log(`hehe: ${emp_name}, ${emp_id}, ${class_id}`)
            record += `<tr>

                <td class="text-center align-middle">${emp_id}</td>
                <td class="text-center align-middle">${emp_name}</td>
                <td class="text-center align-middle">${class_id}</td>
                <td class="text-center align-middle my-auto"><p class= "${btn_class}" onclick="updateLearners('${func_type}', '${emp_id}', '${class_id}'); " id="${emp_id}">${btn_text}</p></td>

                </tr>`;
        }
    }
    // console.log(record);

    return record;
}


export async function updateLearners(update_type, emp_id, class_id) {
    // add alert/service msg when withdraw/assign
    
    var course_id = course_selected;
    console.log(`update info: ${update_type}, ${emp_id}. ${class_id}, ${course_selected}`);

    var url = update_type == "assign" ? 'http://192.168.1.71:5000/assign_course' : 'http://192.168.1.71:5000/withdraw_course';
    var method = update_type == "assign" ? 'POST' : 'PUT';
    console.log(url, method);

    // AJAX call to invoke update of Learner's table in database to change available_slots: assign_course, withdraw_course
    var request = new XMLHttpRequest();

    request.withCredentials = false;
    // request.crossDomain = true;

    request.onreadystatechange = function () {
        try {
            console.log("readystate: ", this.readyState, this.status);
            if (this.readyState == 4 && (this.status == 200 || this.status == 201)) {
                var obj = JSON.parse(this.response);
                alert_msg = `${update_type} of learners is successful`;
                var message = `Successfully ${update_type} the enrollment of Learner #${emp_id} from ${class_id} of ${course_id}.`;
                console.log(`${update_type} of learners is successful`);
                document.getElementById("learners_list").innerHTML = message; // to do

                // alert storage
                window.localStorage.setItem("alert_msg", alert_msg);
                console.log('reload', localStorage['alert_msg']);
                alert(localStorage['alert_msg']);
                reload();
            } else if (this.readyState == 4 && this.status == 404) {
                alert_msg = `${update_type} of learners failed`, "error: ", this.statusText;
                console.log(`${update_type} of learners failed`, "error: ", this.statusText);

                // alert storage
                window.localStorage.setItem("alert_msg", alert_msg);
                console.log('reload', localStorage['alert_msg']);
                alert(localStorage['alert_msg']);
                
                reload(); // location.reload(true);
           
            }
        } catch(err) {
                // Errors when calling the service; such as network error, 
            // service offline, etc
            showError('There is a problem retrieving data, please try again later.<br />' + err);

        }
        // location.reload(true);
        
    }

    

    var data = JSON.stringify({ 'emp_id': emp_id, 
                                'course_id': course_id,
                                'class_id': class_id
    });

    console.log(data);
    request.open(method, url, true, "/json-handler");
    request.setRequestHeader("Content-Type", "application/json");
    request.send(data); // to do     
    
    // location.reload(true);
}




export function reload() {
    location.reload()
}
