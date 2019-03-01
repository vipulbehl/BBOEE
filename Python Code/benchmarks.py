import numpy
import math

simpleList1=[]
simpleList2=[]
simpleList3=[]
matrixDimension = []

# define the function blocks

#Rosenbrock's Function CEC
def F2(z):
    f = 0.0
    for i in range(0,len(z)-1):
        f += 100*pow(pow(z[i],2)-z[i+1],2) + pow(z[i]-1,2)
    return f

#Rastrigin function CEC
def F1(x):
	fitness = 10*len(x)
	for i in range(len(x)):
		fitness += x[i]**2 - (10*math.cos(2*math.pi*x[i]))
	return fitness

def F4(x):
    s=numpy.sum(x**2);
    return s

def getFunctionDetails(a):

    # [name, lb, ub, dim]
    param = {  0: ["F1",-100,100,100],
            }
    return param.get(a, "nothing")

def shiftFunc(pop_inv,list,dimension,simpleList2):
    for(i in range(dimension)):
        list[i] = pop_inv[i]-simpleList2[i]

def rotateFunc(pop_inv,list,dimension,matrixDimension):
    for(i in range(dimension)):
        list[i]=0
        for(j in range(dimension)):
            list[i]= list[i]+pop_inv[j]*matrixDimension[i*dimension+j]

def sr_func(pop_inv, simpleList1, dimension, simpleList2, matrixDimension, shiftRate, shiftFlag, rotateFlag):
    if(shiftFlag==1):
        if(rotateFlag==1):
            shiftFunc(pop_inv,simpleList3,dimension,simpleList2)
            for(i in range(dimension)):
                simpleList3[i] *= shiftRate
            rotateFunc(simpleList3,simpleList1,dimension,matrixDimension)
        else:
            shiftFunc(pop_inv,simpleList1,dimension,simpleList2)
            for(i in range(dimension)):
                simpleList1[i] *= shiftRate
    else:
        if(rotateFlag==1):
            for(i in range(dimension)):
                simpleList3[i] = pop_inv[i]*shiftRate
            rotateFunc(simpleList3,simpleList1,dimension,matrixDimension)
        else:
            for(i in range(dimension)):
                simpleList1[i] = pop_inv[i] * shiftRate
