from wtforms import ValidationError, Form, StringField, validators, EmailField
import requests

def validateLink(url, errMsg):
    try:
        r= requests.get(url)
        if r.status_code == 404:
            raise ValidationError(errMsg)

    except Exception as err:
        raise ValidationError(err)

def videoLinkValidation(form,field):
    url = "http://img.youtube.com/vi/" + field.data + "/mqdefault.jpg"
    validateLink(url,"Invalid video id")

def githubLinkValidation(form, field):
    url = "https://github.com/" + field.data
    validateLink(url,"Invalid github link")

def validation(teamMembers, description, projectName, PROJECTS_NAMES):
    errors = []
    length = len(description)

    if length < 20 or length > 500:
        errors.append(
            'Description must be between 20 and 500 characters long.')

    if projectName not in PROJECTS_NAMES:
        errors.append('Project is not a valid choice')

    for name in teamMembers:
        if len(name) < 2 or len(name) > 25:
            errors.append(
                'Member name must be between 2 and 25 characters long.')
            break

    if len(errors) == 0:
        return True, []
    else:
        return False, errors

class RegistrationForm(Form):
    teamName = StringField('Team Name', [validators.DataRequired(
        "Team name is required"), validators.Length(min=3, max=20, message="Team name must be 3-20 characters")])
    githubLink = StringField('GitHub Repo Link', [validators.Optional(), githubLinkValidation])
    videoLink = StringField('Demo Video link', [validators.DataRequired('Video link is required'),videoLinkValidation])
    email = EmailField('Contact Email', [validators.DataRequired(
        "Email is required"), validators.Email('Invalid email address.')])