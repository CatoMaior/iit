from random import random, randrange, randint
from math import sin, cos, acos, exp, sqrt
from matplotlib import pyplot as plt
from math import pi as PI
from sys import argv

#fileName = str(argv[1])
N = 10
trigger = 5000
J = -1
Kb = 1
res_arr1 = []
res_arr2 = []
res_arr3 = []
res_arr = []
sampleDelay = 100
n_samples = 10
C = [[0] * N for i in range(N)]
S = [[0] * N for i in range(N)]

def randomize():
    for a in range(N):
        for b in range(N):
            S[a][b] = [randrange(-6283, 6283)/2000, acos(2 * random() - 1)]

def scalarProduct(v1 = [0, 0], v2 = [0, 0]):
    return sin(v1[1]) * sin(v2[1]) * cos(v1[0] - v2[0]) + cos(v1[1]) * cos(v2[1])

def getCart():
    for a in range(N):
        for b in range(N):
            C[a][b] = [sin(S[a][b][0]) * cos(S[a][b][1]), sin(S[a][b][0])*sin(S[a][b][1]), cos(S[a][b][1])]

def getMagn():
    ans = [0, 0, 0]
    for a in range(N):
        for b in range(N):
            ans[0] += C[a][b][0]
            ans[1] += C[a][b][1] 
            ans[2] += C[a][b][2]
    return sqrt(ans[0] ** 2 + ans[1] ** 2 + ans[2] ** 2) / N ** 2
    

def runCycles(T):
    m_loc = 0
    m2_loc = 0
    for i in range(trigger + n_samples * sampleDelay):
        x = randint(0, N - 1)
        y = randint(0, N - 1)
        v = [randrange(-6283, 6283)/2000, acos(2 * random() - 1)]
        deltaE =  J * ((scalarProduct(v, S[(x + 1) % N][(y + 1) % N]) +
                           scalarProduct(v, S[(x + 1) % N][(y - 1) % N]) +
                           scalarProduct(v, S[(x - 1) % N][(y + 1) % N]) +
                           scalarProduct(v, S[(x - 1) % N][(y - 1) % N])) -
                           (scalarProduct(S[x][y], S[(x + 1) % N][(y + 1) % N]) +
                           scalarProduct(S[x][y], S[(x + 1) % N][(y - 1) % N]) +
                           scalarProduct(S[x][y], S[(x - 1) % N][(y + 1) % N]) +
                           scalarProduct(S[x][y], S[(x - 1) % N][(y - 1) % N]) ))
        if deltaE < 0:
            S[x][y] = v
        elif random() < exp(-deltaE/(Kb * T)):
            S[x][y] = v

        if i % sampleDelay == 0 and i > trigger:
            getCart()
            d = getMagn()
            m_loc += d
            m2_loc += d ** 2
    return [T, m_loc / n_samples, m2_loc / n_samples]
    
		


"""
for t in range(1, 201):
    t /= 100
    randomize()
    temp = runCycles(t)
    res_arr1.append(temp[0])
    res_arr2.append(temp[1])
    res_arr3.append(temp[2])

res_arr.append(res_arr1)
res_arr.append(res_arr2)
res_arr.append(res_arr3)
myFile = open(fileName, "w")
for i in range(len(res_arr1)):
    myFile.write(str(res_arr1[i]) + " " + str(res_arr2[i]) + " " + str(res_arr3[i]) + "\n")
myFile.close()

"""

for t in range(0, 40000, 5000):
    randomize()
    trigger = t
    res_arr2.append(runCycles(0.005)[1])
    res_arr1.append(t)

print(res_arr2)
plt.plot(res_arr1, res_arr2)
plt.show()












    

                           
