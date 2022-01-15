from firebase_admin import firestore
from flask import Flask, session, redirect, flash
from flask.helpers import flash
from flask import render_template, url_for, request
from validators import validation, RegistrationForm

import firebase_admin
from flask_recaptcha import ReCaptcha  # Import ReCaptcha object

from Team import Team
from db_utils import pushToDb, getCollectionByProject, getTeamDetails, createData, isTeamNameAvailable

app = Flask(__name__)
# session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# recaptcha
# <-- Add your site key
app.config['RECAPTCHA_SITE_KEY'] = '6Ld2IAMeAAAAAIgPizQgCFgYP0K3qJAzmwwJmb3k'
# <-- Add your secret key
app.config['RECAPTCHA_SECRET_KEY'] = '6Ld2IAMeAAAAAFDwCH4t-MjL9XhImq4Q3ovWCKDl'
# Create a ReCaptcha object by passing in 'app' as parameter
recaptcha = ReCaptcha(app)

projects = [
    {
        "icon": "bi bi-film",
        "project": "Cinema Ticketing System",
        "desc": "You are required to implement the current SOP into the cinema’s online ticket booking system which allow customers to purchase tickets and place food orders.",
    },
    {
        "icon": "bi bi-controller",
        "project": "Tower Defense",
        "desc": "You are required to build a brand new Tower of Defence game that allows you - the mayor of the city – to keep your city safe and defeat the dragon.",
    },
    {
        "icon": "bi bi-book",
        "project": "Module Registration Platform",
        "desc": "You are required to build a module registration platform. The end-users consists of students and stuff where both of them have different requirements & usages",
    },
    {
        "icon": "bi bi-bag",
        "project": "Online Shopping Platform",
        "desc": "You are required to build an online shopping app that provides a platform for customers and sellers to trade",
    },
    {
        "icon": "bi bi-shop",
        "project": "Hotel Management System",
        "desc": "You are required to build a system where customers can direct booking through the system and pay before booking to avoid over booking not check-in problems.",
    },
]
PROJECTS_NAMES = [proj["project"] for proj in projects]

# Use a service account
firebase_admin.initialize_app()

@app.route("/")
def index():
    # createData()
    return render_template('index.html', projects=projects)


@app.route("/upload")
def upload():
    if 'formDetails' in session:
        team = session.pop('formDetails')
    else:
        team = {
            'teamName': "",
            'projectName': ["",],
            'teamMembers' : "",
            'githubLink': "",
            'videoLink': "",
            'description': "",
            'email': "",
        }
    return render_template('upload.html', projects=projects, team=team)


@app.route('/projects/<projectName>')
def projectPage(projectName):
    teams = getCollectionByProject(projectName)
    print(projectName)
    print(teams)
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

    validate, errors = validation(teamMembers, description, projectName, PROJECTS_NAMES)

    if request.method == 'POST':
        github = form.githubLink.data

        if not github:
            github = ''

        team = Team('21-22', form.teamName.data, projectName, teamMembers,
                    github, form.videoLink.data, description, form.email.data)

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

    return render_template('upload.html', projects=projects)


@app.route("/projects/<projectName>/<teamName>")
def showProjectDetails(projectName, teamName):
    details, currentIdx = getTeamDetails(projectName, teamName)
    if not details:
        print("Team is not is database!")

    return render_template('projectDetails.html', team=details['teams'][currentIdx], pagination=details)

@app.route("/checkTeamName")
def checkTeamName():
    teamName =request.args.get('teamName')
    availability = isTeamNameAvailable(teamName)
    if availability:
        return {"result": True}
    else:
        return {"result": False}

if __name__ == "__main__":
    app.run(debug=True)
