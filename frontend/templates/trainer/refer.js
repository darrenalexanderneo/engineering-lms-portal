import {session} from 'wix-storage';
import wixWindow from 'wix-window';
import wixData from 'wix-data';
import wixLocation from 'wix-location';

// NOTE: Redirect to this application page has been included in:
// Dynamic Pages > Project Pages (Dynamic) > Projects - Detailed (DRAFT)
// Project details have also been set in session in the above page.


const APP_TYPE = {
	INDIVIDUAL: {
		TYPE: "individual",
		MSG: "This project can be only applied as an individual"
	},
	GROUP: {
		TYPE: "group",
		MSG: "This project can be applied as a group"
	}
}
const FIELD_NAMES = [
	"name", 
	"contact", 
	"email", 
	"school", 
	"occupation",
	"portfolio"
]

const REQUIRED_FIELD_NAMES = [
	"name", 
	"contact", 
	"email", 
	"occupation",
	"resume"
]
let appType
let currNumOfVolsDisplayed = 1
let maxVols // dummy variable ***
let maxVolsMsg

class VolDetails {
	// NOTE: no "Resume/CV" attribute as this is a upload file input -
	// there is a getter but no setter, so retrieving and placing this value in
	// a new container is not possible
	constructor(name, contact, email, school, occupation, resume) {
		this.name = name
		this.contact = contact
		this.email = email
		this.school = school
		this.occupation = occupation
	}
}

$w.onReady(function () {
	// REMOVE THIS LATER WHEN MERGED - Set mock session data
	// session.setItem("projectId", "209e99ca-6cbd-4bf7-9ea1-00bdba85f738");
	// session.setItem("projectName", "Dummy Project Name");
	// session.setItem("organizationName", "10.10 Media Productions");
	// session.setItem("numberOfVolunteers", 5)

	// Retrieve project details
	const projectId = session.getItem("projectId")
	const projectName = session.getItem("projectName")
	const organizationName = session.getItem("organizationName")
	const numberOfVolunteers = parseInt(session.getItem("numberOfVolunteers"))

	// Check if application is for individual or group
	// Since there's a limit of 5 volunteer Section 1 components in this application form,
	// the limit will be 5.
	maxVols = numberOfVolunteers > 5 ? 5 : numberOfVolunteers
	appType = maxVols > 1 ? APP_TYPE.GROUP : APP_TYPE.INDIVIDUAL
	if (appType == APP_TYPE.GROUP) {

		$w("#appIntroText").text = `${APP_TYPE.GROUP.MSG} (max ${maxVols} volunteers).`

		maxVolsMsg = `Maximum of ${maxVols} volunteers only.`
		$w("#maxVolsText").text = maxVolsMsg

		$w("#section3heading").text = "Let us know your availability."
		$w("#section4heading").text = "Share what makes you interested in joining this project!"
		$w("#vol1header").text = "Volunteer #1"


	} else if (appType == APP_TYPE.INDIVIDUAL) {

		$w("#appIntroText").text = `${APP_TYPE.INDIVIDUAL.MSG}.`

		$w("#volStripIndividual").expand()
		$w("#volStrip1").collapse()

		$w("#addVolStrip").collapse()
		$w("#individualIcon").show()
		$w("#groupIcon").hide()

		$w("#section3heading").text = "Let us know your availability."
		$w("#section4heading").text = "Share what makes you interested in joining this project!"

	}

	$w("#breadcrumb2").label = projectName
	// Set project details (i.e. "You have selected to apply for...") once page loads
	$w("#projectDetailText").html = `
		<p style="font-size: 16px; color: #2A2A2A; font-family: 'Open Sans'">
			You have selected to apply for 
				<span style="font-weight: 700">${projectName}</span> with 
				<span style="font-weight: 700">${organizationName}</span>.
		</p>`

	// Clicking on the privacy clause will check the corresponding checkbox
	$w("#privacyPolicyCheckboxGrp").onClick((event) => {
		let privacyClauseCheckbox = $w("#privacyClauseCheckbox")
		privacyClauseCheckbox.checked = !privacyClauseCheckbox.checked
	})
});

