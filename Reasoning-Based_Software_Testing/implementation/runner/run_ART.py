import pandas as pd
import multiprocessing
import logging
import time
from sympy import false
from lib.art import *
from datetime import datetime
from runner import run_single_scenario

logger = None;

class Pylot_caseStudy():
    def __init__(self):
        logger = logging.getLogger()

        now = datetime.now()
        log_file = 'output/temp/' + str(i) + 'ADAPT' + str(now) + '.log'
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


def run(i):

    ub ={"road_type":3, "road_ID":3, "scenario_length":0, "vehicle_in_front":1, "vehicle_in_adjcent_lane":1, "vehicle_in_opposite_lane":1, "vehicle_in_front_two_wheeled":1, "vehicle_in_adjacent_two_wheeled":1, "vehicle_in_opposite_two_wheeled":1, "time_of_day":2, "weather":6, "pedestrian":1, "vehicle_target_speed":2, "presence_of_trees":1, "presence_of_buildings":1, "driving_task":2}
    size = 20
    lb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ub = [4, 4, 0, 2, 2, 2, 2, 2, 2, 3, 7, 2, 3, 2, 2, 3]

    while(True):

        print("I Generating one test")
        generated_test = generate_adaptive_random_population(size, ub, lb)

        for test in generated_test:
            print(test)
            print("I Executing RANDOM test...")

            output = Pylot_caseStudy()._evaluate(test)
            print(output)


if __name__ == "__main__":
    times_of_repetitions = 1

    for i in range(0, times_of_repetitions):
            
        p = multiprocessing.Process(target=run, name="run", args=(i,))
        p.start()

        for t in range(120):
            if p.is_alive():
                time.sleep(60)
            else:
                break

        p.terminate()
        p.join()
        time.sleep(60)
