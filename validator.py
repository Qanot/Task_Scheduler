import re
import numpy as np
from collections import defaultdict
from os import listdir





def get_score(file_name):
    with open(file_name) as f:
        score = int(next(f).strip())
        tab = np.array([int(x) for x in re.sub(' +', ' ', next(f)).strip().split(" ")])
        f.close()
        return score, tab

def split_early_late(problem, d):
    current = 0
    for i in range(len(problem)):
        current += problem[i, 0]
        if (current >= d):
            return problem[0:i], problem[i:]

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

def load_files():
    files_names = ["sch10.txt", "sch20.txt", "sch50.txt", "sch100.txt", "sch200.txt", "sch500.txt", "sch1000.txt"]
    problems_tasks = {}
    result_set = np.empty([len(files_names), 1])
    for (i, file) in enumerate(files_names):
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

def load_bounds(n, k, h):
    dict_n = {}
    with open("bounds.txt", "r") as f:
        for i in [10,20,50,100,200,500,1000]:
            tab_k = np.empty([10], dtype=object)
            for kk in range(10):
                dict_h = {}
                tab = np.array([int(x.replace("*", "")) for x in re.sub(' +', ' ', next(f)).strip().split("\t")])
                for itr, hh in enumerate(["0.2", "0.4", "0.6", "0.8"]):
                    dict_h[hh] = tab[itr]
                tab_k[kk] = dict_h
            dict_n[str(i)] = tab_k
    return dict_n[str(n)][k-1][str(h)]

def algorytm(problem, d):
    temp_problem = np.copy(problem)
    temp_problem = temp_problem[(temp_problem[:, 1] - temp_problem[:, 2]).argsort()]
    # temp_problem = np.concatenate(split_early_late_better(temp_problem), axis=0)

    early_jobs, late_jobs = split_early_late(temp_problem, d)

    early_jobs = early_jobs[((0.01*early_jobs[:, 1] / early_jobs[:, 0])).argsort()]
    late_jobs = np.copy(late_jobs[((late_jobs[:, 0] / (late_jobs[:, 2]))).argsort()])
    temp_problem = np.concatenate((early_jobs, late_jobs), axis=0)
    return cost_function(temp_problem, d)

def proces_file(file, n, k, h, ranking_list):
    index = re.search(r'[0-9]{6}', file).group(0)
    # problem = load_files()[str(n)][k - 1]
    problem = load_file(str(n), k-1)
    d = int(np.sum(problem[:, 0]) * h)
    score, tab = get_score(file)
    print(index, n, k, h, "score: " + str(score))
    true = cost_function(problem[tab], d)
    print("True score: " + str(true))
    if (score != true):
        print("WARNING: " + str(index) + " score and true score not equal!!!!")
    # mine = algorytm(problem, d)
    mine = load_bounds(n, k, h)
    ref_vaule = (true-mine)/mine
    ranking_list[index].append((n, k, h, ref_vaule))

    f = open("results_" + str(n) + "_" + str(k) + "_" + str(int(h*10)) + ".txt", "a")
    f.write(str(index) + ": his " + str(score) +"; true " + str(true) + "; ref  " + str(ref_vaule) + "\n")
    f.close()

def print_ranking(ranking):
    mean_ranking = {}

    for key, value in ranking.items():
        mean_ranking[key] = np.mean([x[3] for x in value])
    mean_ranking =  sorted(mean_ranking.items(), key=lambda kv: kv[1])

    f = open("Ranking.txt", "w")
    f.write("Ranking: \n")
    print("\n\n\nRanking: ")
    x = 1;
    for key, value in mean_ranking:
        print(str(x) + "; Index " + str(key) + "; score: " +  str(value))
        f.write(str(x) + "; Index " + str(key) + "; score: " +  str("{:.4f}".format(value)) + "\n")
        x += 1
    f.close()

def main():
    print("Validator initialated")

    ranking_list = defaultdict(list)

    file_list = listdir("D:\inne\inne\Szeregowanie zadań")
    print(file_list)
    file_list = [x for x in file_list if x.endswith(".out")]
    # for n in [10, 20, 50, 100, 200, 500, 1000]:
    for out in file_list:
        (index, n, k, h) = out.replace("sch_", "").replace(".out", "").split("_")
        proces_file(out, int(n), int(k), float(h)/10, ranking_list)
    # print(ranking_list)
    print_ranking(ranking_list)



if __name__ == "__main__":
    main()