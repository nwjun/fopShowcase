from wtforms import validators


class Team(object):
    def __init__(self, year, teamName, project, teamMembers, githubLink, videoLink, description):
        self.year=year
        self.teamName = teamName
        self.project = project
        self.teamMembers = teamMembers
        self.videoLink = "https://youtu.be/"+videoLink
        self.description = description
        
        if (githubLink == ''):
            self.githubLink = ""
        else:
            self.githubLink = "https://github.com/"+githubLink
    
    def getJoinedMembers(self):
        return ','.join(self.teamMembers)