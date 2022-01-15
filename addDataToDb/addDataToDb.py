from yearProject import YearProject
import csv,firebase_admin
from flask import Flask
from db_utils import addYearProjects

app = Flask(__name__)

firebase_admin.initialize_app()

@app.route("/")
def index():
    filepath = '/home/jun/fopShowcase/projects21_22.csv'
    isHeaderExist = False
    # filepath = input("File path: ")

    # while True:
    #     isHeaderExist = input('Is header exist? (y/n): ')
    #     if str.lower(isHeaderExist) in ['y', 'yes']:
    #         isHeaderExist = True
    #         break
    #     elif str.lower(isHeaderExist) in ['n', 'no']:
    #         isHeaderExist = False
    #         break
    #     else:
    #         print('Only accept (y/yes/n/n). Please retype.')

    # url = input("Url to server: ")

    file = open(filepath, newline='')
    csvreader = csv.reader(file,delimiter=',')

    if isHeaderExist:
        header = next(csvreader)
        print(len(header))
    
    for row in csvreader:
        yearProject = YearProject(row[0], row[1], row[2])
        addYearProjects(yearProject)
        print("added project 1")

    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)