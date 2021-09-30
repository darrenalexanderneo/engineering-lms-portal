function getAllUnassignedCourses() {
    document.getElementById("trainers_list").innerHTML = "";


    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var unassigned = obj.unassigned_courses;
            console.log(unassigned);

            var record = '';
            for (var i = 0; i < unassigned.length; i++) {
                var course_name = unassigned[i].course_name;
                var class_id = unassigned[i].class_id;
                var start_date = unassigned[i].start_date;

                record += `<tr>
                    <td class="text-center align-middle">${course_name}</td>
                    <td class="text-center align-middle">${class_id}</td>
                    <td class="text-center align-middle">${start_date}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto'>Assign</p></td>
                  </tr>`;
            }
            document.getElementById("trainers_list").innerHTML = record;
        }
    };

    url = "../hardcoded.json";
    request.open("GET", url, true);
    request.send();
};

function getAllAssignedCourses() {
    document.getElementById("trainers_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var assigned = obj.assigned_courses;
            console.log(assigned);

            var record = '';
            for (var i = 0; i < assigned.length; i++) {
                var course_name = assigned[i].course_name;
                var class_id = assigned[i].class_id;
                var start_date = assigned[i].start_date;


                record += `<tr>
                    <td class="text-center align-middle">${course_name}</td>
                    <td class="text-center align-middle">${class_id}</td>
                    <td class="text-center align-middle">${start_date}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-danger btn rounded-pill align-middle my-auto'>Unassign</p></td>
                  </tr>`;
            }
            document.getElementById("trainers_list").innerHTML = record;
        }
    };

    url = "../hardcoded.json";
    request.open("GET", url, true);
    request.send();
};

function approve_reg_learners() {
// updates database by removing record from registered + adding record to enrolled

//refresh page
} 

function preassign_learners() {
// updates database by removing record from preassigned + adding record to ...??? (not sure)
}

function withdraw_learners() {
    //updates database by removing record from enrolled
}