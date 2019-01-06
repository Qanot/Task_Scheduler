from subprocess import Popen
from os import listdir
from os.path import isfile, join
import re
import time
import numpy as np



def main():
    bat_re = re.compile(r'\b[0-9]{6}.bat')
    file_list = listdir("D:\inne\inne\Szeregowanie zadań")
    file_list = [x for x in file_list if bat_re.match(x)]
    # for n in [10, 20, 50, 100, 200, 500, 1000]:

    f = open("Times.txt", "w")
    f.write("Czasy: \n")

    # nn = [10, 20, 50, 100, 200, 500, 1000, 10, 20, 50, 100, 200, 500, 1000, 10, 20, 50, 100, 200, 500, 1000, 10, 20, 50, 100, 200, 500, 1000]
    # hh = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
    # kk = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 8]

    nn = [1000,1000,1000,1000,1000]
    hh = [0.2, 0.2, 0.2, 0.2, 0.2]
    kk = [1, 2, 3, 4, 5]


    for bat in file_list:
        time_list = []
        for i in range(len(nn)):
            tic = time.clock()
            p = Popen(bat + " " + str(nn[i]) + " " + str(kk[i]) + " " + str(hh[i]), cwd=r"D:\inne\inne\Szeregowanie zadań")
            p.communicate()
            toc = time.clock()
            delta = toc - tic
            time_list.append(delta)
        # print(bat, time_list)
        f.write(str(bat.replace(".bat", "")) + "; time: " + str("{:.4f}".format(np.mean(time_list))) + "\n")
    f.close()


if __name__ == "__main__":
    main()