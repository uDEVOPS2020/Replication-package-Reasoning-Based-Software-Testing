from curses import termattrs
import numpy as np, pandas as pd
import random

def calculate_minimum_distance(candidate, random_pop):
    distance = 1000
    for each_candidate in random_pop:
        vals = each_candidate
        candidate_vals = candidate
        dist = np.linalg.norm(np.array(vals) - np.array(candidate_vals))
        if dist < distance:
            distance = dist
    return distance


def generate_adaptive_random_population(size, lb, ub, i =0):
    random_pop = []

    random_pop.append(generate_random_population(1, lb, ub)[0])

    while len(random_pop) < size:
        D = 0
        selected_candidate = None
        rp = generate_random_population(size, lb, ub)
        for each_candidate in rp:
            min_dis = calculate_minimum_distance(each_candidate, random_pop)
            if min_dis > D:
                D = min_dis
                selected_candidate = each_candidate
        random_pop.append(selected_candidate)

    return random_pop


def generate_random_population(size, lb, ub):
    random_pop = []

    for i in range(size):
        candidate_vals = []
        for index in range(len(lb)):
            val = int(random.uniform(lb[index], ub[index]))

            if index == 12:
                if val == 0:
                    val = 20
                elif val == 1:
                    val = 30
                else:
                    val = 40

            candidate_vals.append(val)

        random_pop.append(candidate_vals)
    return random_pop