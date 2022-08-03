import pandas as pd

def cleanup(filtered, clustered, matchings):
    df = pd.DataFrame(columns=["Name", "Scores", "Social Causes"])
    for i in range(len(matchings)):
        person = matchings[i]
        score, name = person[0], person[1]
        # print(filtered.keys())
        social_causes = filtered[filtered['Name'] == name]['What social causes matter to  you? Employers and students identify causes that matter to them.(Choose up to 3).  Check out our Get Involved page on Intern Pursuit for more information: https://www.internpursuit.tech/get-involved']
        df.loc[len(df)] = [name, score, social_causes]
    return df

def match_socials(dataframe, curr, students):
    curr = curr[['Name', 'Social Causes']]
    employer_social = set(curr['Social Causes'].values[0].split(';'))
    df = pd.DataFrame(columns=["Name", "Final Score", "Major"])
    for index, row in dataframe.iterrows():
        if len(row[3].values) > 0:
            social = row[3].values[0]
            if isinstance(social, str):
                causes = social.split(';')
                overlap = len(list(employer_social.intersection(causes)))/9
            else:
                overlap = 0
            row[2] = row[2]/6
            # updated_score = (row[1] * 0.5) + (row[2] * 0.3) + (overlap * 0.2)
            updated_score = (row[1] * 0.80) + (overlap * 0.25)

            student_major = students.loc[students['Name'] == row[0]]['Major'].values[0]
            df.loc[len(df)] = [row[0], updated_score, student_major]

    return df