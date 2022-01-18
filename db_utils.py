from http import client
from flask import session
from Team import Team
from firebase_admin import firestore
from yearProject import YearProject


def createData():
    """
    Function to create and push dummy data to database
    """
    teamsName = ['test1', 'test2', 'test3', 'test4', 'test5']
    projectName = 'Cinema Ticketing System'
    teamMembers = ["abcd", "efgh"]
    github = ""
    videoLink = "SBsDkwbL-G4"
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vitae purus maximus, egestas lorem in, ultrices nibh. Sed nec leo luctus, rutrum nulla et, pellentesque augue. Morbi convallis massa eget nisi commodo porta nec id felis. Proin posuere vel risus nec sollicitudin. Vestibulum elementum lacinia purus. Mauris accumsan molestie fringilla. Aenean pellentesque luctus porttitor. Donec varius leo sit amet ipsum c"

    for i in range(5):
        team = Team('21-22', teamsName[i], projectName,
                    teamMembers, github, videoLink, description)
        pushToDb(team)


def pushToDb(team):
    """
    Function to push team to database
    team: instance of Team class
    """
    assert isinstance(
        team, Team), "object should be instance of Team class"
    db = firestore.client()
    doc_ref = db.collection(team.year).document()
    res = doc_ref.set(team.to_dict())
    if res:
        return True
    else:
        return False


def getCollectionByProject(projectName):
    """
    Function to retrieve data that has the same project name
    Return all the teams with the same project name
    """
    if projectName not in session:
        db = firestore.client()
        docs = db.collection(
            u'21-22').where(u'projectName', u'==', projectName).stream()

        # docs is generator, which has no length
        # must be converted to dict first to count length
        queryTeams = [doc.to_dict() for doc in docs]

        if len(queryTeams) != 0:
            teams = {
                "teams": queryTeams,
                "maxIdx": len(queryTeams)-1,
            }
            return teams
        else:
            return None


def getTeamDetails(projectName, teamName):
    """
    Function to retrieve data that has the same team name
    Return a dict "details"
    details={
        'maxIdx': max index for all teams of projectName
        'teams': all teams of projectName
        'currentIdx': index of teamName in all teams
    }
    """
    db = getCollectionByProject(projectName)

    teams = db['teams']

    details = {
        'maxIdx': db['maxIdx'],
        'teams': teams,
        'currentIdx': -1,
    }

    for idx, team in enumerate(teams):
        if team['teamName'] == teamName:
            details['currentIdx'] = idx

    if details['currentIdx'] != -1:
        return details, details['currentIdx']

    return None, None


def isTeamNameAvailable(teamName):
    """
    Function to check whether team name exists
    Return true if team name is available, else false
    """
    db = firestore.client()

    docs = db.collection(u'21-22').where(u'teamName', u'==', teamName).stream()
    # cant use len(docs) to determine whether has record as generator has no len()
    query = [doc.to_dict() for doc in docs]

    if len(query) == 0:
        return True
    else:
        return False


def addYearProjects(yearProject):
    """
    Push yearProject to database
    yearProject: instance of YearProject
    """
    assert isinstance(
        yearProject, YearProject), "object should be instance of YearProject"
    db = firestore.client()
    doc_ref = db.collection('yearProject').document()
    res = doc_ref.set(yearProject.to_dict())
    if res:
        return True
    else:
        return False


def getYearProjects(year):
    """
    Retrieve all yearProject that has the same year as "year"
    Return 1D array of yearProject
    """
    db = firestore.client()
    docs = db.collection(
        u'yearProject').where(u'year', u'==', year).stream()

    queryTeams = [doc.to_dict() for doc in docs]

    if len(queryTeams) != 0:
        return queryTeams
    else:
        return None
