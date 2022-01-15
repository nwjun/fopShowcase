from firebase_admin import firestore
from flask import session

class Team(object):
    def __init__(self, year, teamName, projectName, teamMembers, githubLink, videoLink, description, email):
        self.year=year
        self.teamName = teamName
        self.projectName = projectName
        self.teamMembers = teamMembers
        self.videoLink = videoLink
        self.description = description
        self.email = email

        if (githubLink == ''):
            self.githubLink = ""
        else:
            self.githubLink = "https://github.com/"+githubLink
    
    def getJoinedMembers(self):
        return '$$'.join(self.teamMembers)
    
    @staticmethod
    def from_dict(source):
        # [START_EXCLUDE]
        team = Team("21-22", source[u'teamName'], source[u'projectName'], source[u'teamMembers'],
        source[u'githubLink'], source[u'videoLink'],source[u'description'], source[u'email'])
        return team
        # [END_EXCLUDE]

    def to_dict(self):
        dict = {
            u"year": self.year,
            u"teamName": self.teamName,
            u"projectName": self.projectName,
            u'teamMembers': self.teamMembers,
            u"videoLink": self.videoLink,
            u"description": self.description,
            u"githubLink": self.githubLink,
            u"email": self.email,
        }

        return dict