/**
 *	Adds an event handler that runs when the element is clicked.
 *	 @param {$w.MouseEvent} event
 */
export function addVolBtn_click(event) {
	// console.log("Add vol button clicked") COMMENTED OUT FOR DEPLOYMENT
	
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	if (currNumOfVolsDisplayed <= maxVols) {
		currNumOfVolsDisplayed += 1
		const idOfNextVolStrip = `volStrip${currNumOfVolsDisplayed}`
		// console.log("clicked add volunteer to expand id:", `#${idOfNextVolStrip}`) COMMENTED OUT FOR DEPLOYMENT
		$w(`#${idOfNextVolStrip}`).expand() 


		// call function to initialise all input fields to avoid the red outline
		initialiseInputFields(currNumOfVolsDisplayed)

		initialiseHeaders()

	}

	


	if (currNumOfVolsDisplayed == maxVols) {
		// console.log("Max. vols reached") COMMENTED OUT FOR DEPLOYMENT
		$w("#addVolBtn").collapse()
		$w("#maxVolsText").show()
	}
}

function initialiseInputFields(idxInput){
	// console.log("initialising input fields....") COMMENTED OUT FOR DEPLOYMENT
	$w(`#nameField${idxInput}`).resetValidityIndication()
	$w(`#contactField${idxInput}`).resetValidityIndication()
	$w(`#emailField${idxInput}`).resetValidityIndication()
	// $w(`#schoolField${idxInput}`).value = ""
	$w(`#occupationField${idxInput}`).resetValidityIndication()

}

function initialiseHeaders(){
		// update the text being shown 
		if (currNumOfVolsDisplayed > 1) { 
			$w("#vol1header").text = "Volunteer #1 - Team Leader"

			$w("#section3heading").text = "Let us know your team's availability."
			$w("#section4heading").text = "Share what makes your team interested in joining this project!"

		}
		else if(currNumOfVolsDisplayed == 1){
			$w("#vol1header").text = "Volunteer #1"

			$w("#section3heading").text = "Let us know your availability."
			$w("#section4heading").text = "Share what makes you interested in joining this project!"

		}
}

/**
 *	Adds an event handler that runs when the element is clicked.
 *	 @param {$w.MouseEvent} event
 */
export function volDelBtn_click(event) {
	// console.log("Vol delete button clicked") COMMENTED OUT FOR DEPLOYMENT
	const containerToDelete = event.target.id
	const idxToDelete = parseInt(containerToDelete.slice(containerToDelete.length - 1))
	let volToDeleteIsEmpty = true

	for (let i = 0; i < FIELD_NAMES.length; i++) {
		let attribute = FIELD_NAMES[i]
		// console.log( FIELD_NAMES[i] , $w(`#${attribute}Field${idxToDelete}`).value ) COMMENTED OUT FOR DEPLOYMENT
		if(attribute === "school"){
			volToDeleteIsEmpty = volToDeleteIsEmpty && ($w(`#${attribute}Field${idxToDelete}`).value === undefined || $w(`#${attribute}Field${idxToDelete}`).value == "")
		}
		else{
			volToDeleteIsEmpty = volToDeleteIsEmpty && $w(`#${attribute}Field${idxToDelete}`).value == ""
		}
	}

	// Do not open Lightbox for confirmation if there are no existing values in the to-be-deleted container
	if (volToDeleteIsEmpty) {
		updateFieldValues(idxToDelete)
		initialiseHeaders()
	} 
	else {
		$w(`#rmvOverlay${idxToDelete}`).expand()

	// Open Lightbox for confirmation to delete
	// 	wixWindow.openLightbox("Application - Delete Volunteer")
	// 		.then((data) => {
	// 			// Only delete if "Confirm" is clicked
	// 			if (data[0].toDelete) {
	// 				updateFieldValues(idxToDelete)
	// 			}
	// 		})
	}



}

