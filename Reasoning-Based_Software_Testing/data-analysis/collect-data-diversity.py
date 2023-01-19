from email import header
import os
import random
from collections import OrderedDict
import pandas as pd
import sys
import bz2
import glob
import numpy as np


def loadTestSuite(input_file):
    TS = {}
    with open(input_file) as fin:
        tcID = 1
        for tc in fin:
            TS[tcID] = tc[:-1]
            tcID += 1
    del TS[1]
    shuffled = list(TS.items())
    TS = OrderedDict(shuffled)
    return TS

def compressExcept(TCS, toExclude):
    s = " ".join([TCS[tcID] for tcID in TCS.keys() if tcID != toExclude])
    b = s.encode()
    cs = bz2.compress(b)
    return sys.getsizeof(cs)

def compressSingle(tc):
    b = tc.encode()
    cs = bz2.compress(b)
    return sys.getsizeof(cs)

def select(TCS):
    maxIndex, maxCompress, minCompress = 0, 0, float("inf")
    c_set = compressExcept(TCS, -1)
    for tcID in TCS.keys():
        c = compressExcept(TCS, tcID)
        if c > maxCompress:
            maxIndex, maxCompress = tcID, c
        c_min = compressSingle(TCS[tcID])
        if c_min < minCompress:
            minCompress = c_min
    nc_1 = (c_set - minCompress) / maxCompress
    return maxIndex, nc_1

# # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":

    algorithms = ["RBST","SBST-ML","ART"]

    for alg in algorithms:
        input_files = glob.glob("./data_for_scripts/_csv/"+ alg +"/*.csv")

        list_of_NCD = []
        list_of_NCD_in = []
        list_of_NCD_out = []
        for input in range(len(input_files)):

            input_file=input_files[input]
            print("Processing input file ...")
            print(input_file)
            print("\n")

            output_columns = ['max_dist_center_of_the_lane', 'min_dist_with_other_vehicles', 'min_dist_with_pedestrians', 'min_dist_static_obstacles', 'dist_traveled']
            all_data = pd.read_csv(input_file)

            i_tsd_data = all_data.drop(columns=output_columns)
            o_tsd_data = all_data.loc[:, output_columns]

            i_tsd_data.to_csv("./temp_in_file.csv", mode='w')
            o_tsd_data.to_csv("./temp_out_file.csv", mode='w')

            TCS = loadTestSuite("./temp_in_file.csv")
            P = []
            NC_1 = []
            iteration, total = 0, float(len(TCS))
            if len(TCS) <= 1:
                NCD_in = 0
                print("NCD IN value = "+str(NCD_in))
            else:
                while len(TCS) > 1:
                    s, nc_1 = select(TCS)
                    NC_1.append(nc_1)
                    P.append(s)
                    del TCS[s]
                NCD_in = max(NC_1)
                print("NCD IN value = "+str(NCD_in))

            TCS = loadTestSuite("./temp_out_file.csv")
            P = []
            NC_1 = []
            iteration, total = 0, float(len(TCS))
            if len(TCS) <= 1:
                NCD_out = 0
                print("NCD IN value = "+str(NCD_out))
            else:
                    while len(TCS) > 1:
                        s, nc_1 = select(TCS)
                        NC_1.append(nc_1)
                        P.append(s)
                        del TCS[s]
                    NCD_out = max(NC_1)
                    print("NCD OUT value = " + str(NCD_out))
            
            list_of_NCD.append((NCD_in, NCD_out))
            os.remove("./temp_in_file.csv")
            os.remove("./temp_out_file.csv")
        print("List of NCD values for all processed files:")

        print(list_of_NCD)
        all_NCD = np.asarray(list_of_NCD)
        print("\n")
        print(all_NCD)

        df = pd.DataFrame(all_NCD, columns=['input_d','output_d'])
        df.insert(0,'technique',alg)


        df.to_csv("./output/_diversity/"+ alg +"_NCD.csv", mode='w', header=True, index=False)


    # combine
    first = True
    path = "./output/_diversity/"

    for alg in algorithms:
        if os.path.exists(path + alg + "_NCD.csv"):
            if first == True:
                df_combined = pd.read_csv(path + alg + "_NCD.csv")
                first = False
            else:
                df_temp = pd.read_csv(path + alg + "_NCD.csv")
                df_combined = pd.concat([df_combined, df_temp], ignore_index=True)
    
    df_combined.to_csv(path + "combined_all.csv", index=False)
