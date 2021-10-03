function getAllRegisteredLearners() {
    document.getElementById("learners_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var registered = obj.ENG201.registered_learners;
            console.log(registered);

            var record = '';
            for (var i = 0; i < registered.length; i++) {
                var name = registered[i].name;
                var id = registered[i].id;
                var apply_datetime = registered[i].apply_datetime;
                var class_section = registered[i].class;

                record += `<tr>
                    <td class="text-center align-middle">${name}</td>
                    <td class="text-center align-middle">${id}</td>
                    <td class="text-center align-middle">${apply_datetime}</td>
                    <td class="text-center align-middle">${class_section}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto'>Approve</p></td>
                  </tr>`;
            }
            document.getElementById("learners_list").innerHTML = record;
        }
    };

    url = "../../templates/learners-v2.json";  // api endpoint example:  flask --> localhost:5000/learners/course/ENG101 OR AWS RDS --> some URL
    request.open("GET", url, true);
    request.send();
};

function getAllEnrolledLearners() {
    document.getElementById("learners_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var enrolled = obj.ENG201.enrolled_learners;
            console.log(enrolled);

            var record = '';
            for (var i = 0; i < enrolled.length; i++) {
                var name = enrolled[i].name;
                var id = enrolled[i].id;
                var apply_datetime = enrolled[i].apply_datetime;
                var class_section = enrolled[i].class;


                record += `<tr>
                    <td class="text-center align-middle">${name}</td>
                    <td class="text-center align-middle">${id}</td>
                    <td class="text-center align-middle">${apply_datetime}</td>
                    <td class="text-center align-middle">${class_section}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-danger btn rounded-pill align-middle my-auto'>Withdraw</p></td>
                  </tr>`;
            }
            document.getElementById("learners_list").innerHTML = record;
        }
    };

    url = "../../templates/learners-v2.json";  // api endpoint example:  flask --> localhost:5000/learners/course/ENG101 OR AWS RDS --> some URL
    request.open("GET", url, true);
    request.send();
};

function getAllPreassignLearners() {
    document.getElementById("learners_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var preassign = obj.ENG201.preassign_learners;
            console.log(preassign);

            var record = '';
            for (var i = 0; i < preassign.length; i++) {
                var name = preassign[i].name;
                var id = preassign[i].id;
                var apply_deadline = preassign[i].apply_deadline;
                var class_section = preassign[i].class;

                record += `<tr>
                    <td class="text-center align-middle">${name}</td>
                    <td class="text-center align-middle">${id}</td>
                    <td class="text-center align-middle">${apply_deadline}</td>
                    <td class="text-center align-middle">${class_section}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto'>Assign</p></td>
                  </tr>`;
            }
            document.getElementById("learners_list").innerHTML = record;
        }
    };

    url = "../../templates/learners-v2.json";  // api endpoint example:  flask --> localhost:5000/learners/course/ENG101 OR AWS RDS --> some URL
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