export function cancelRemove(event){

	// console.log("cancel remove volunteer ") COMMENTED OUT FOR DEPLOYMENT
	const containerToDelete = event.target.id
	const idxToDelete = parseInt(containerToDelete.slice(containerToDelete.length - 1))
	

	$w(`#rmvOverlay${idxToDelete}`).collapse()


}

export function confirmRemove(event){

	// console.log("confirm remove volunteer ") COMMENTED OUT FOR DEPLOYMENT

	const containerToDelete = event.target.id
	const idxToDelete = parseInt(containerToDelete.slice(containerToDelete.length - 1))

	updateFieldValues(idxToDelete)
	$w(`#rmvOverlay${idxToDelete}`).collapse()
	initialiseHeaders()


}

function updateFieldValues(idxToDelete) {
	let existingInputValues = [] // arr of VolDetails objects
	let nameFieldVal, contactFieldVal, emailFieldVal, schoolFieldVal, occupationFieldVal

	// collect all inputs after the selected container to be deleted
	if (currNumOfVolsDisplayed > idxToDelete) {
		for (let i = idxToDelete + 1; i <= currNumOfVolsDisplayed; i++) {
			nameFieldVal = $w(`#nameField${i}`).value
			contactFieldVal = $w(`#contactField${i}`).value
			emailFieldVal = $w(`#emailField${i}`).value
			schoolFieldVal = $w(`#schoolField${i}`).value
			occupationFieldVal = $w(`#occupationField${i}`).value

			existingInputValues.push(
				new VolDetails(
					nameFieldVal,	
					contactFieldVal,	
					emailFieldVal,	
					schoolFieldVal,
					occupationFieldVal
				)
			)
		}
		// update containers, only without the deleted container's values
		for (let i = idxToDelete; i <= currNumOfVolsDisplayed - 1; i++) {
			const currFieldValues = existingInputValues.shift()
			for (let j = 0; j < FIELD_NAMES.length; j++) {
				let attribute = FIELD_NAMES[j]
				$w(`#${attribute}Field${i}`).value = currFieldValues[attribute]
			}
		}
	}

	// remove the populated values in fields of last element
	// (i.e. the one that is collapsed)
	for (let i = 0; i < FIELD_NAMES.length; i++) {
		let attribute = FIELD_NAMES[i]
		$w(`#${attribute}Field${currNumOfVolsDisplayed}`).value = ""
	}

	$w(`#volStrip${currNumOfVolsDisplayed}`).collapse()
	currNumOfVolsDisplayed -= 1

	// Display the add vol button again if currNumOfVolsDisplayed < max
	if (currNumOfVolsDisplayed == maxVols - 1) {
		$w("#addVolBtn").expand()
		$w("#maxVolsText").hide()
	}
}

/**
 *	 SUBMISSION FUNCTIONS
 */
class ApplicationDetails {
	// NOTE: no "Resume/CV" attribute as this is a upload file input -
	// there is a getter but no setter, so retrieving and placing this value in
	// a new container is not possible
	
	constructor(projectName, organizationName, projectID , name, contact, email, school, occupation, resumeFile, portfolioLink, comment, availableDate, groupID) {

	
		this.name = name
		this.contactNumber = contact
		this.email = email
		this.school = school
		this.occupation = occupation
		this.resume =  resumeFile
		this.portfolioLink = portfolioLink
		this.comments = comment
		this.availableDate = availableDate
		this.projects = projectID
		this.projectName = projectName
		this.organizationName =organizationName
		this.group = groupID

	}
}


