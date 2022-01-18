from wtforms import ValidationError, Form, StringField, validators, EmailField
import requests, re
from db_utils import isTeamNameAvailable

def validateLink(url, errMsg):
    """
    Validate url, raise errMsg if url doesn't exist
    It works by sending GET request to server. If the response is 404, meaning
    the url doesn't exist
    """
    try:
        r = requests.get(url)
        if r.status_code == 404:
            raise ValidationError(errMsg)

    except Exception as err:
        raise ValidationError(err)


def videoLinkValidation(form, field):
    """
    Custom validation for WTForm to validate video link. 
    """
    url = "http://img.youtube.com/vi/" + field.data + "/mqdefault.jpg"
    validateLink(url, "Invalid video id")


def githubLinkValidation(form, field):
    """
    Custom validation for WTForm to validate github link
    """
    url = "https://github.com/" + field.data
    validateLink(url, "Invalid github link")

def teamNameValidation(form, field):
    """
    Check whether team name exists in database
    """
    
    teamName = field.data.trim()
    if len(teamName) == 0:
        raise ValidationError("Team name cannot be blank!")
    havSpecialChar = re.search("[^a-zA-Z0-9_-]",teamName)
    if havSpecialChar:
        raise ValidationError("Team name can only consists of  A-Z, a-z, 0-9,_ and -!")
    availability = isTeamNameAvailable(teamName)
    if not availability:
        raise ValidationError("Team name is already taken!")


def validation(teamMembers, description, projectName, PROJECTS_NAMES):
    """
    Validate teamMembers, description, projectName.
    PROJECTS_NAMES is 1D array with all projects names in database. It's used to validate
    the <Select> tag in the form by making sure the projectName is in PROJECTS_NAMES
    """
    # to store all the errors
    errors = []
    description = description.strip()
    desLength = len(description)

    # validate description length (20-500 characters)
    if desLength < 20 or desLength > 500:
        errors.append(
            'Description must be between 20 and 500 characters long.')

    # validate project name
    if projectName not in PROJECTS_NAMES:
        errors.append('Project is not a valid choice')

    # validate teamMembers name (2-25 characters)
    for name in teamMembers:
        if len(name) < 2 or len(name) > 25:
            errors.append(
                'Member name must be between 2 and 25 characters long.')
            break
    
    # no error occurs
    if len(errors) == 0:
        return True, []
    # error occurs
    else:
        return False, errors


class RegistrationForm(Form):
    """
    Class inherited from Form class in WTForm
    For form validation
    """
    teamName = StringField('Team Name', [validators.DataRequired(
        "Team name is required"), validators.Length(min=3, max=20, message="Team name must be 3-20 characters"), teamNameValidation])
    githubLink = StringField('GitHub Repo Link', [
                             validators.Optional(), githubLinkValidation])
    videoLink = StringField('Demo Video link', [validators.DataRequired(
        'Video link is required'), videoLinkValidation])
    email = EmailField('Contact Email', [validators.DataRequired(
        "Email is required"), validators.Email('Invalid email address.')])
