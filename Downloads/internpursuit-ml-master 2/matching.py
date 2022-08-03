import pandas as pd
from termcolor import colored
import warnings

warnings.filterwarnings("ignore")

from round1 import round1_filter
from round1match import round1_match
from round2 import round2_cluster, match_skills
from round3 import cleanup, match_socials
from utils import pretty_print, optimize_skills, plot_evaluation, find_num_clusters

def match(students, employers, employer_name, count, api=False):
    # print(employers.columns.values.tolist())
    # print(students.columns.values.tolist())
    employers = employers.rename(columns={'Employee First Name (person that will work with student)': 'First Name', 'Employee Last Name (person that will work with student)': 'Last Name', 'Company Name': 'Name', 'Majors and Minors (check all that apply)':'Majors/Minors', 'Identify only 3':'Social Causes', 'Citizenship (check all that apply)':'Citizenship'})
    students = students.rename(columns={'Email Address':'Name', 'Your Major ':'Major', 'Your Minor (if applicable)':'Minor','Social Causes':'Social Causes', 'internPay': 'Unpaid or Paid intern options. Select which options you are open to interning.  Approximately 70% of the internships are unpaid. Please be open to options.'})
    for i in range(len(employers.index)):

        # obtain i-th employer from dataframe
        curr = employers.iloc[[i]]
        if api == True:
            if curr['First Name'].values.tolist()[0] + " " + curr['Last Name'].values.tolist()[0] == employer_name:
                # perform filtering on all students based on criteria of i-th employer
                filtered = round1_match(students, curr)
                # for i in filtered['Username'].values.tolist():
                #     print(i)
                # print(filtered['Username'].values.tolist())
                text = "First round complete"
                print(colored(text, "magenta"))
                # filtered = students
                # create dataframe with filtered students and i-th employer
                appended = filtered.append(curr)
                # find optimal number of clusters for appended dataframe
                s_score, db_score = optimize_skills(appended)
                s_clusters = find_num_clusters(plot_evaluation(s_score))
                db_clusters = find_num_clusters(plot_evaluation(db_score))

                # perform clustering on appended using both of the optimized cluster scores, use appended dataframe because we need apply a bonus weight if student and employer's clusters match
                # print("num clusters: ", s_score)
                s_clustered = round2_cluster(appended, 2)
                db_clustered = round2_cluster(appended, db_clusters)

                # get list of top 10-12 candidates as a list of tuples (x, y) where x is the candidate's email address and y is their similarity score
                
                s_optimal_matchings = match_skills(s_clustered, filtered)
                db_optimal_matchings = match_skills(db_clustered, filtered)
                # for i in s_optimal_matchings:
                #     print(i)
                text = "Second round complete"
                print(colored(text, "magenta"))

                # cleanup all dataframes and get new dataframe which includes candidate's email, similarity score, and social causes columns
                # s_cleaned_up = cleanup(filtered, s_clustered, s_optimal_matchings)
                # db_cleaned_up = cleanup(filtered, db_clustered, db_optimal_matchings)

                # return list of top 3-5 candidates based on social clustering
                s_final = match_socials(s_optimal_matchings, curr, students)
                db_final = match_socials(db_optimal_matchings, curr, students)
                # for i in s_final['Name'].values.tolist():
                #     print(i)
                # pretty print top candidates for current employer
                # print("silhoutte score matching: ")
                output = pretty_print(s_final, curr, employer_name, count)

                # print("================================================================")

                # print("db score matching: ")
                # output = pretty_print(db_final, curr, count)

                # pretty_print(db_final)
                return
        else:
            filtered = round1_filter(students, curr)
            text = "Students remaining after first round: " + str(len(filtered))
            print(colored(text, "magenta"))
            # filtered = students
            # create dataframe with filtered students and i-th employer
            appended = filtered.append(curr)

            # find optimal number of clusters for appended dataframe
            s_score, db_score = optimize_skills(appended)

            s_clusters = find_num_clusters(plot_evaluation(s_score))
            db_clusters = find_num_clusters(plot_evaluation(db_score))

            # perform clustering on appended using both of the optimized cluster scores, use appended dataframe because we need apply a bonus weight if student and employer's clusters match
            s_clustered = round2_cluster(appended, s_clusters)
            db_clustered = round2_cluster(appended, db_clusters)

            # get list of top 10-12 candidates as a list of tuples (x, y) where x is the candidate's email address and y is their similarity score
            s_optimal_matchings = match_skills(s_clustered)
            db_optimal_matchings = match_skills(db_clustered)
            text = "Students remaining after second round: " + str(len(s_optimal_matchings))
            print(colored(text, "magenta"))

            # cleanup all dataframes and get new dataframe which includes candidate's email, similarity score, and social causes columns
            s_cleaned_up = cleanup(filtered, s_clustered, s_optimal_matchings)
            db_cleaned_up = cleanup(filtered, db_clustered, db_optimal_matchings)

            # return list of top 3-5 candidates based on social clustering
            s_final = match_socials(s_cleaned_up, curr, students)
            db_final = match_socials(db_cleaned_up, curr, students)
            
            # pretty print top candidates for current employer
            output = pretty_print(s_final, curr, employer_name)
            return
    return

if __name__ == "__main__":
    # student_file = input("Enter hte name of the student csv file (with path): ")
    # employer_file = input("Enter the name of the employer csv file (with path): ")
    # employer_name = input("Enter name of the company: ")
    employer_name = "Joseph Nastasi"
    match(pd.read_csv('updated_students.csv'), pd.read_csv('updated_employers.csv'), employer_name, 0, True)