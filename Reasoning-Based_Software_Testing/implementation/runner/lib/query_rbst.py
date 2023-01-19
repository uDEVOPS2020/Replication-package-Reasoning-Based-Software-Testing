import sys
import os
from dowhy import gcm
import numpy as np, pandas as pd
from dowhy.gcm.uncertainty import estimate_variance
from pycausal.pycausal import pycausal as pc
from pycausal import search as s
import networkx as nx



pc = pc()


def init_model(df_in):
    df = df_in.drop('scenario_length', axis=1)
  
    tetrad = s.tetradrunner()
  
    tetrad.run(algoId = 'fci', dfs = df, testId = 'fisher-z-test', 
        depth = -1, maxPathLength = -1, 
        completeRuleSetUsed = False, verbose = False)

    dot = pc.tetradGraphToDot(tetrad.getTetradGraph())
    original_stdout = sys.stdout
    with open("./temp_data/graph.dot", 'w') as res:
        sys.stdout = res
        print(dot)
        sys.stdout = original_stdout 

    causal_model = nx.DiGraph(nx.nx_pydot.read_dot("./temp_data/graph.dot")) 
    nodes = causal_model.nodes
    graph = causal_model
    causal_model = gcm.StructuralCausalModel(causal_model)

    data = df

    gcm.auto.assign_causal_mechanisms(causal_model, data)

    gcm.fit(causal_model, data)

    return causal_model, nodes, graph



def evolve_model(df_in):
    df = df_in.drop('scenario_length', axis=1)

    tetrad = s.tetradrunner()

    tetrad.run(algoId = 'fci', dfs = df, testId = 'fisher-z-test', 
        depth = -1, maxPathLength = -1, 
        completeRuleSetUsed = False, verbose = False)

    dot = pc.tetradGraphToDot(tetrad.getTetradGraph())
    original_stdout = sys.stdout
    with open("./temp_data/graph.dot", 'w') as res:
        sys.stdout = res
        print(dot)
        sys.stdout = original_stdout 

    causal_model = nx.DiGraph(nx.nx_pydot.read_dot("./temp_data/graph.dot")) 
    nodes = causal_model.nodes
    graph = causal_model
    causal_model = gcm.StructuralCausalModel(causal_model) 

    gcm.auto.assign_causal_mechanisms(causal_model, df)

    gcm.fit(causal_model, df)

    return causal_model, nodes, graph



def query_model(causal_model, dictionary):    

    samples = gcm.interventional_samples(causal_model,
                                        dictionary,
                                        num_samples_to_draw=1000)

    return samples
    

def causal_influence(causal_model, feature):
    contributions = gcm.intrinsic_causal_influence(causal_model, feature,
                                                gcm.ml.create_linear_regressor(),
                                                lambda x, _: estimate_variance(x))
    return contributions



def compute_raw(inputs):
    data_directory="./Results/"
    csv_directory="./Results/csv/"
    file_name = data_directory + str(inputs)
    file_name_ex = file_name+'_ex.log'

    f=open(file_name, 'r')
    
    f_lines = f.readlines()

    original_stdout = sys.stdout

    with open(csv_directory + str(inputs)+'.csv', 'w') as fp:
        sys.stdout = fp 
        print('DfC,DfV,DfP,DfM,DT')
        for line in f_lines:
            line_parts = line.split('>')
            line = line_parts[1].replace('DfC:','').replace('DfV:','').replace('DfP:','').replace('DfM:','').replace('DT:','')
            print(line)
        
    sys.stdout = original_stdout 

    df = pd.read_csv(csv_directory + str(inputs)+'.csv')

    DfC = round(df['DfC'].max(),4)
    DfV = round(df['DfV'].min(),4)
    DfP = round(df['DfP'].min(),4)
    DfM = round(df['DfM'].min(),4)

    Dm = df['DT'].min()
    if Dm < 0:
        Dm = 0

    DT = round((df['DT'].max() - Dm)/df['DT'].max(),4)

    if os.path.exists(file_name_ex):
        file_handler_ex = open(file_name_ex, "r")
        for line_ex in file_handler_ex:
            # if "red_light" in line_ex:
            #     print("Red_light invasion")
            #     traffic_lights_max = 0
            if "lane" in line_ex:
                print("lane invasion")
                DfC = 1.5
            if "vehicle" in line_ex:
                print("vehicle collision")
                DfV = 0
            if "static" in line_ex:
                print("static collision")
                DfM = 0    


    return DfC, DfV, DfP, DfM, DT


def get_covered_objectives():
    covered_objectives = []

    if os.path.exists("./temp_data/dataset_simulated.csv"):
        
        simulated_tests = pd.read_csv("./temp_data/dataset_simulated.csv")


        # if((simulated_tests['max_dist_center_of_the_lane'] >= 1.15).any()):
        #     covered_objectives.append('max_dist_center_of_the_lane')

        if((simulated_tests['min_dist_with_other_vehicles'] <= 0).any()):
            covered_objectives.append('min_dist_with_other_vehicles')
            
        # if((simulated_tests['min_dist_with_pedestrians'] <= 0).any()):
        #     covered_objectives.append('min_dist_with_pedestrians')

        # if((simulated_tests['min_dist_static_obstacles'] <= 0).any()):
        #     covered_objectives.append('min_dist_static_obstacles')

        # if((simulated_tests['dist_traveled'] <= 0.95).any()):
        #     covered_objectives.append('dist_traveled')

    return covered_objectives