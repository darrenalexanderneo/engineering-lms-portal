    /***** STORAGE *****/
    const storage = window.localStorage;
    // const asyncLocalStorage = {
    //   setItem: async function (key, value) {
    //       await null;
    //       return storage.setItem(key, value);
    //   },
    //   getItem: async function (key) {
    //       await null;
    //       return storage.getItem(key);
    //   }
    // };

    /***** VARIABLES *****/
    // hardcoded learner
    // const learner_id = "LNR8"; 

    // GET learner_id from localStorage (stored in login.html)
    const learner_id = storage.getItem("learner_id");  
    console.log(learner_id);

    document.getElementById("learner-id").innerHTML = learner_id;


    var course_id;
    var getRegCoursesURL;
    var withdrawLearnerURL;

    // to retrieve api keys without exposing
    async function getAPIkeys () {  
      var request = new XMLHttpRequest();
      request.onreadystatechange = function () {
          if (this.readyState == 4 && this.status == 200) {
              var api_keys = JSON.parse(this.response);
              // getRegCoursesURL = api_keys.getRegCoursesURL;
              // withdrawLearnerURL = api_keys.withdrawLearnerURL;
              getRegCoursesURL = api_keys.getEnrollmentStatus;
              withdrawLearnerURL = api_keys.withdraw_POST;
              // console.log(getRegCoursesURL);
              // console.log(withdrawLearnerURL);
          }
      }
      request.open("GET", "../../apikey.json", false);
      request.send();
    }

    /***** LOAD FILES *****/
    // callback function to load files, reference from https://stackoverflow.com/questions/12460378/how-to-get-json-from-url-in-javascript
    var getJSON = function (url, done) {
      var xhr = new XMLHttpRequest();
      xhr.onload = function () { return done(this.response) }
      xhr.open("GET", url, true);
      xhr.send();
   }
    
    async function load() {
        // console.log("url: ", getRegisteredCourses)
        
        let obj = await (await fetch(`${getRegCoursesURL}${learner_id}`)).json();
        console.log(obj);
    }
    
    /***** REGISTRATION FUNCTION *****/
    // display table
    function showClassesforRegistration (learner_id) {
        getAPIkeys();
        // console.log(`${getRegCoursesURL}${learner_id}`);
        console.log("learner_id: ", learner_id);

        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                console.log(this.response);
                var reg_courses = JSON.parse(this.response).results;
                console.log("# of reg courses: ", reg_courses.length);
                console.log(reg_courses);

                document.getElementById("reg-course-body").innerHTML = '';

                if (reg_courses.length == 0) {
                  // show message
                  console.log("** 0 **");
                  document.getElementById("no-reg-course").classList.remove("d-none");
                  document.getElementById("reg-course").classList.add("d-none"); //ensure that reg-course does not show on reload
                } else {
                  console.log("** >=1 **");
                  document.getElementById("no-reg-course").classList.add("d-none");
                  document.getElementById("reg-course").classList.remove("d-none"); //ensure that no-reg-course does not show on reload

                  var html_content = "";

                  for (course of reg_courses) { 
                    var class_id = course.class_id;
                    var course_id = course.course_id;  
                    var course_name = course.course_name;  
                    var is_approved = course.is_approved;  // boolean value 
                    var course_detail = `${course_name} (${course_id}) of Class ${class_id}`;
                    console.log(course_detail);

                    html_content += 
                    `
                    <tr>
                      <td scope="row">${course_id}</td>
                      <td>${class_id.slice(-1)}</td>
                      <td>${course_name}</td>
                      <td class="text-secondary">${is_approved == 0? "Pending" : "Approved"}</td>
                      <td><button type="button" class="btn btn-outline-danger" onclick="exampleOnclick(this, '${class_id}', '${course_id}', ${is_approved})">Withdraw</button></td>
                    </tr>
                    `;
                  }

                  document.getElementById("reg-course-body").innerHTML = html_content;
                }   
            }
        }

        var url = `${getRegCoursesURL}${learner_id}`;
        console.log(url);
        request.open("GET", url, true);
        request.send();
      }
    

      /***** WITHDRAW BUTTON ONCLICK *****/
      // display modal when withdraw button is clicked
      function exampleOnclick(btn, class_id, course_id, is_approved) {
          // console.log(course_detail)

          var name = btn.innerHTML;
          var exampleModal = getExampleModal();

          // Init the modal if it hasn't been already.
          if (!exampleModal) { exampleModal = initExampleModal(); }
          
          initExampleModal()
          var html =
              `<div class="modal-header">
                  <h5 class="modal-title" id="exampleModalLabel">Withdraw</h5>
                </div>
                <div class="modal-body">
                  Are you sure you want to withdraw your ${is_approved == 0? "registration" : "enrollment"}?
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-dismiss="modal" onclick="closeModal()" id="modal-close-btn">Close</button>
                  <button type="button" class="btn btn-danger" onclick="withdrawLearner('${class_id}', '${course_id}', '${is_approved}')">Withdraw</button>
                </div>`;
        
          setExampleModalContent(html);
        
          // Show the modal.
          jQuery(exampleModal).modal('show');
        
        }

        
      // send a POST request when withdraw button is clicked
      function withdrawLearner(class_id, course_id, is_approved) {
        console.log(class_id, course_id, is_approved, learner_id);

        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                
              try {
                console.log("ready state: ", this.readyState, this.status);

                alert_msg = `withdrawal is successful`;
                window.localStorage.setItem("alert_msg", alert_msg);
                window.localStorage.setItem("learner_id", learner_id);
                
                setTimeout(function() {
                  console.log('hehe')
                  alert(localStorage['alert_msg']);
                  location.reload();
                  
                }, 850);
                
                jQuery(exampleModal).modal('hide');
              }
              catch(err) {
                showError('There is a problem retrieving data, please try again later.<br />' + err);
              }
            }
        }

        var data = JSON.stringify({ 'class_id': `${class_id}`,  
                                    'course_id': `${course_id}`,
                                    'learner_id': `${learner_id}`,
                                    'is_approved': parseInt(is_approved)
        });

        console.log(data);
        request.open("POST", withdrawLearnerURL, true, "/json-handler");
        request.setRequestHeader("Content-Type", "application/json");
        request.send(data);   

      }


        /***** HELPER FUNCTIONS *****/
        function getExampleModal() {
          return document.getElementById('exampleModal');
        }
        
        function setExampleModalContent(html) {
          getExampleModal().querySelector('.modal-content').innerHTML = html;
        }
        
        function initExampleModal() {
          var modal = document.createElement('div');
          modal.classList.add('modal', 'fade');
          modal.setAttribute('id', 'exampleModal');
          modal.setAttribute('tabindex', '-1');
          modal.setAttribute('role', 'dialog');
          modal.setAttribute('aria-labelledby', 'exampleModalLabel');
          modal.setAttribute('aria-hidden', 'true');
          modal.innerHTML =
                '<div class="modal-dialog" role="document">' +
                  '<div class="modal-content"></div>' +
                '</div>';

      
          document.body.appendChild(modal);
          // console.log("modal", modal)
          return modal;
        }
        
        function closeModal() {
          console.log('close')
          jQuery(exampleModal).modal('hide');
        }

        // LOGOUT FUNCTION
        function logout () {
            storage.clear();


            window.location.replace("./login.html");
        }