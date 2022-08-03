import pandas as pd
from sklearn.utils import validation
from termcolor import colored
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
import random

def optimize_skills(appended):
    df = appended
    df['Problem Solving'] = df['Rank each skill on the list first to last. [Problem Solving]'].astype(str).str[0]
    df['Creativity'] = df['Rank each skill on the list first to last. [Creativity]'].astype(str).str[0]
    df['Research'] = df['Rank each skill on the list first to last. [Research]'].astype(str).str[0]
    df['Time Management'] = df['Rank each skill on the list first to last. [Time Management]'].astype(str).str[0]
    df['Communication'] = df['Rank each skill on the list first to last. [Communication]'].astype(str).str[0]
    df['Critical Thinking'] = df['Rank each skill on the list first to last. [Critical Thinking ]'].astype(str).str[0]

    newdf = df[['Problem Solving', 'Creativity', 'Research', 'Time Management', 'Communication', 'Critical Thinking']]
    newdf['Problem Solving'].replace("n", value="0", inplace=True)
    newdf['Creativity'].replace("n", value="0", inplace=True) 
    newdf['Research'].replace("n", value="0", inplace=True) 
    newdf['Time Management'].replace("n", value="0", inplace=True) 
    newdf['Communication'].replace("n", value="0", inplace=True) 
    newdf['Critical Thinking'].replace("n", value="0", inplace=True) 

    scaler = MinMaxScaler()
    new_df = pd.DataFrame(scaler.fit_transform(newdf), columns=newdf.columns[:], index=newdf.index)

    # Setting the amount of clusters to test out
    cluster_cnt = [i for i in range(2, 12, 1)]

    # Establishing empty lists to store the scores for the evaluation metrics
    s_scores = []

    db_scores = []

    # Looping through different iterations for the number of clusters
    for i in cluster_cnt:
        
        # Hierarchical Agglomerative Clustering with different number of clusters
        hac = AgglomerativeClustering(n_clusters=i)
        
        hac.fit(new_df)
        
        cluster_assignments = hac.labels_
        
        ## KMeans Clustering with different number of clusters
        k_means = KMeans(n_clusters=i)
        
        k_means.fit(new_df)
        
        cluster_assignments = k_means.predict(new_df)
        # Appending the scores to the empty lists    
        s_scores.append(silhouette_score(new_df, cluster_assignments))
        
        db_scores.append(davies_bouldin_score(new_df, cluster_assignments))
    return s_scores, db_scores

def plot_evaluation(scores):
    df = pd.DataFrame(columns=['Cluster Score'], index=[i for i in range(2, len(scores)+2)])
    df['Cluster Score'] = scores
    
    # Plotting out the scores based on cluster count
    # plt.figure(figsize=(16,6))
    # plt.style.use('ggplot')
    # plt.plot(x,y)
    # plt.xlabel('# of Clusters')
    # plt.ylabel('Score')
    # plt.show()
    return df['Cluster Score']==df['Cluster Score'].max()

def find_num_clusters(scores):
    for i in range(2, len(scores)):
        if scores[i]:
            scores = i
            return i

def pretty_print(dataframe, curr, employer_name, count):
    names = dataframe['Name'].values.tolist()
    scores = dataframe['Final Score'].values.tolist()
    majors = dataframe['Major'].values.tolist()
    if count == 0:
        count = len(names)
    top_students = sorted(zip(scores, names, majors), reverse=True)
    size = 0
    for i in range(len(top_students)):
        if top_students[i][0] > 0.5:
            size += 1
    text = "Third round completed"
    print(colored(text, "magenta"))
    print(colored(("The top students for " + curr['Name'].values[0]  + " with employee " + employer_name + " after filtering, skills matching, and social cause matching are:"), "blue"))
    validation_list = ["test@gmail.com", "ichita@gmail.com", "vishal@gmail.com", "vuk@gmail.com", "rohan@gmail.com", "bharath@gmail.com"]
    for i in range(len(top_students)):
        if i < count:
            if i > 5:
                score = top_students[i][0] - 0.05
            else:
                score = top_students[i][0]
            email = str(top_students[i][1])
            if email in validation_list:
                print(colored((str(i+1)+". " + str(top_students[i][1]) + " with a " + str(round(score * 100, 1)) + "% similarity match as a " + top_students[i][2] + " intern."), "blue", "on_white", ['blink'])) 
                validation_list.remove(email)
            else:
                print(colored((str(i+1)+". " + str(top_students[i][1]) + " with a " + str(round(score * 100, 1)) + "% similarity match as a " + top_students[i][2] + " intern."), "green")) 
    print()
    for i in validation_list:
        print(colored((i + " was not listed in top candidates."), "red"))
    return top_students