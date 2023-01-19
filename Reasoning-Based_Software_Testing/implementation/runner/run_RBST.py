import pandas as pd
import multiprocessing
import sys
import logging
import time

from sympy import false
from lib.query_rbst import *
from lib.rbst import *
from datetime import datetime
from runner import run_single_scenario
from pycausal.pycausal import pycausal as pc


pc = pc()
logger = None;

class Pylot_caseStudy():
    def __init__(self):
        logger = logging.getLogger()

        now = datetime.now()
        log_file = 'output/temp/' + str(i) + 'RBST' + str(now) + '.log'
        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(message)s')
        logger.setLevel(logging.DEBUG)
        logger.info("Started")
    def _evaluate(self,x):
        fv = x
        if fv[0]!= 3:
            fv[15] = 0
        DfC_min, DfV_max, DfP_max, DfM_max, DT_max, traffic_lights_max = run_single_scenario(fv)

        logger = logging.getLogger()


        logger.info(str(fv)+':'+ str(DfC_min)+ ','+str( DfV_max)+','+str(DfP_max)+ ','+str(DfM_max)+ ','+str( DT_max) +','+ str(traffic_lights_max))

        return [DfC_min, DfV_max, DfP_max, DfM_max, DT_max, traffic_lights_max]

def check_if_test_simulated(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            line = line.replace(",", ", ")
            if string_to_search in line:
                return True
    return False


def update_vehicle_target_speed(data, op):
    if op == "normalize":
        data.loc[data['vehicle_target_speed'] == 20, 'vehicle_target_speed'] = 0
        data.loc[data['vehicle_target_speed'] == 30, 'vehicle_target_speed'] = 1
        data.loc[data['vehicle_target_speed'] == 40, 'vehicle_target_speed'] = 2
    elif op == "denormalize":
        data.loc[data['vehicle_target_speed'] == 0, 'vehicle_target_speed'] = 20
        data.loc[data['vehicle_target_speed'] == 1, 'vehicle_target_speed'] = 30
        data.loc[data['vehicle_target_speed'] == 2, 'vehicle_target_speed'] = 40

    return data

def run(i):

    input_features = ["road_type","road_ID","scenario_length","vehicle_in_front","vehicle_in_adjcent_lane","vehicle_in_opposite_lane","vehicle_in_front_two_wheeled","vehicle_in_adjacent_two_wheeled","vehicle_in_opposite_two_wheeled","time_of_day","weather","pedestrian","vehicle_target_speed","presence_of_trees","presence_of_buildings","driving_task"]

    ub ={"road_type":3, "road_ID":3, "scenario_length":0, "vehicle_in_front":1, "vehicle_in_adjcent_lane":1, "vehicle_in_opposite_lane":1, "vehicle_in_front_two_wheeled":1, "vehicle_in_adjacent_two_wheeled":1, "vehicle_in_opposite_two_wheeled":1, "time_of_day":2, "weather":6, "pedestrian":1, "vehicle_target_speed":2, "presence_of_trees":1, "presence_of_buildings":1, "driving_task":2}
    pc.start_vm()

    iteration = 0

    while(True):
        if iteration==0:
            print("I Initializing model")
            data_compl = pd.read_csv(sys.argv[1])
            data_compl.to_csv("./temp_data/knowledge.csv",index=False)
            data_compl = update_vehicle_target_speed(data_compl, "normalize")
            causal_model, nodes, graph = init_model(data_compl)
            data_compl = select_n_higher_reward(data_compl,1)
        else:
            print("I Evolving model")
            knowledge = pd.read_csv("./temp_data/knowledge.csv")
            data_compl = select_n_higher_reward(knowledge,1)
            knowledge = update_vehicle_target_speed(knowledge, "normalize")
            causal_model, nodes, graph = evolve_model(knowledge)
        
        data = data_compl[list(nodes)]
        data = data[list(set(input_features).intersection(nodes))]

        new_tests = pd.DataFrame()


        for i in range(0,data_compl.shape[0]):
            to_simulate = True
            combos = list(set(input_features).intersection(nodes))

            # print("NODES: " + str(nodes))
            # print("COMBOS: " + str(combos))

            test = data_compl.iloc[[i]]
            temp_test = test.reset_index(drop=True)
            generated_test = alg2_sel_and_maximize_rand(combos, 1, causal_model, temp_test, graph, input_features, ub)
            generated_test = update_vehicle_target_speed(generated_test, "denormalize")
            inputs = generated_test.iloc[: ,0:16].to_csv(header=None, index=False)
            inputs = inputs.replace("\r", "").replace("\n", "").split(",")
            inputs = [int(float(numeric_string)) for numeric_string in inputs]

            for column in input_features:
                generated_test[column] = generated_test[column].astype(np.int64)

            if i > 0:
                try:
                    merged = pd.merge(generated_test[input_features], new_tests[input_features], on=input_features, how='outer', indicator=True)
                    merged = merged[merged["_merge"] == "both"]
                    print("MERGE i="+ str(i) +": " + str(merged[merged["_merge"] == "both"]))
                    if not merged.empty:
                        print("I test already simulated, skipping...")
                        to_simulate = False
                except Exception as e:
                    print("EXCEPTION_not able to merge")


            if os.path.exists("./simulazione_risultati/dataset_simulated.csv"):
                if check_if_test_simulated("./simulazione_risultati/dataset_simulated.csv", str(inputs).replace('[','').replace(']','')):
                    print("I test already simulated, skipping...")
                    to_simulate = False

            if to_simulate:
                print("I Executing test...")
                output = Pylot_caseStudy()._evaluate(inputs)
                print(output)
                # time.sleep(5)
                DfC, DfV, DfP, DfM, DT = compute_raw(inputs)

                generated_test["max_dist_center_of_the_lane"] = DfC
                generated_test["min_dist_with_other_vehicles"] = DfV
                generated_test["min_dist_with_pedestrians"] = DfP
                generated_test["min_dist_static_obstacles"] = DfM
                generated_test["dist_traveled"] = DT

                new_tests=new_tests.append(generated_test)

        new_tests.to_csv("./temp_data/knowledge.csv", mode='a', header=False, index=False)

        if os.path.exists("./temp_data/dataset_simulated.csv"):
            new_tests.to_csv("./temp_data/dataset_simulated.csv", mode='a', header=False, index=False)
        else:
            new_tests.to_csv("./temp_data/dataset_simulated.csv", header=True, index=False)
            
        new_tests.to_csv("./temp_data/dataset_iteration.csv",index=False)
        iteration = iteration + 1


if __name__ == "__main__":
    times_of_repetitions = 1

    for i in range(0, times_of_repetitions):

        if os.path.exists("./temp_data/dataset_simulated.csv"):
            os.remove("./temp_data/dataset_simulated.csv")
            
        p = multiprocessing.Process(target=run, name="run", args=(i,))
        p.start()

        for t in range(1200):

            if p.is_alive():
                time.sleep(60)
            else:
                break

        p.terminate()
        
        # Cleanup
        p.join()
        time.sleep(60)

    pc.stop_vm()