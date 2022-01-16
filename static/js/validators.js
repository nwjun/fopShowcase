function turnValidShowErrMsgIfNotValid(input, yes, errMsg, invalidFeedbackEle) {
    if (yes) {
        input.classList.add('is-valid')
        input.classList.remove("is-invalid")
    } else {
        input.classList.add("is-invalid")
        input.classList.remove('is-valid')
        if (errMsg) {
            invalidFeedbackEle.innerHTML = errMsg
        }
    }
}

async function teamNameValidation(teamNameEle) {
    const URL = globalThis.SCRIPT_ROOT + '/checkTeamName';
    let text = teamNameEle.value
    let invalid = document.getElementsByClassName('invalid-feedback')[0]
    if (text.length != 0) {
        if (text.length < 3 || text.length > 20) {
            turnValidShowErrMsgIfNotValid(teamNameEle, false, 'Name must be 3-20 characters', invalid)

        } else {
            let spinner = document.getElementById("spinnerTeamName")
            spinner.style.display = "block"

            const response = await fetch(URL + '?teamName=' + teamName.value)
                .then(data => { return data.json() })
                .then(res => {
                    // let result = res["result"]
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
                .finally(e => { spinner.style.display = "none" })
        }
    } else {
        removeValidInvalidClass(teamNameEle)
    }
}

function validateLength(element, min, max) {
    let text = element.value
    let length = text.length
    if (length < min || length > max) {
        return false
    } else {
        return true
    }
}

function memberNameValidation(element) {
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
    input.id = `teamMember[${memberDiv.childElementCount - 1}]`

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

    inputGroupDiv.appendChild(input)
    inputGroupDiv.appendChild(btn)

    container.appendChild(inputGroupDiv)
    inputGroupDiv.appendChild(invalidFeedback)

    memberDiv.appendChild(container)
    input.addEventListener('blur', f => memberNameValidation(input))
    input.addEventListener('focus', removeValidInvalidClass(input))

    if (memberDiv.childElementCount == 6) {
        addBtn.disabled = true
    }
}

function regexValidateEmail(mail) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail)) {
        return true
    }
    return false
}

function emailValidation(email) {
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
    const url = "http://img.youtube.com/vi/" + id + "/mqdefault.jpg";
    return await validateUrl(url)
}

async function videoLinkValidation(element) {
    if ((element.value).length != 0) {
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
    regExp = /\//i;
    if (regExp.test(link)) {
        const url = "https://github.com/" + link
        return await validateUrl(url)
    }
    return false
}

async function githubLinkValidation(element) {
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
    element.classList.remove("is-invalid")
    element.classList.remove("is-valid")
}