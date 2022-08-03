import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity
from termcolor import colored


def round1_match(students, employer):
    filtered = students
    drop = set()
    if type(employer['Majors/Minors'].values[0]) is not list:
        employer_majors = employer['Majors/Minors'].values[0].split(', ')
        employer_citizenship = employer['Citizenship'].values[0].split(', ')
        employer_hours = employer['Full Time or Part Time (Choose weekly hours)'].values[0].split(', ')
        employer_flex = employer['Flex Schedule (check all that apply)'].values[0].split(', ')
        employer_paid = employer['What type of internships are you offering unpaid or paid?'].values[0].split(', ')
        employer_cred = employer['Credit or Non-Credit '].values[0].split(', ')
        employer_cal = employer['Which semester are you seeking interns working with you'].values[0].split(', ')
        employer_cal = [x.lower() for x in employer_cal]
    else:
        employer_majors = employer['Majors/Minors'].values[0]
        employer_citizenship = employer['Citizenship'].values[0]
        employer_hours = employer['Full Time or Part Time (Choose weekly hours)'].values[0]
        employer_flex = employer['Flex Schedule (check all that apply)'].values[0]
        employer_paid = employer['What type of internships are you offering unpaid or paid?'].values[0]
        employer_cred = employer['Credit or Non-Credit '].values[0]
        employer_cal = employer['Which semester are you seeking interns working with you'].values[0]
        employer_cal = [x.lower() for x in employer_cal]
    # details = [student_majors, student_citizenship, paid, student_hours, student_flex, cred_score, student_cal]

    employer_details = [1, 1, 1, 1, 1, 1, 1]
    scores = []
    for index in range(len(filtered.index)):
        # print(index)
        row = filtered.iloc[[index]]

        """
        Majors/Minors matching
        """
        major_score = 0
        # print(row.keys())
        majors = row['Major'].values[0]
        minors = row['Minor'].values[0]
        # print(row['Name'].values[0], " : ", majors)
        # if row['Name'].values[0] == 'dorsi.jesse@gmail.com':
            # print(type(majors))
        if not isinstance(majors, str):
            # print(row["Name"].values[0])
            # print(colored("nan", "red"))
            drop.add(index)
        else:
            # print(employer_majors)
        # print(minors)
            student_majors = majors.split(", ")
            inside = False
            for i in student_majors:
                # print("i: ", i, " , ", i in employer_majors)
                if i in employer_majors:
                    student_majors = 5
                    inside = True
                    # print(colored("match", "green"))
                    break
            if not inside:
                drop.add(index)
                # print(colored("no match", "red"))
                student_majors = 0

        """
        Citizenship matching
        """
        student_citizenship = row['Citizenship'].values[0]
        # print(employer_citizenship)
        # print(student_citizenship)
        if str(student_citizenship)[0:3] == "Int":
            student_citizenship = "International Student"
        if student_citizenship in employer_citizenship:
            student_citizenship = 4
        else:
            student_citizenship = 0

        """
        Unpaid vs Paid matching
        """
        s = "Unpaid or Paid intern options. Select which options you are open to interning.  Approximately 70% of the internships are unpaid. Please be open to options."
        student_paid = str(row[s].values[0]).split(', ')
        # print(student_paid)

        if student_paid[0] == "Both":
            student_paid = ["Unpaid", "Paid"]
        for i in str(student_paid):
            if i in str(employer_paid):
                paid = 4
                inside = True

        if not inside:
            paid = 0

        """
        Working hours matching
        """
        student_hours = str(row['Full Time or Part Time Student'].values[0])
        # print(employer_hours)
        if student_hours == "Part Time Student (3-11 hours)":
            student_hours = "Part time (3-11 hours)"
        if student_hours == "Full Time Student (12+ hours)":
            student_hours = "Full time (12 + hours)"
        # student_hours = 0
        # print(student_hours)

        if student_hours in employer_hours:
            student_hours = 4
        else:
            student_hours = 0

        """
        Flexibility matching
        """
        student_flex = str(row['Remote, Onsite, Flex Options - Check your preferences'].values[0]).split(',')
        # print(employer_flex)
        # print(student_flex)
        inside = False
        for i in student_flex:
            if i in employer_flex:
                student_flex = 3
                inside = True
                break
        if not inside:
            student_flex = 0
        
        """
        Academic credit matching -- Filter not working (Values imported from Mongo are null)
        """
        # s = 'Credit or Noncredit Internship (Requires a full semester commitment)'
        # if str(row[s].values[0]) == 'nan':
        #     row[s].values[0] = 'Non-Credit - Think of this like a volunteer role'
        # cred_score = 0
        # student_cred = row['Credit or Noncredit Internship (Requires a full semester commitment)'].values[0].split(';')
        # # print(employer_cred)
        # # print(student_cred)
        # if str(student_cred)[0] in str(employer_cred):
        cred_score = 2


        """
        Academic calendar matching -- Disabled for now 
        """
        # student_cal = str(row['Which semester are you seeking an internship?'].values[0]).split(',')
        # student_set = set(student_cal)
        # print(employer_cal)
        # print(student_cal)
        # if 'Flexible' in student_cal:
        #     student_cal = 1
        # else:
        #     inside = False
        #     for i in student_cal:
        #         if i in employer_cal:
        #             student_cal = 1
        #             inside = True
        #             break
        #     if not inside:
        student_cal = 0
        # if not student_set.isdisjoint(set(employer_cal)):
        #     student_cal = 1
        # else:
        #     student_cal = 0


        details = [student_majors, student_citizenship, paid, student_hours, student_flex, cred_score, student_cal]
        details = np.array(details)
        employer_details = np.array(employer_details)
        # print("employer details: ", employer_details)
        # if row['Name'].values[0] == 'sngraciak7@gmail.com':
        #     print("student details: ", details)
        score = np.dot(employer_details, details)
        # print(score)
        scores.append(score)
        if score == 0:
            drop.add(index)
    # print(scores)
    m = pd.Series(scores)
    filtered.insert(len(filtered.columns), "Scores", m)
    # print(filtered['Scores'])
    # filtered = filtered[filtered['Scores'] != np.nan]
    # filtered.reset_index(inplace=True)
    filtered = filtered.drop(list(drop))
    filtered.reset_index(inplace=True)

    return filtered