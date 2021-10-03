var class_dropdown = document.getElementById('class_dropdown');
var class_selected = class_dropdown.value;
        
/* section 1: load files*/
// get the course selected
const course_selected = localStorage['course_selected'];
//localStorage.removeItem( 'course_selected' ); // Clear the localStorage
console.log('course selected: ' + course_selected);

// we need a function to load files
var loadFile = function (filePath, done) {
    var xhr = new XMLHttpRequest();
    xhr.onload = function () { return done(this.response) }
    xhr.open("GET", filePath, true);
    xhr.send();
}
// paths to all of your files
var myFiles = [ "../course_list.json", "../learners-v2.json"];
var jsonData = [];
myFiles.forEach(function (file, i) {
    // and call loadFile
    loadFile(file, function (response) {
        jsonData[i] = JSON.parse(response);
    }
)});

/* section 2: get course details */
function getCourseDetails() {
    // global variables
    const course_ls = jsonData[0].courses;
    const class_ls = jsonData[0].course_classes;
    const learner_ls = jsonData[1][course_selected];
    
    // registered
    var reg_ls = learner_ls.registered_learners;

    // get description 
    for (var j = 0; j < course_ls.length; j++) { 
        var c_id = course_ls[j].course_id;
        if (course_selected == c_id) { 
            var c_name = course_ls[j].course_name;
            var c_desc = course_ls[j].course_description;
            break
        }
    }

    console.log('check', c_name, c_id, c_desc);
    document.getElementById("course_title").innerHTML = `${c_id} - ${c_name}`;
    document.getElementById("course_description").innerHTML = `${c_desc}`;
}

/* section 3: dropdown */
function getRowDetails(list) { 
    var record = '';

    for (var i = 0; i < list.length; i++) {
        // declare variables
        var course_avail = 0;

        // learners details
        var name = list[i].name;
        var id = list[i].id; 
        var app_dt = list[i].apply_datetime;
        var class_id = list[i].class_id;
        var class_name = list[i].class;
        
        // input row details
        record += `<tr onclick="" id="${id}"><a href="#">

            <td class="text-center align-middle">${name}</td>
            <td class="text-center align-middle">${id}</td>
            <td class="text-center align-middle">${app_dt}</td>
            <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto'>Approve</p></td>

            <td><i class="fa bi bi-chevron-double-right" ></i></td>
            
        </a></tr>`;
    }

    return record;
}

// populate list
function getClassDropdown() { 
    var class_dropdown = document.getElementById('class_dropdown');
    const class_ls = jsonData[0].course_classes[course_selected];
    
    // get dropdown value
    var options = [];
    for (const [key, value] of Object.entries(class_ls)) {
        var class_name = value['class_name'];
        options.push(class_name);
    }
    console.log(options);


    for(var i = 0; i < options.length; i++) {
        var opt = options[i]; 
        //console.log(opt);
        
        // create element
        var li = document.createElement("li");
        var link = document.createElement("a");             
        var text = document.createTextNode(opt);
        link.appendChild(text);

        // set attributes: text, onclick event
        link.setAttribute("class", "dropdown-item");
        link.setAttribute("value", `${opt}`);
        link.setAttribute("onclick", `getLearnersOfClass('${opt}')`);
        //link.href = "#";
        
        li.appendChild(link);
        class_dropdown.appendChild(li);
    }

    console.log(class_dropdown);
}

function getAllLearnersOfClass() { 
    const learner_ls = jsonData[1][course_selected];
    var reg_ls = learner_ls.registered_learners;

    record = getRowDetails(reg_ls);

    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}

function getLearnersOfClass(class_name) { 
    const learner_ls = jsonData[1][course_selected];
    var reg_ls = learner_ls.registered_learners;
    console.log("class_name", class_name);
    //
    var class_reg_ls = [];
    //console.log(reg_ls); 
    for (const [key, value] of Object.entries(reg_ls)) {
        var curr_class_name = value['class'];

        if (class_name == curr_class_name) { 
            class_reg_ls.push(value);
        }
    }
    //console.log(class_reg_ls);

    // 
    record = getRowDetails(class_reg_ls);

    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}

