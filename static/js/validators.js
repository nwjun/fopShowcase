function turnValidShowErrMsgIfNotValid(input, yes, errMsg, invalidFeedbackEle) {
    /**
    * function to show input as valid or invalid
    * input: input element in field
    * yes: true if invalid-> valid
    * errMsg: message to show when field is invalid
    * invalidFeedbackEle: div element with class 'invalid-feedback'
    */
    if (yes) {
        // invalid -> valid
        input.classList.add('is-valid')
        input.classList.remove("is-invalid")
    } else {
        // valid -> invalid
        input.classList.add("is-invalid")
        input.classList.remove('is-valid')
        if (errMsg) {
            // add error message in invalid feedback element
            invalidFeedbackEle.innerHTML = errMsg
        }
    }
}

async function teamNameValidation(teamNameEle) {
    /**
    * function to validate team name on client side
    * teamNameEle: input element for team name
    */

    // globalThis.SCRIPT_ROOT is set in the "base.html"
    // it stores base URL to server
    const URL = globalThis.SCRIPT_ROOT + '/checkTeamName';
    let text = teamNameEle.value
    let invalid = document.getElementsByClassName('invalid-feedback')[0]
    if (text.length != 0) {
        if (text.length < 3 || text.length > 20) {
            turnValidShowErrMsgIfNotValid(teamNameEle, false, 'Name must be 3-20 characters', invalid)

        } else {
            let spinner = document.getElementById("spinnerTeamName")
            // show spinner when checking with server 
            // initially has display none, turning to block will show spinner
            spinner.style.display = "block"

            // sending GET request to server for checking availablity of team name
            const response = await fetch(URL + '?teamName=' + teamName.value)
                .then(data => { return data.json() })
                .then(res => {
                    result = res["result"]

                    if (result) {
                        turnValidShowErrMsgIfNotValid(teamNameEle, true, '')
                    } else {
                        turnValidShowErrMsgIfNotValid(teamNameEle, false, 'Team name is taken. Please use another name', invalid)
                    }
                })
                .catch(err => {
                    turnValidShowErrMsgIfNotValid(teamNameEle, false, err, invalid)
                })
                // stop showing spinner when request is responsed
                .finally(e => { spinner.style.display = "none" })
        }
    } else {
        removeValidInvalidClass(teamNameEle)
    }
}

function validateLength(element, min, max) {
    /**
    * function to validate length of element on client side
    */
    let text = element.value
    let length = text.length
    if (length < min || length > max) {
        return false
    } else {
        return true
    }
}

function memberNameValidation(element) {
    /**
    * function to validate member name on client side
    * teamNameEle: input element for member name
    */
    if ((element.value).length != 0) {
        if (validateLength(element, 2, 25)) {
            turnValidShowErrMsgIfNotValid(element, true)
        } else {
            turnValidShowErrMsgIfNotValid(element)
        }
    } else {
        removeValidInvalidClass(element)
    }

}

function addMember(addBtn, memberDiv) {
    /**
    * function to add member group containing input and remove button when add button is pressed
    * remove button is attached with listener which will delete whole member group when pressed.
    * 
    * addBtn: button to attach listener
    * memberDiv: div containing all member group
    * 
    * member group:
    * <div class="input-group mb-3"><input class="form-control input-needs-validation" type="text"
    *     aria-label="Who are your team members?" required="" minlength="2" maxlength="25" name="teamMembers[1]"
    *     placeholder="2-25 characters" id="teamMember[1]"><button type="button" class="btn btn-danger">Remove</button>
    *     <div class="invalid-feedback">Name must be 2-25 characters</div>
    * </div>
    */
    let container = document.createElement('div')

    let inputGroupDiv = document.createElement("div")
    inputGroupDiv.classList.add("input-group", "mb-3")

    let input = document.createElement("input")
    input.classList.add("form-control", "input-needs-validation")
    input.type = "text"
    input.ariaLabel = "Who are your team members?"
    input.required = true;
    input.minLength = "2";
    input.maxLength = "25";
    input.name = `teamMembers[${memberDiv.childElementCount}]`
    input.placeholder = "2-25 characters"
    input.id = `teamMember[${memberDiv.childElementCount}]`

    let btn = document.createElement("button")
    btn.innerHTML = "Remove"
    btn.type = "button"
    btn.classList.add("btn", "btn-danger")
    btn.onclick = function () {
        memberDiv.removeChild(container)
        addBtn.disabled = false
    };

    let invalidFeedback = document.createElement("div")
    invalidFeedback.classList.add('invalid-feedback')
    invalidFeedback.innerHTML = 'Name must be 2-25 characters'

    // add input and btn to inputGroupDiv
    inputGroupDiv.appendChild(input)
    inputGroupDiv.appendChild(btn)

    container.appendChild(inputGroupDiv)
    inputGroupDiv.appendChild(invalidFeedback)

    memberDiv.appendChild(container)
    input.addEventListener('blur', f => memberNameValidation(input))
    input.addEventListener('focus', removeValidInvalidClass(input))

    // maximum of member in a group is 6
    if (memberDiv.childElementCount == 6) {
        addBtn.disabled = true
    }
}

