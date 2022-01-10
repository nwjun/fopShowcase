from flask import Flask,session, redirect, flash
from flask.helpers import flash
from flask import render_template, url_for,request
from wtforms import Form, StringField, validators

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from Team import Team

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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
        "desc":"You are required to build an online shopping app that provides a platform for customers and sellers to trade",
    },
    {
        "icon": "bi bi-shop",
        "project": "Hotel Management System",
        "desc":"You are required to build a system where customers can direct booking through the system and pay before booking to avoid over booking not check-in problems.",
    },
]
PROJECTS_NAMES = [proj["project"] for proj in projects]

# Use a service account
firebase_admin.initialize_app()
db = firestore.client()


@app.route("/")
def index():
    return render_template('index.html', projects=projects)

@app.route("/upload")
def upload():
    return render_template('upload.html',projects=projects)

class RegistrationForm(Form):
    teamName = StringField('Team Name', [validators.Length(min=3, max=10)])
    githubLink = StringField('GitHub Repo Link', [validators.Optional(), validators.Length(min=5, message="Github link must be at least 5 characters long")])
    videoLink = StringField('Demo Video link', [validators.Length(min=5, message="Demo video link must be at least 5 characters long")])

def validation(teamMembers, description, projectName):
    errors=[]
    length = len(description)

    if length <20 or length > 500:
        errors.append('Description must be between 20 and 500 characters long.')

    if projectName not in PROJECTS_NAMES:
        errors.append('Project is not a valid choice')

    for name in teamMembers:
        if len(name) < 2 or len(name)>25:
            errors.append('Member name must be between 2 and 25 characters long.')
            break
    
    if len(errors) == 0:
        return True,[]
    else:
        return False, errors


@app.route('/projects/<project>')
def projectPage(project):
    return render_template('project.html')

@app.route("/submitForm", methods=['POST'])
def formSubmission():
    form = RegistrationForm(request.form)
    teamMembers=[]

    try:
        for i in range(6):
            temp = request.form['teamMembers['+str(i)+']']
            teamMembers.append(temp)
    except:
        print("end")

    description = request.form['projectDescription']
    projectName = request.form['selectProject']

    validate, errors = validation(teamMembers, description, projectName)

    if request.method == 'POST':
        if  form.validate() and validate:
            github = form.githubLink.data

            if not github:
                github = ''

            team = Team('21-22',form.teamName.data, projectName, teamMembers, github, form.videoLink.data, description)

            doc_ref = db.collection(team.year).document(team.teamName)
            doc_ref.set({
                u'project': team.project,
                u'members': team.getJoinedMembers(),
                u'githubLink': team.githubLink,
                u'videoLink': team.videoLink,
                u'description': team.description,
            })

            flash('You were successfully uploaded the form')
            return redirect(url_for('index'))
        else:
            errors = errors + [err_msg[0] for _, err_msg in form.errors.items()]
            flash(errors)
            return redirect(url_for('upload'))

    return render_template('upload.html', projects=projects, errors=errors)

if __name__ == "__main__":
    app.run(debug=True)
