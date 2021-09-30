function getAllAvailableTrainers() {
    document.getElementById("assign_trainers_list").innerHTML = "";


    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var obj = JSON.parse(this.response);
            var assign_trainers = obj.assign_trainers;
            console.log(assign_trainers);

            var record = '';
            for (var i = 0; i < assign_trainers.length; i++) {
                var trainer_id = assign_trainers[i].trainer_id;
                var trainer_name = assign_trainers[i].trainer_name;
                var no_assigned_courses = assign_trainers[i].no_assigned_courses;

                record += `<tr>
                    <td class="text-center align-middle">${trainer_id}</td>
                    <td class="text-center align-middle">${trainer_name}</td>
                    <td class="text-center align-middle">${no_assigned_courses}</td>
                    <td class="text-center align-middle my-auto"><p class='btn-success btn rounded-pill align-middle my-auto'>Assign</p></td>
                  </tr>`;
            }
            document.getElementById("assign_trainers_list").innerHTML = record;
        }
    };

    url = "../hardcoded.json";
    request.open("GET", url, true);
    request.send();
};

function update_database() {
    
}