function validateFields(numOfApplications){

	let validate = true
	let startIdx = 1  // default for group application

	if (appType == APP_TYPE.INDIVIDUAL){
		numOfApplications = 0  // to allow only one iteration 
		startIdx = 0
	}

	for(let idx = startIdx; idx <= numOfApplications; idx++ )
		for (let i = 0; i < REQUIRED_FIELD_NAMES.length; i++) {
			let attribute = REQUIRED_FIELD_NAMES[i]
			if(attribute == "resume"){
				validate = validate && (($w(`#${attribute}Field${idx}`).value.length > 0))
				if(!($w(`#${attribute}Field${idx}`).value.length > 0)){
					$w(`#${attribute}Field${idx}`).updateValidityIndication()  //reset value to create the red required outline
				}
			}
			else{
				validate = validate && ($w(`#${attribute}Field${idx}`).value !== null && $w(`#${attribute}Field${idx}`).value !== "")
				if(!($w(`#${attribute}Field${idx}`).value !== null && $w(`#${attribute}Field${idx}`).value !== "")){  
					$w(`#${attribute}Field${idx}`).value = ""  //reset value to create the red required outline
				}
			}

			
		}
	validate = validate && ( $w(`#interestDescText`).value !== null  && $w(`#interestDescText`).value !== "")  // check validation of essay
	if(!( $w(`#interestDescText`).value !== null  && $w(`#interestDescText`).value !== "")){
		$w(`#interestDescText`).value = ""
	}

	// console.log("VALIDATION" , validate) COMMENTED OUT FOR DEPLOYMENT
	return validate

}

export async function submitButton_click(event) {
	
	if(!validateFields(currNumOfVolsDisplayed)){
		$w("#feedbackText").text = "Please fill in the required fields outlined in red."
		$w("#errorIcon").show()
		$w("#loadingIcon").hide()
		$w("#feedbackBox").expand()
	}
	else if(!$w("#checkbox2").checked){
		//show error
		$w("#feedbackText").text = "Please accept the Terms and Conditions before submitting."
		$w("#checkbox2").updateValidityIndication()
		$w("#errorIcon").show()
		$w("#loadingIcon").hide()
		$w("#feedbackBox").expand()
	}
	else{

		$w("#feedbackBox").collapse()
	

		// console.log(" opening confirmation box ") COMMENTED OUT FOR DEPLOYMENT
		wixWindow.openLightbox("Application - Confirm Application")
		.then(async (data) => {
			if(data === null){
				// console.log("no confirmation") COMMENTED OUT FOR DEPLOYMENT
				return
			}
			if (data[0].confirmApplication) {
				$w("#feedbackText").text = "We are currently processing your application, just a little while more!"
				$w("#errorIcon").hide()
				$w("#loadingIcon").show()
				$w("#feedbackBox").expand()

				var startIdx;
				var numOfApplications;
				var groupNumber; 

				const projectId = session.getItem("projectId")
				const projectName = session.getItem("projectName")
				const organizationName = session.getItem("organizationName")

				let comment = $w('#interestDescText').value
				let availableDate=  $w('#datePicker1').value

				if (appType == APP_TYPE.INDIVIDUAL){

					numOfApplications = 0
					startIdx = 0
					groupNumber = null
		
				}
				else if(appType == APP_TYPE.GROUP && currNumOfVolsDisplayed == 1){   //for application that allows group but only one vol applied
					numOfApplications = 1
					startIdx = 1 //for group application - vol #1
					groupNumber = null
				}
				else
				{
					startIdx = 1
 					numOfApplications = currNumOfVolsDisplayed
					// console.log("query Applications Data") COMMENTED OUT FOR DEPLOYMENT
					groupNumber = await wixData.query("Applications")
						.isNotEmpty("group")
						.descending("group")
						.limit(1)
						.distinct("group", {"suppressAuth": true, "suppressHooks": true})
						.then(r => {
						let lastID= r.items[0];
						// console.log(lastID) COMMENTED OUT FOR DEPLOYMENT
						let nextID = lastID ? lastID + 1 : 1;
						// console.log("in query " , nextID) COMMENTED OUT FOR DEPLOYMENT
						return nextID
						})

					// console.log("Group number ", groupNumber) COMMENTED OUT FOR DEPLOYMENT

				}

				for (let i = startIdx ; i <= numOfApplications; i++) {
						let nameFieldVal = $w(`#nameField${i}`).value
						let contactFieldVal = $w(`#contactField${i}`).value
						let emailFieldVal = $w(`#emailField${i}`).value
						let schoolFieldVal = $w(`#schoolField${i}`).value == "" ||$w(`#schoolField${i}`).value === undefined ? "NA" : $w(`#schoolField${i}`).value

						let occupationFieldVal = $w(`#occupationField${i}`).value

						let isStudent = occupationFieldVal.includes("student") || occupationFieldVal.includes("undergraduate") 
						// Standardise Student Input Choice
						if(isStudent){ 
							occupationFieldVal = "Student"
						}
		
						let portfolioFieldVal = $w(`#portfolioField${i}`).value

					
						let resumeFile = await $w(`#resumeField${i}`).uploadFiles()
							.then( (uploadedFiles) => {
								
								// console.log('File url:', uploadedFiles[0].fileUrl); COMMENTED OUT FOR DEPLOYMENT
								return uploadedFiles[0].fileUrl
							
							})
							.catch( (uploadError) => {
								let errCode = uploadError.errorCode;  // 7751
								let errDesc = uploadError.errorDescription; // "Error description"
							} );


						// console.log('after uploaded File url:',resumeFile); COMMENTED OUT FOR DEPLOYMENT


						let toInsert =  new ApplicationDetails(
							projectName, 
							organizationName, 
							projectId ,  
							nameFieldVal,	
							contactFieldVal,	
							emailFieldVal,	
							schoolFieldVal,
							occupationFieldVal,
							resumeFile,
							portfolioFieldVal,
							comment, 
							availableDate,
							groupNumber
						)


						await wixData.insert("Applications", toInsert)
							.then( (results) => {
								// console.log("insertingg " , results) COMMENTED OUT FOR DEPLOYMENT
								let item = results; //see item below
							} )
							.catch( (err) => {
								let errorMsg = err;
								// console.log("inserting application error ", err) COMMENTED OUT FOR DEPLOYMENT
							} );
				
					}
				$w("#feedbackBox").collapse()
				$w("#successBox").expand()
				wixLocation.to("/thank-you-pg");


				return
			}

		});

	}
}





