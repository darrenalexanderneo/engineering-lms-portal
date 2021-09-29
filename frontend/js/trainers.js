function getAllRegisteredLearners() {
    document.getElementById("learners_list").innerHTML = "";


    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var registered = obj.registered_learners;
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

    url = "../hardcoded.json";
    request.open("GET", url, true);
    request.send();
};

function getAllEnrolledLearners() {
    document.getElementById("learners_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var registered = obj.enrolled_learners;
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
                    <td class="text-center align-middle my-auto"><p class='btn-danger btn rounded-pill align-middle my-auto'>Withdraw</p></td>
                  </tr>`;
            }
            document.getElementById("learners_list").innerHTML = record;
        }
    };

    url = "../hardcoded.json";
    request.open("GET", url, true);
    request.send();
};

function getAllPreassignLearners() {
    document.getElementById("learners_list").innerHTML = "";

    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var registered = obj.preassign_learners;
            console.log(registered);

            var record = '';
            for (var i = 0; i < registered.length; i++) {
                var name = registered[i].name;
                var id = registered[i].id;
                var apply_deadline = registered[i].apply_deadline;
                var class_section = registered[i].class;

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