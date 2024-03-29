import pandas as pd
import numpy as np
import scipy
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

def round2_cluster(appended, num_clusters):
    # print(num_clusters)
    df = appended
    # print(appended.keys())
    df['Problem Solving'] = df['Rank each skill on the list first to last. [Problem Solving]'].astype(str).str[0]
    df['Creativity'] = df['Rank each skill on the list first to last. [Creativity]'].astype(str).str[0]
    df['Research'] = df['Rank each skill on the list first to last. [Research]'].astype(str).str[0]
    df['Time Management'] = df['Rank each skill on the list first to last. [Time Management]'].astype(str).str[0]
    df['Communication'] = df['Rank each skill on the list first to last. [Communication]'].astype(str).str[0]
    df['Critical Thinking'] = df['Rank each skill on the list first to last. [Critical Thinking ]'].astype(str).str[0]
    
    newdf = df[['Problem Solving', 'Creativity', 'Research', 'Time Management', 'Communication', 'Critical Thinking', 'Scores']]
    newdf['Problem Solving'].replace("n", value="0", inplace=True)
    newdf['Creativity'].replace("n", value="0", inplace=True) 
    newdf['Research'].replace("n", value="0", inplace=True) 
    newdf['Time Management'].replace("n", value="0", inplace=True) 
    newdf['Communication'].replace("n", value="0", inplace=True) 
    newdf['Critical Thinking'].replace("n", value="0", inplace=True) 

    newdf = newdf.fillna(0)
    # newdf.drop(df.tail(1).index,inplace=True)
    # print(len(newdf))
    # newdf = newdf.drop_duplicates()

    scaler = MinMaxScaler()
    # print(df)
    new_df = pd.DataFrame(scaler.fit_transform(newdf), columns=newdf.columns[:], index=newdf.index)

    # print(new_df)

    clustering = AgglomerativeClustering(num_clusters)

    # Fitting
    clustering.fit(new_df)

    # Getting cluster assignments
    cluster_assignments = clustering.labels_


    # print(len(cluster_assignments))
    # print(len(df.index))
    # Unscaling the categories then replacing the scaled values
    df = df[['Name']].join(pd.DataFrame(scaler.inverse_transform(newdf), columns=newdf.columns[:]))
    # df = df['Name']
    # Assigning the clusters to each profile
    # print(len(cluster_assignments), "\n\n")
    # print(df)
    df['Cluster #'] = cluster_assignments
    return df

def match_skills(clustered, filtered):
    employer = clustered.iloc[[-1]]
    filtered_students = clustered[0:-1]
    best_student = ""
    best_arr = []
    most_similar = -1
    scores = []
    names = []
    for index, student in filtered_students.iterrows():
        
        arr = employer.values.tolist()
        # print('employer: ', arr)
        student_arr = student.values.tolist()
        # print('student: ', student_arr)
        employer_values = np.array(arr[0][2:-1])
        # print('employer values: ', employer_values)
        student_values = np.array(student_arr[2:-1])
        # print('student_values: ', student_values)
        cosine = cosine_similarity(employer_values.reshape(1, -1), student_values.reshape(1, -1))[0][0]
        euclidean = scipy.spatial.distance.euclidean(employer_values, student_values)
        name = student_arr[0]
        # print(name)
        if cosine > 0.5:
            scores.append(cosine)
            names.append(name)
    for i in range(len(names)):
        if isinstance(names[i], float):
            names[i] = 'Error'
    # print(names)
    # print(scores)
    matchings = sorted(zip(scores, names), reverse=True)
    df = pd.DataFrame(columns=["Name", "Skill Scores", "Filter Scores", "Social Causes"])
    for i in range(len(matchings)):
        person = matchings[i]
        score, name = person[0], person[1]
        round1_scores = filtered[filtered['Name'] == name]['Scores'].values
        # print(type(filtered[filtered['Name'] == name]['Scores'].values[0]))
        social_causes = filtered[filtered['Name'] == name]['What social causes matter to  you? Employers and students identify causes that matter to them.(Choose up to 3).  Check out our Get Involved page on Intern Pursuit for more information: https://www.internpursuit.tech/get-involved']
        df.loc[len(df)] = [name, score, round1_scores, social_causes]

    return df