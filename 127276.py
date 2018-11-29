import re
import time
import numpy as np
import sys


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
        if (n == file.replace("sch","").replace(".txt", "")):
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


def algorytm(problem, d):
    temp_problem = np.copy(problem)
    temp_problem = temp_problem[(temp_problem[:, 1] - temp_problem[:, 2]).argsort()]
    # temp_problem = np.concatenate(split_early_late_better(temp_problem), axis=0)

    early_jobs, late_jobs = split_early_late(temp_problem, d)

    early_jobs = early_jobs[((0.01*early_jobs[:, 1] / early_jobs[:, 0])).argsort()]
    late_jobs = np.copy(late_jobs[((late_jobs[:, 0] / (late_jobs[:, 2]))).argsort()])
    temp_problem = np.concatenate((early_jobs, late_jobs), axis=0)
    return temp_problem.copy()


def proces(n, k, h):
    # problem = load_files()[str(n)][k - 1]
    problem = load_file(str(n), k-1)
    d = int(np.sum(problem[:, 0]) * h)
    tic = time.clock()
    min_cost_prob = (algorytm(problem, d))
    toc = time.clock()
    delta = toc - tic

    ind_list = get_indices(problem, min_cost_prob)
    cost = cost_function(min_cost_prob, d)

    f = open("sch_" + "127276_" + str(n) + "_" + str(k) + "_" + str(int(h*10)) + ".out", "w")
    f.write(str(int(cost)) + "\n")
    f.write(str(ind_list[0]))
    for i in ind_list[1:]:
        f.write(" " + str(i))
    print("k: " + str(k) + " n: " + str(len(min_cost_prob)) + " sum: " +
		str(np.sum(min_cost_prob[:, 0])) + " h: " + str(h) + " cost: " +
		str(cost) + " Time: " + "{:.4f}".format(delta*1000) + " ms")
    # print(ind_list)
    print(cost)
    f.close()

def main():
    # try:
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    h = float(sys.argv[3])
    proces(n, k, h)

if __name__ == "__main__":
    main()




