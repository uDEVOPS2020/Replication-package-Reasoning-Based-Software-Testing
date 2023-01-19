import numpy as np, pandas as pd
import networkx as nx
import random
from curses import termattrs
from dowhy import gcm
from query_rbst import *


def select_n_higher_reward(data_compl, num):
    selected_tests = pd.DataFrame(data=None, columns = data_compl.columns)

    for i in range(0,num):
        maxs = compute_maxs(data_compl)
        mins = compute_mins(data_compl)
        r = []

        for index, row in data_compl.iterrows():
            r.append(reward(row, maxs, mins))

        selected_tests.loc[len(selected_tests.index)] = data_compl.iloc[r.index(max(r))]

        data_compl.drop(r.index(max(r)), axis=0, inplace=True)
        data_compl.reset_index(inplace=True, drop=True)

    return selected_tests

def select_n_higher_reward_obj(data_compl):
    selected_tests = pd.DataFrame(data=None, columns = data_compl.columns)
    objectives = ["max_dist_center_of_the_lane", "min_dist_with_other_vehicles", "min_dist_with_pedestrians", "min_dist_static_obstacles", "dist_traveled"]

    for objective in objectives:
        print(objective)
        r = []
        for index, row in data_compl.iterrows():
            r.append(reward_spec(row, data_compl[objective].max(), data_compl[objective].min(), objective))

        print(r)
        selected_tests.loc[len(selected_tests.index)] = data_compl.iloc[r.index(max(r))]

        data_compl.drop(r.index(max(r)), axis=0, inplace=True)
        data_compl.reset_index(inplace=True, drop=True)

    return selected_tests


def compute_maxs(tests):
    columns = []
    values = []

    if "min_dist_with_other_vehicles" in tests:
        columns.append("min_dist_with_other_vehicles")
        max = tests["min_dist_with_other_vehicles"].max()
        if max >= 950:
            df_temp = tests.drop(tests.loc[tests['min_dist_with_other_vehicles']==max].index)
            max = df_temp["min_dist_with_other_vehicles"].max()
        values.append(max)
    
    return pd.DataFrame([values], columns = columns, index=None)

def compute_mins(tests):
    columns = []
    values = []
        
    if "min_dist_with_other_vehicles" in tests:
        columns.append("min_dist_with_other_vehicles")
        min = tests["min_dist_with_other_vehicles"].min()
        if min < 0:
            min = 0
        values.append(min)
    
    return pd.DataFrame([values], columns = columns, index=None)

def reward(test_outcome, maxs, mins):
    rew = 0

    if "min_dist_with_other_vehicles" in maxs:
        DV = test_outcome["min_dist_with_other_vehicles"]
        max = maxs["min_dist_with_other_vehicles"]
        min = mins["min_dist_with_other_vehicles"]
        
        if DV < 0:
            DV = 0
        elif DV > float(max):
            DV = max

        rew = 1 - (DV-min)/(max-min)

    return rew[0]



def simulation_more_compl(test, causal_model, selected_feature):
    dictionary = {}
    for i in selected_feature:
        y = test.iloc[0][i]
        temp_dict = dict({i: lambda y=y: y})
        dictionary.update(temp_dict) 

    gen_tests = query_model(causal_model, dictionary)

    r = []

    maxs = compute_maxs(gen_tests)
    mins = compute_mins(gen_tests)

    for index, row in gen_tests.iterrows():
        r.append(reward(row, maxs, mins))

    print("Reward = " + str(max(r)))

    return gen_tests.iloc[r.index(max(r))]
        

def alg2_sel_and_maximize_rand(combos, num, causal_model, test, graph, input_features, ub):
    sel = []
    generated_test = test.copy()

    #initialize random test
    for input in input_features:
        val = random.randint(0, ub[input])
        generated_test[input][0] = val

    for i in range(0, num):
        sel.append(random.choice(combos))
        combos.remove(sel[i])

    gen_test = simulation_more_compl_v2(causal_model, sel[0], ub)
    
    for column in gen_test.index:
        if column in input_features:

            pd.set_option('mode.chained_assignment', None)
            value = round(gen_test[column])

            if value >= 0:
                if value > ub[column]:
                    value = ub[column]

                generated_test[column][0] = value
            else:
                generated_test[column][0] = 0

    return generated_test


def simulation_more_compl_v2(causal_model, selected_feature, ub):
    dict_arr = []
    ub_sel = ub.get(selected_feature)

    print(selected_feature + ' UB ' + str(ub_sel))

    for i in range(0,ub_sel+1):
        dictionary = {}
        y=i
        temp_dict = dict({selected_feature: lambda y=y: y})
        dictionary.update(temp_dict) 
        dict_arr.append(dictionary)
    
    best_rew = []
    best_tests = []

    for i in range(0,len(dict_arr)):
        r = []
        gen_tests = query_model(causal_model, dict_arr[i])

        maxs = compute_maxs(gen_tests)
        mins = compute_mins(gen_tests)

        for index, row in gen_tests.iterrows():
            r.append(reward(row, maxs, mins))

        best_rew.append(max(r))
        best_tests.append(gen_tests.iloc[r.index(max(r))])
        print(str(i) + ': ' + str(best_rew[i]))


    return best_tests[best_rew.index(max(best_rew))]


def reward_spec(test_outcome, max, min, objective):
    rew = 0
    covered_objectives = get_covered_objectives()

    if objective not in covered_objectives:
        value = test_outcome[objective]
        print("value: " + str(value) + "max: " + str(max) + "min: " + str(min))
        if value < 0:
            value = 0
        elif value > float(max):
            value = max

        if objective == "max_dist_center_of_the_lane":
            rew = (value-min)/(max-min)
        else:
            rew = 1 - (value-min)/(max-min)
            
        print(str(rew))

    return rew


def generate_random_test(ub):
    columns = ["road_type","road_ID","scenario_length","vehicle_in_front","vehicle_in_adjcent_lane","vehicle_in_opposite_lane","vehicle_in_front_two_wheeled","vehicle_in_adjacent_two_wheeled","vehicle_in_opposite_two_wheeled","time_of_day","weather","pedestrian","vehicle_target_speed","presence_of_trees","presence_of_buildings","driving_task","max_dist_center_of_the_lane","min_dist_with_other_vehicles","min_dist_with_pedestrians","min_dist_static_obstacles","dist_traveled"]
    
    selected_tests = pd.DataFrame(data=None, columns = columns)

    test = []

    count = 0
    for column in columns:
        
        if count >= 16 and column == "max_dist_center_of_the_lane":
            val = 0
        elif count >= 16:
            val = 1000
        else:
            val = random.randint(0, ub[column])
        count = count + 1
        test.append(val)

    selected_tests = selected_tests.append(pd.DataFrame([test], columns = columns), ignore_index=True)

    return selected_tests