class YearProject(object):
    def __init__(self, year, projectName, description):
        self.year = year
        self.projectName = projectName
        self.description = description
    
    @staticmethod
    def from_dict(source):
        yearProject = YearProject(source[u'year'], source[u'projectName'], source[u'description'])
        return yearProject
    
    def to_dict(self):
        dict = {
            u'year': self.year,
            u'projectName': self.projectName,
            u'description': self.description,
        }
        return dict