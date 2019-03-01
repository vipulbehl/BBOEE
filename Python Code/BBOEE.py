from __future__ import division
import random
import numpy
import math
from solution import solution
import time
import ClearDups


def BBOEE(objf,lb,ub,dim,PopSize,iters):
    # Defining the solution variable for saving output variables
    sol=solution()

    # Initializing BBO parameters
    pmutate = 0.01 # initial mutation probability
    Keep = 2 # elitism parameter: how many of the best habitats to keep from one generation to the next
    EvolConst = 50 # Evolution Constant

    # Initializing the parameters with default values
    fit = numpy.zeros(PopSize)
    EliteSolution=numpy.zeros((Keep,dim))
    EliteCost=numpy.zeros(Keep)
    Island=numpy.zeros((PopSize,dim))
    mu=numpy.zeros(PopSize)
    lambda1=numpy.zeros(PopSize)
    MinCost=numpy.zeros(iters)
    BestPopulation=numpy.zeros(dim)

    # Initializing Population
    population=numpy.random.uniform(0,1,(PopSize,dim)) *(ub-lb)+lb

    #Calculate objective function for each particle
    for i in range(PopSize):
        # Performing the bound checking
        population[i,:]=numpy.clip(population[i,:], lb, ub)
        fitness=objf(population[i,:])
        fit[i]=fitness

    # Calculating the growth and decline rate
    for i in range(PopSize):
        #Decline Rate
        mu[i] = (1 - ((i+1)/PopSize)) + EvolConst/(i+1);
        #Growth Rate
        lambda1[i] = ((i+1)/PopSize)*((i+1)*(PopSize-(i+1))/PopSize**2) + 2*((PopSize*(i+1))**0.5);


    print("BBOEE is optimizing  \""+objf.__name__+"\"")

    timerStart=time.time()
    sol.startTime=time.strftime("%Y-%m-%d-%H-%M-%S")

    # Defining the loop
    for l in range(iters):
        # Defining the Elite Solutions
        for j in range(Keep):
            EliteSolution[j,:]=population[j,:]
            EliteCost[j]=fit[j]

        # Performing Migration operator
        for k in range(PopSize):
            for j in range(dim):
                if random.random() < lambda1[k]:
                    # Performing Roulette Wheel
                    RandomNum = random.random() * sum(mu);
                    Select = mu[1];
                    SelectIndex = 0;
                    while (RandomNum > Select) and (SelectIndex < (PopSize-1)):
                        SelectIndex = SelectIndex + 1;
                        Select = Select + mu[SelectIndex];

                    Island[k,j] = population[SelectIndex,j]
                else:
                    Island[k,j] = population[k,j]

        # Performing Mutation
        for k in range(PopSize):
            for parnum in range(dim):
                if pmutate > random.random():
                    Island[k,parnum] = lb + (ub-lb) * random.random();

        # Performing the bound checking
        for i in range(PopSize):
            Island[i,:]=numpy.clip(Island[i,:], lb, ub)

        # Replace the habitats with their new versions.
        for k in range(PopSize):
            population[k,:] = Island[k,:]

        #Calculate objective function for each individual
        for i in range(PopSize):
            fitness=objf(population[i,:])
            fit[i]=fitness

        # Sort the fitness
        fitness_sorted=numpy.sort(fit)

        # Sort the population on fitness
        I=numpy.argsort(fit)
        population=population[I,:]

        # Replacing the individual of population with EliteSolution
        for k in range(Keep):
            population[(PopSize-1)-k,:] = EliteSolution[k,:];
            fit[(PopSize-1)] = EliteCost[k];

        # Removing the duplicate individuals
        population=ClearDups.ClearDups(population, PopSize, dim, ub, lb)

        #Calculate objective function for each individual
        for i in range(PopSize):
            fitness=objf(population[i,:])
            fit[i]=fitness

        # Sort the fitness
        fitness_sorted=numpy.sort(fit)

        # Sort the population on fitness
        I=numpy.argsort(fit)
        population=population[I,:]

        # Saving the best individual
        MinCost[l] = fit[1]
        BestPopulation=population[1,:]
        gBestScore=fit[1]

        # Displaying the best fitness of each iteration
        if (l%1==0):
               print(['At iteration '+ str(l+1)+ ' the best fitness is '+ str(gBestScore)]);

    timerEnd=time.time()
    sol.endTime=time.strftime("%Y-%m-%d-%H-%M-%S")
    sol.executionTime=timerEnd-timerStart
    sol.convergence=MinCost
    sol.optimizer="BBOEE"
    sol.objfname=objf.__name__

    return sol
