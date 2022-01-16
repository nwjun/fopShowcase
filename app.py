from flask import Flask, session, redirect, flash
from flask_cors import CORS
from flask.helpers import flash
from flask import render_template, url_for, request
from validators import validation, RegistrationForm
from dotenv import load_dotenv
from os import environ
from validators import validateLink
import json

import firebase_admin
from flask_recaptcha import ReCaptcha  # Import ReCaptcha object

from Team import Team
from db_utils import pushToDb, getCollectionByProject, getTeamDetails, isTeamNameAvailable, getYearProjects

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

load_dotenv()

app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['RECAPTCHA_SITE_KEY'] = environ.get('RECAPTCHA_SITE_KEY')
app.config['RECAPTCHA_SECRET_KEY'] = environ.get('RECAPTCHA_SECRET_KEY')
# app.config.from_file("config.json", load=json.load)

ggl_data = {
    "type": environ.get('FIREBASE_SERVICE_TYPE'),
    "project_id": environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": environ.get('FIREBASE_AUTH_URI'),
    "token_uri": environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": environ.get('FIREBASE_CLIENT_X509_CER_URL')
}

credentials = firebase_admin.credentials.Certificate(ggl_data)


# Create a ReCaptcha object by passing in 'app' as parameter
recaptcha = ReCaptcha(app)

years = ['21-22']

# Use a service account
firebase_admin.initialize_app(credential=credentials)


@app.context_processor
def injectYearsProjects():
    if 'allYearsProjectsNames' not in session or 'allYearsProjectsDetails' not in session:
        allYearsProjectsNames = []
        allYearsProjectsDetails = []
        for year in years:
            oneYearProject = getYearProjects(year)
            projectsNames = [proj["projectName"] for proj in oneYearProject]
            allYearsProjectsNames.append([year, projectsNames])
            allYearsProjectsDetails.append([year, oneYearProject])
        session['allYearsProjectsNames'] = allYearsProjectsNames
        session['allYearsProjectsDetails'] = allYearsProjectsDetails
    return dict(allYearsProjectsNames=session['allYearsProjectsNames'])


def getAllYearsProjectsDetails():
    if "allYearsProjectsDetails" not in session:
        allYearsProjectsDetails = []
        for year in years:
            oneYearProject = getYearProjects(year)
            allYearsProjectsDetails.append([year, oneYearProject])
        session['allYearsProjectsDetails'] = allYearsProjectsDetails
    return session['allYearsProjectsDetails']


@app.route("/")
def index():
    allYearsProjectsDetails = getAllYearsProjectsDetails()
    return render_template('index.html', allYearsProjectsDetails=allYearsProjectsDetails)


@app.route("/upload")
def upload():
    if 'formDetails' in session:
        team = session.pop('formDetails')
    else:
        team = {
            'teamName': "",
            'projectName': ["", ],
            'teamMembers': "",
            'githubLink': "",
            'videoLink': "",
            'description': "",
            'email': "",
        }
    return render_template('upload.html', team=team)


@app.route('/projects/<projectName>')
def projectPage(projectName):
    db = getCollectionByProject(projectName)
    teams = None
    if db:
        teams = db["teams"]

    return render_template('project.html', projectName=projectName, year="21-22", teams=teams)


@app.route("/submitForm", methods=['POST'])
def formSubmission():
    form = RegistrationForm(request.form)
    teamMembers = []

    try:
        for i in range(6):
            temp = request.form['teamMembers['+str(i)+']']
            teamMembers.append(temp)
    except:
        print("end")

    description = request.form['projectDescription']
    projectName = request.form['selectProject']

    validate, errors = validation(
        teamMembers, description, projectName, session['allYearsProjectsNames'][0][1])

    if request.method == 'POST':
        team = Team('21-22', form.teamName.data, projectName, teamMembers,
                    form.githubLink.data, form.videoLink.data, description, form.email.data)

        session['formDetails'] = team.to_dict()

        if recaptcha.verify():
            if form.validate() and validate:
                succeed = pushToDb(team)
                if succeed:
                    session.pop('formDetails')
                    flash('Successfully uploaded the form')
                else:
                    flash('Failed to upload the form to server!')
                return redirect(url_for('index'))
            else:
                errors = errors + [err_msg[0]
                                   for _, err_msg in form.errors.items()]
        else:
            errors = ['Please fill out the ReCaptcha!']
        flash(errors)
    return redirect(url_for('upload'))


@app.route("/projects/<projectName>/<teamName>")
def showProjectDetails(projectName, teamName):
    details, currentIdx = getTeamDetails(projectName, teamName)
    if not details:
        raise Exception("Team is not is database!")

    return render_template('projectDetails.html', team=details['teams'][currentIdx], pagination=details)


@app.route("/checkTeamName")
def checkTeamName():
    teamName = request.args.get('teamName')
    availability = isTeamNameAvailable(teamName)
    if availability:
        return {"result": True}
    else:
        return {"result": False}


@app.route("/checkLink")
def checkLink():
    url = request.args.get('u')
    try:
        validateLink(url, "Error validating link")
        return {"result": True}
    except Exception as err:
        return err


if __name__ == "__main__":
    app.run(debug=True)
