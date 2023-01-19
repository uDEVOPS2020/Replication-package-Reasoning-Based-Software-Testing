import glob
import sys
from datetime import datetime
from lib2to3.pytree import convert
import os
import pandas as pd

def count_violations(file_contents_parts):
    count = 0

    for part in file_contents_parts:
            if part.__contains__("]:"):
                part_without_date = part.split("[")[1]
                feature_values = part_without_date.split("]:")[0]
                fitness_values = part_without_date.split("]:")[1]

                fitness_values_parts = fitness_values.split(",")


                # DfC_min = float(fitness_values_parts[0])
                DfV_min = float(fitness_values_parts[1])
                # DfP_min = float(fitness_values_parts[2])
                # DfM_min = float(fitness_values_parts[3])
                # DT_max = float(fitness_values_parts[4])
                # traffic_lights_max = float(fitness_values_parts[5])

                # if DfC_min <= 0:
                #     count = count+1

                if DfV_min <= 0:
                    count = count+1

                # if DfP_min <= 0:
                #     count = count+1

                # if DfM_min <= 0:
                #     count = count+1

                # if DT_max <= 0.95:
                #     count = count+1

                # if traffic_lights_max <= 0:
                #     count = count+1

    return count

def get_time(stime):
   return stime.split(",")[0]

def handle_config(folder_names):
    
    file_writer = open('output/output-fails.csv', 'w')

    for i in range(20, 130, 20):
        for folder_n in range(len(folder_names)):
            folder = folder_names[folder_n]
            file_writer.write(folder + '-' + str(i) + ", ")
            list_of_all_files = (glob.glob('data_for_scripts'  + "/" + folder + "/*.log"))

            for file in list_of_all_files:
                count = 0

                file_reader = open(file, "r")
                file_contents_parts = []
                file_contents_ps = file_reader.read().split("\n")
                stime = file_contents_ps[0]
                if "Started" in stime:
                    stime = get_time(stime)
                    FMT = '%Y-%m-%d %H:%M:%S'
                    for content in file_contents_ps:
                        if ']:' not in content:
                            continue
                        n_time = get_time(content)
                        if n_time == stime:
                            continue
                        time_diff = datetime.strptime(n_time, FMT) - datetime.strptime(stime, FMT)
                        minutes = divmod(time_diff.total_seconds(), 60)
                        if minutes[0] < i:
                            file_contents_parts.append(content)
                        else:
                            break
                else:
                    print("W not started in file")

                count = count + (count_violations(file_contents_parts))
                file_writer.write(str(count)+",")

            file_writer.write('\n')

def convert():

    if os.path.exists("./output/data-fails.csv"):
            os.remove("./output/data-fails.csv")

    df = pd.read_csv("./output/output-fails.csv", header=None)
    df = df.iloc[: , :-1]

    df = df.transpose()

    new_header = df.iloc[0] 
    df = df[1:] #
    df.columns = new_header 

    df = df.mean(axis = 0)

    df = pd.DataFrame(df)
    df = df.transpose()


    df1 = df.filter(regex='RBST')
    df2 = df.filter(regex='SBST-ML')
    df3 = df.filter(regex='ART')

    original_stdout = sys.stdout

    with open("output/data-fails.csv", 'a') as res:
        sys.stdout = res


        if not df1.empty:
            print('RBST,0.0' + str(df1.iloc[0].tolist()).replace('[',',').replace(']','') + ',')
        if not df2.empty:
            print('SBST-ML,0.0' + str(df2.iloc[0].tolist()).replace('[',',').replace(']','') + ',')
        if not df3.empty:
            print('ART,0.0' + str(df3.iloc[0].tolist()).replace('[',',').replace(']','') + ',')

        sys.stdout = original_stdout 


if __name__ == "__main__":

    folder_names = ["RBST","SBST-ML","ART"]

    handle_config(folder_names)
    convert()


