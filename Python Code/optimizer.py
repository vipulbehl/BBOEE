import BBO as bbo
import BBOEE as bboee
import benchmarks
import csv
import numpy
import time
import matplotlib.pyplot as plt

def selector(algo,func_details,popSize,Iter):
    function_name=func_details[0]
    lb=func_details[1]
    ub=func_details[2]
    dim=func_details[3]

    if(algo==0):
        x=bbo.BBO(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    elif(algo==1):
        x=bboee.BBOEE(getattr(benchmarks, function_name),lb,ub,dim,popSize,Iter)
    return x

def plotGraph():
    for con in results:
        plt.plot(con.convergence)
    plt.xlabel('Iterations')
    plt.ylabel('Fitness')
    plt.show()

# Select optimizers
BBO=False
BBOEE=True

# Select benchmark function
F1=True
F2=False
F3=False
F4=False
F5=False
F6=False
F7=False
F8=False
F9=False
F10=False
F11=False
F12=False
F13=False
F14=False
F15=False
F16=False
F17=False
F18=False
F19=False



optimizer=[BBO,BBOEE]
benchmarkfunc=[F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,F11,F12,F13,F14,F15,F16,F17,F18,F19]

# Select number of repetitions for each experiment.
# To obtain meaningful statistical results, usually 30 independent runs are executed for each algorithm.
NumOfRuns=1

# Select general parameters for all optimizers (population size, number of iterations)
PopulationSize = 30
Iterations= 100

# Check if it works at least once
Flag=False

#Export results ?
Export=True

# CSV Header for the convergence
CnvgHeader=[]
for l in range(0,Iterations):
	CnvgHeader.append("Iter"+str(l+1))

results = []
# numpy.zeros((optimizer.size,1))

# Loop for different optimizer functions
for i in range (0, len(optimizer)):

    #Loop for benchmark functions
    for j in range (0, len(benchmarkfunc)):
        if((optimizer[i]==True) and (benchmarkfunc[j]==True)):

            for k in range (0,NumOfRuns):
                func_details=benchmarks.getFunctionDetails(j)
                #Calling the main algorithm code
                x=selector(i,func_details,PopulationSize,Iterations)

                #Saving the results
                results.append(x)

                #Exporting the results in a csv file
                if(Export==True):
                    ExportToFile="Results/"+str(func_details[3])+"dimension"+str(Iterations)+".csv"
                    with open(ExportToFile, 'a') as out:
                        writer = csv.writer(out,delimiter=',')
                        if (Flag==False): # just one time to write the header of the CSV file
                            header= numpy.concatenate([["Optimizer","objfname","startTime","EndTime","ExecutionTime"],CnvgHeader])
                            writer.writerow(header)
                        a=numpy.concatenate([[x.optimizer,x.objfname,x.startTime,x.endTime,x.executionTime],x.convergence])
                        writer.writerow(a)
                    out.close()
                Flag=True # at least one experiment
plotGraph()

if (Flag==False): # Faild to run at least one experiment
    print("No Optomizer or Cost function is selected. Check lists of available optimizers and cost functions")
