from flask import Flask, jsonify
from matching import match
from flask_cors import CORS
from flask import request
from termcolor import colored
import pandas as pd

#_id
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])

@app.route('/', methods=['POST'])
def matching():
    print(colored("Running E4C Matching algorithm", "magenta"))
    print(colored("––––––––––––––––––––––––––––––", "magenta"))
    students =  pd.DataFrame(request.json[0])
    problem_solving = []
    creativity = []
    research = []
    time = []
    communication = []
    thinking = []
    students['rankings'] = students['rankings'].fillna(0)
    for index in range(len(students['rankings'].index)):
        row = students['rankings'][index]
        if row is 0:
            row = {'Problem Solving': 0, 'Creativity': 0, 'Research': 0, 'Time Management': 0, 'Communication': 0, 'Critical Thinking': 0 }
        problem_solving.append(row['Problem Solving'])
        creativity.append(row['Creativity'])
        research.append(row['Research'])
        time.append(row['Time Management'])
        communication.append(row['Communication'])
        thinking.append(row['Critical Thinking'])
    students['Rank each skill on the list first to last. [Problem Solving]'] = problem_solving
    students['Rank each skill on the list first to last. [Creativity]'] = creativity
    students['Rank each skill on the list first to last. [Research]'] = research
    students['Rank each skill on the list first to last. [Time Management]'] = time
    students['Rank each skill on the list first to last. [Communication]'] = communication
    students['Rank each skill on the list first to last. [Critical Thinking ]'] = thinking
    employers = pd.DataFrame(request.json[1])
    employers = employers.rename(columns={'companyName': 'Name', 'majors':'Majors/Minors', 'socialChannel':'Social Causes', 'citizenship':'Citizenship', 'weeklyHours': 'Full Time or Part Time (Choose weekly hours)', 'schedule': 'Flex Schedule (check all that apply)', 'pay': 'What type of internships are you offering unpaid or paid?', 'credit': 'Credit or Non-Credit ', 'semester': 'Which semester are you seeking interns working with you'})
    students = students.rename(columns={'firstName':'Name', 'major':'Major', 'minor':'Minor','socialCause':'What social causes matter to  you? Employers and students identify causes that matter to them.(Choose up to 3).  Check out our Get Involved page on Intern Pursuit for more information: https://www.internpursuit.tech/get-involved', 'citizenship':'Citizenship', 'workHours':'Full Time or Part Time Student', 'schedule': 'Remote, Onsite, Flex Options - Check your preferences', 'credit':'Credit or Noncredit Internship (Requires a full semester commitment)', 'semester': 'Which semester are you seeking an internship?'})
    employer_name = "Employers 4 Change"
    test = match(students, employers, employer_name, 0, True)
    return jsonify(test)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)