/* section 4: tabs */
function getAllRegisteredLearners() { 
    const learner_ls = jsonData[1][course_selected];
    var reg_ls = learner_ls.registered_learners;

    var class_dropdown = document.getElementById('class_dropdown');
    console.log("class_dropdown: ", class_dropdown);
    console.log(reg_ls);

    document.getElementById("learners_list").innerHTML = "";
    
    //to set table headers
    if (document.getElementById("app_dt").classList.contains("d-none")) {
        document.getElementById("app_dt").classList.remove("d-none");
    }

    var record = '';
    for (var i = 0; i < reg_ls.length; i++) {
        // declare variables
        var course_avail = 0;

        // learners details
        var name = reg_ls[i].name;
        var id = reg_ls[i].id; 
        var app_dt = reg_ls[i].apply_datetime;
        var class_id = reg_ls[i].class_id;
        var class_name = reg_ls[i].class;
        
        // input row details
        record += `<tr>

            <td class="text-center align-middle">${name}</td>
            <td class="text-center align-middle">${id}</td>
            <td class="text-center align-middle">${app_dt}</td>
            <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto' onclick="approve_reg(${id})" id="${id}">Approve</p></td>
            
        </tr>`;
    }
    
    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}

function getAllEnrolledLearners() {
    const learner_ls = jsonData[1][course_selected];
    var enrolled_ls = learner_ls.enrolled_learners;

    console.log(enrolled_ls);

    document.getElementById("learners_list").innerHTML = "";

    var record = '';
    for (var i = 0; i < enrolled_ls.length; i++) {
        // declare variables
        var course_avail = 0;

        // learners details
        var name = enrolled_ls[i].name;
        var id = enrolled_ls[i].id; 
        // var app_dt = enrolled_ls[i].apply_datetime;
        var class_id = enrolled_ls[i].class_id;
        var class_name = enrolled_ls[i].class;
        
        // hide table header for application datetime 
        document.getElementById("app_dt").classList.add("d-none");

        // input row details
        record += `<tr>

            <td class="text-center align-middle">${name}</td>
            <td class="text-center align-middle">${id}</td>
            <td class="text-center align-middle my-auto"><p class='btn-danger btn rounded-pill align-middle my-auto' onclick="approve_reg(${id})" id="${id}">Withdraw</p></td>

            </tr>`;
    }
    
    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}

function getAllPreassignLearners() {
    const learner_ls = jsonData[1][course_selected];
    var preassign_ls = learner_ls.preassign_learners;
    
    console.log(class_selected);
    console.log(preassign_ls);

    document.getElementById("learners_list").innerHTML = "";

    //to set table headers
    // if (document.getElementById("app_dt").classList.contains("d-none")) {
    //     document.getElementById("app_dt").classList.remove("d-none");
    // }

    document.getElementById("app_dt").classList.add("d-none");

    var record = '';
    for (var i = 0; i < preassign_ls.length; i++) {
        // declare variables
        var course_avail = 0;

        // learners details
        var name = preassign_ls[i].name;
        var id = preassign_ls[i].id; 
        // var assign_deadline = preassign_ls[i].assign_deadline;
        var class_id = preassign_ls[i].class_id;
        var class_name = preassign_ls[i].class;
        
        // input row details
        record += `<tr>

        <td class="text-center align-middle">${name}</td>
        <td class="text-center align-middle">${id}</td>
        <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto' onclick="approve_reg(${id})" id="${id}">Assign</p></td>

        </tr>`;
    }
    
    // update table with data
    document.getElementById("learners_list").innerHTML = record;
}

function approve_reg(learner_id) {
    console.log(learner_id);
}