import re
import sys
import time

import numpy as np


def load_files():
    files_names = ["sch10.txt", "sch20.txt", "sch50.txt", "sch100.txt", "sch200.txt", "sch500.txt", "sch1000.txt"]
    problems_tasks = {}
    result_set = np.empty([len(files_names), 1])
    for (i, file) in enumerate(files_names):
        with open(file) as f:
            num_of_instances = int(next(f).strip())
            #             num_of_instances = 1 #set if want to have only one example of
            temp_instances = np.empty([num_of_instances], dtype=object)
            for nr_inst in range(num_of_instances):
                num_of_examples = int(next(f).strip())
                temp_tasks = np.empty([num_of_examples, 3], dtype=object)
                for nr_examp in range(num_of_examples):
                    temp_tasks[nr_examp] = np.array([int(x) for x in re.sub(' +', ' ', next(f)).strip().split(" ")])
                temp_instances[nr_inst] = temp_tasks
            problems_tasks[file.replace("sch", "").replace(".txt", "")] = temp_instances
            f.close()
    return problems_tasks


def load_file(n, k):
    files_names = ["sch10.txt", "sch20.txt", "sch50.txt", "sch100.txt", "sch200.txt", "sch500.txt", "sch1000.txt"]
    problems_tasks = {}
    result_set = np.empty([len(files_names), 1])
    for (i, file) in enumerate(files_names):
        if (n == file.replace("sch", "").replace(".txt", "")):
            with open(file, "r") as f:
                num_of_instances = int(next(f).strip())
                #             num_of_instances = 1 #set if want to have only one example of
                temp_instances = np.empty([num_of_instances], dtype=object)
                for nr_inst in range(num_of_instances):
                    num_of_examples = int(next(f).strip())
                    temp_tasks = np.empty([num_of_examples, 3], dtype=object)
                    for nr_examp in range(num_of_examples):
                        temp_tasks[nr_examp] = np.array([int(x) for x in re.sub(' +', ' ', next(f)).strip().split(" ")])
                    temp_instances[nr_inst] = temp_tasks
                problems_tasks[file.replace("sch", "").replace(".txt", "")] = temp_instances
                f.close()
    return problems_tasks[str(n)][k]


def cost_function(problem, d):
    cost_function_value = 0
    current = 0
    for i in range(len(problem)):
        current += problem[i, 0]
        if (current < d):
            cost_function_value += (d - current) * problem[:, 1][i]
        if (current > d):
            cost_function_value += (current - d) * problem[:, 2][i]
    return cost_function_value


def split_early_late(problem, d):
    current = 0
    for i in range(len(problem)):
        current += problem[i, 0]
        if (current >= d):
            return problem[0:i], problem[i:]


def split_early_late_better(problem):
    early = []
    late = []
    for i in problem:
        if i[1] < i[2]:
            early.append(i)
        else:
            late.append(i)
    return np.array(early), np.array(late)


def get_indices(x, y):
    x_temp = np.copy(x)
    result = np.empty([len(x_temp)], dtype=int)
    for (i, yy) in enumerate(y):
        for (j, xx) in enumerate(x_temp):
            if (yy[0] == xx[0] and yy[1] == xx[1] and yy[2] == xx[2]):
                result[i] = j
                x_temp[j] = -1
                break;
    return result


def initial_algorithm(problem, d):
    temp_problem = np.copy(problem)
    temp_problem = temp_problem[(temp_problem[:, 1] - temp_problem[:, 2]).argsort()]
    # temp_problem = np.concatenate(split_early_late_better(temp_problem), axis=0)

    early_jobs, late_jobs = split_early_late(temp_problem, d)

    early_jobs = early_jobs[((0.01 * early_jobs[:, 1] / early_jobs[:, 0])).argsort()]
    late_jobs = np.copy(late_jobs[((late_jobs[:, 0] / (late_jobs[:, 2]))).argsort()])
    temp_problem = np.concatenate((early_jobs, late_jobs), axis=0)
    return temp_problem.copy()


def heuristic(problem, d, time_left):

    temp_problem = problem.copy()
    temp_cost = cost_function(temp_problem, d)
    counter = 0
    while time_left > 200: #empiricly tested for appropriate value in miliseconds; there may be need of adjustment
        tic = time.clock()

        swap_indices = np.random.random_integers(0, len(temp_problem) - 1, int(len(temp_problem) * 0.1) + 1)
        # swap_indices = np.random.random_integers(0, len(temp_problem) - 1, 2)
        for task_index in swap_indices[1:]:
            temp_problem[[swap_indices[0], task_index]] = temp_problem[[task_index, swap_indices[0]]]
            # temp_problem[swap_indices] = temp_problem[swap_indices[::-1]]
            if cost_function(temp_problem, d) <= temp_cost:
                temp_cost = cost_function(temp_problem, d)
            else:
                temp_problem[[task_index, swap_indices[0]]] = temp_problem[[swap_indices[0], task_index]]
                # temp_problem[swap_indices[::-1]] = temp_problem[swap_indices]
        # counter += 1
        # print(counter)


        toc = time.clock()
        time_left -= (toc - tic) * 1000
    return temp_problem


def proces(n, k, h, c):
    time_left = n * c

    time_start_processing = time.clock()

    # problem = load_files()[str(n)][k - 1]
    problem = load_file(str(n), k - 1)
    d = int(np.sum(problem[:, 0]) * h)

    time_start_algorithm = time.clock()
    min_cost_prob = (initial_algorithm(problem, d))
    time_left_minus = time.clock()
    min_cost_prob = heuristic(min_cost_prob, d, time_left - (time_left_minus - time_start_processing))
    time_end_algorithm = time.clock()
    delta = time_end_algorithm - time_start_algorithm

    ind_list = get_indices(problem, min_cost_prob)
    cost = cost_function(min_cost_prob, d)


    #write results to file
    f = open("sch_" + "127276_" + str(n) + "_" + str(k) + "_" + str(int(h * 10)) + ".out", "w")
    f.write(str(int(cost)) + "\n")
    f.write(str(ind_list[0]))
    for i in ind_list[1:]:
        f.write(" " + str(i))
    print("k: " + str(k) + " n: " + str(len(min_cost_prob)) + " sum: " +
          str(np.sum(min_cost_prob[:, 0])) + " h: " + str(h) + " cost: " +
          str(cost) + " Time: " + "{:.4f}".format(delta * 1000) + " ms")
    f.close()


def main():
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    h = float(sys.argv[3])
    c = int(sys.argv[4])
    proces(n, k, h)


if __name__ == "__main__":
    main()