/**
*	Adds an event handler that runs when the input element receives
input.
*	 @param {$w.Event} event
*/
export function occupationField_input(event) {

	let field = event.target.id
	const idx = parseInt(field.slice(field.length - 1))
	
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 

	let occupationValue = $w(`#occupationField${idx}`).value.toLowerCase()
	// console.log(occupationValue) COMMENTED OUT FOR DEPLOYMENT
	let isStudent = occupationValue.includes("student") || occupationValue.includes("undergraduate") 

	if(isStudent){
		// console.log("applicant is student") COMMENTED OUT FOR DEPLOYMENT
		$w(`#schoolInputGrp${idx}`).expand()

	}
	else if(!isStudent && !$w(`#schoolInputGrp${idx}`).collapsed){
		$w(`#schoolInputGrp${idx}`).collapse()

	}


}

/**
 *	Adds an event handler that runs when the element is clicked.
 *	 @param {$w.MouseEvent} event
 */
export function breadcrumb2_click(event) {
	// This function was added from the Properties & Events panel. To learn more, visit http://wix.to/UcBnC-4
	// Add your code for this event here: 
	// console.log("project link clicked") COMMENTED OUT FOR DEPLOYMENT
	let projID = session.getItem("projectId")
	let projURL = wixData.get("Projects", projID)
		.then( (results) => {
			let item = results; //see item below
			// console.log(item) COMMENTED OUT FOR DEPLOYMENT
			let field ="link-projects-3-projOrgName"
			// console.log(item[field]) COMMENTED OUT FOR DEPLOYMENT
			wixLocation.to( item[field]);

			return
		} )
		.catch( (err) => {
			let errorMsg = err;
		});




}