function regexValidateEmail(email) {
    /**
     * function to validate email using regex
     * return true if email is valid, else return false
     */
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
        return true
    }
    return false
}

function emailValidation(email) {
    /**
     * function to response to email validation
     */
    result = regexValidateEmail(email.value)
    if (email.value) {
        if (result) {
            turnValidShowErrMsgIfNotValid(email, true)
        } else {
            turnValidShowErrMsgIfNotValid(email, false)
        }
    } else {
        removeValidInvalidClass(email)
    }
}

async function validateUrl(url) {
    /**
     * function to validate url by sending GET request to Flask server
     * response in {"result": true} if url is valid else {"result":false}
     * 
     */
    result = await fetch(globalThis.SCRIPT_ROOT + '/checkLink' + '?u=' + url)
        .then(data => { return data.json() })
        .catch(err => {
            console.log("Error when validating url:" + err)
            return false
        })
    if (result['result']) {
        return true
    } else {
        return false
    }
}

async function isYoutubeVideoId(id) {
    /**
     * function to check whether youtube id exist
     */
    // this url will direct to thumbmail of youtube
    const url = "http://img.youtube.com/vi/" + id + "/mqdefault.jpg";
    return await validateUrl(url)
}

async function videoLinkValidation(element) {
    /**
     * function to check whether youtube id is valid
     */
    if ((element.value).length != 0) {
        // show spinner when checking, hide it when checking is done
        let spinner = document.getElementById("spinnerVideoLink")
        spinner.style.display = "block"
        isYoutubeVideoId(element.value)
            .then(k => {
                if (k)
                    turnValidShowErrMsgIfNotValid(element, true)
                else
                    turnValidShowErrMsgIfNotValid(element)
            })
            .catch(err => console.log("Error in validating video link: " + err))
            .finally(() => spinner.style.display = "none")
    }
    else {
        removeValidInvalidClass()
    }
}

async function isGithubLink(link) {
    /**
     * function to check whether github repo exist
     */
    regExp = /\//i;
    if (regExp.test(link)) {
        const url = "https://github.com/" + link
        return await validateUrl(url)
    }
    return false
}

async function githubLinkValidation(element) {
    /**
     * function to check whether github repo is valid
     */
    if ((element.value).length != 0) {
        element.classList.add("input-needs-validation")
        let spinner = document.getElementById("spinnerGithubLink")
        spinner.style.display = "block"
        isGithubLink(element.value)
            .then(k => {
                if (k)
                    turnValidShowErrMsgIfNotValid(element, true)
                else
                    turnValidShowErrMsgIfNotValid(element)
            })
            .catch(err => console.log("Error in validating github link: " + err))
            .finally(() => spinner.style.display = "none")
    }
    else {
        element.classList.remove("input-needs-validation")
        removeValidInvalidClass(element)
    }
}

function descriptionValidation(element) {
    /**
     * function to validate description
     * description must be 20 - 500 characters
     */
    count = element.value.length
    if (count != 0) {
        if (count < 20 || count > 500) {
            turnValidShowErrMsgIfNotValid(element, false)
        } else {
            turnValidShowErrMsgIfNotValid(element, true)
        }
    } else {
        removeValidInvalidClass(element)
    }
}

function removeValidInvalidClass(element) {
    /**
     * function to remove "is-invalid" and "is-valid" classes in element
     */
    element.classList.remove("is-invalid")
    element.classList.remove("is-valid")
}