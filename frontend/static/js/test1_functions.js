    // env file: without preload
    /*
    require('dotenv').config({
        path: `${_dirname}/.env.${process.env.NODE_ENV}`
    });
    console.log(`DIRECTORY: ${_dirname}/.env.${process.env.NODE_ENV}`);
    console.log("TEST: ", process.env.NUMBER);
    */
    // global variables
    //var course_name_ls = [];
    // var course_json = [];

    // load course_list data
    /*
    loadFile(`${env.COURSE_LIST_URL}`, function (response) {
        course_json.push(JSON.parse(response).data);
        //console.log(course_json);
        course_json = window.localStorage.setItem("course_json", JSON.stringify(course_json));
    })
    */
    // import the variables and function from module.js
    // import * as env from '../../apikey.js';

    // const storage = window.localStorage;

    var course_id;
    const storage = window.localStorage;
    // const course_list_url = storage.getItem("course_list_url");

    // document.body.onload = getAllCourses();

    export function getAllCourses() { 
      

        document.getElementById("course_list").innerHTML = "";
    
        // get course data
        const course_ls = JSON.parse(storage.getItem("course_json"));
        console.log("course_ls: ", course_ls);
    
        // get course_id
        /*for (var i = 0; i < course_ls.length; i++) { 
            var course_id = course_ls[i]['course_id'];
            course_name_ls.push(course_id);
        }
        console.log(course_name_ls);*/
        
        //
        var record = '';
        for (var i = 0; i < course_ls.courses.length; i++) {
            // declare variables
            // var course_avail = 0;
    
            // get course details
            var course_name = course_ls.courses[i].course_name;
            course_id = course_ls.courses[i].course_id;
            var num_of_classes = course_ls.courses[i].num_of_class;
            var total_slot_avail = course_ls.courses[i].slot_available;
    
            console.log(course_name);
            console.log(course_id);
    
    
            // input row details
            record += `<tr onclick="getAllLearners(this.id)" id="${course_id}"><a href="#">
    
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
    

    // when course is clicked, direct to another page
    // function getAllLearners(id) {
        
    //     asyncLocalStorage.setItem('course_selected', id);
    //     const course_selected = asyncLocalStorage.getItem('course_selected');
    //     console.log(course_selected);
        
    //     location.href = "v3_test2.html";
    // }


    // document.getElementById(course_id).addEventListener("click", getAllLearners(course_id));