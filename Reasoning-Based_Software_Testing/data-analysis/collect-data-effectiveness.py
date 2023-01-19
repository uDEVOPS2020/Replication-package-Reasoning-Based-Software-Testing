import glob
import sys
import pandas as pd


def get_data(folder_names,file_name):
    file_writer = open(file_name, 'w')
    file_writer.write("\"technique\",\"repetition\",\"count_DCL\",\"count_DV\",\"count_DP\",\"count_DS\",\"count_DT\",\"count_TR\",\"count_TOT\",\"count_f_test\"")
    file_writer.write("\n")

    df = pd.DataFrame(columns=['technique','0','1','2','3','4','5','6'], index=range(0,len(folder_names)))

    for i in range(len(folder_names)):
        df.iloc[i] = [folder_names[i],0,0,0,0,0,0,0]

    print(df)

    for folder_n in range(len(folder_names)):
        folder = folder_names[folder_n]
        list_of_all_files = (glob.glob('data_for_scripts/' + folder + '/*.log'))

        rep = 1
        for file in list_of_all_files:
            count_DCL = 0
            count_DV = 0
            count_DP = 0
            count_DS = 0
            count_DT = 0
            count_TR = 0
            count_failed_test = 0

            inputs = ["test"]

            file_reader = open(file, "r")
            file_contents = file_reader.read()
            file_contents_parts = file_contents.split('\n')

            for part in file_contents_parts:
                fail = False
                if part.__contains__("]:"):
                    countFails = 0

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
                    
                    if feature_values not in inputs:
                        # if DfC_min <= 0:
                        #     count_DCL += 1
                        #     countFails += 1
                        #     fail = True
                    
                        if DfV_min <= 0:
                            count_DV += 1
                            countFails += 1
                            fail = True
                    
                        # if DfP_min <= 0:
                        #     count_DP += 1
                        #     countFails += 1
                        #     fail = True
                    
                        # if DfM_min <= 0:
                        #     count_DS += 1
                        #     countFails += 1
                        #     fail = True
                    
                        # if DT_max <= 0.95:
                        #     count_DT += 1
                        #     countFails += 1
                        #     fail = True
                    
                        # if traffic_lights_max <= 0:
                        #     count_TR += 1
                        #     countFails += 1
                        #     fail = True

                        if fail:
                            count_failed_test += 1
                        
                        df.at[folder_n,str(countFails)]= df.iloc[folder_n][str(countFails)] + 1
                    else:
                        print("Found duplicate test:" + file)

                    inputs.append(feature_values)

            count_tot = count_DCL + count_DV + count_DP + count_DS + count_DT + count_TR
            file_writer.write(folder + "," + str(rep) + "," + str(count_DCL) + "," + str(count_DV) + "," + str(count_DP) + "," + str(count_DS) + "," + str(count_DT) + "," + str(count_TR) + "," + str(count_tot)+ "," + str(count_failed_test))
            file_writer.write("\n")
            rep += 1
        df.to_csv("output/_fails/fails_x_test.csv", index=False)
        print("File is saved with name: "+file_name)



        
if __name__ == "__main__":

    folder_names = ["RBST","SBST-ML","ART"]

    file_name = "output/output-cfails.csv"

    get_data(folder_names,file_name)


