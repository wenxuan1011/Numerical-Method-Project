import numpy as np
import random
import math
import pandas as pd

class GeneticAlgorithm():
    def __init__(self, weight, intensity, duration, calories):
        self.N = 10  # Nnumber
        self.D = 2  # Dimension
        self.B = 5  # Bitnum
        self.n = 4  # Elite_num
        self.cr = 0.8  # CrossoverRate
        self.mr = 0.2  #MutationRate
        self.max_iter = 1000 # MaxIteration

        self.weight = weight
        self.intensity = intensity
        self.duration = duration
        self.calories = calories
        self.data = pd.read_csv('exercises_METs.csv')
        
    def generatePopulation(self):
        population = []
        for number in range(self.N):
            chrom_list = []
            for run in range(self.D):
                element = (np.zeros((1,self.B))).astype(int)
                for i in range(1):
                    a = True
                    while(a == True):  # here
                        for j in range(self.B):
                            element[i,j] = np.random.randint(0,2)
                        if(self.check_range(self.B2D(element[i])) == True):
                            a = False  # to here
                #print(self.check_range(self.B2D(element[i])))
                #print(self.B2D(element[i]))
                chromosome = list(element[0])
                chrom_list.append(chromosome)
            population.append(chrom_list)
        return population
        
    def B2D(self, pop):
        dec = str(pop[0])+str(pop[1])+str(pop[2])+str(pop[3])+str(pop[4])
        return int(str(dec),2)
    
    def D2B(self, num):
        return [int(i) for i in (bin(10)[2:])]
    
    # Fitness function
    def fun(self, pop):
        X = np.array(pop)
        funsum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(self.D):
            x = X[:,i]
            for j in range(len(x)):
                funsum[j] += self.weight * (self.duration/2) * self.data.iat[x[j], 1]
        for i in range(len(x)):
            funsum[i] = abs(self.calories - funsum[i])
        return funsum

    # Check is the METs in the range or not
    def check_range(self, number):
        if(self.intensity == 'Moderate intensity (from 3.1-6.0 METs)'):
            if(3 < self.data.iat[number, 1] <= 6):
                return True
            else:
                return False
        elif(self.intensity == 'Vigorous intensity (upper 6.0 METs)'):
            if(self.data.iat[number, 1] > 6):
                return True
            else:
                return False
        else:
            return True
    
    # Roulette Wheel Selection
    def Selection(self, pop_bin, fitness):
        select_bin = pop_bin.copy()
        fitness1 = fitness.copy()
        Parents = []
        if sum(fitness1) == 0:
            for i in range(self.n):
                parent = select_bin[random.randint(0,(self.N)-1)]
                Parents.append(parent)
        else: 
            NorParent = [(1 - indivi/sum(fitness1))/((self.N-1)) for indivi in fitness1]
            tep = 0
            Cumulist = []
            for i in range(len(NorParent)):
                tep += NorParent[i]
                Cumulist.append(tep)
            # Find parents
            for i in range(self.n):
                z1 = random.uniform(0,1)
                for pick in range(len(Cumulist)):
                    if z1<=Cumulist[0]:
                        parent = select_bin[NorParent.index(NorParent[0])]
                    elif Cumulist[pick] < z1 <=Cumulist[pick+1]:
                        parent = select_bin[NorParent.index(NorParent[pick+1])]
                Parents.append(parent)
        return Parents
    
    # Crossover & Mutation
    def Crossover_Mutation(self, parent1, parent2):
        def swap_machine(element_1, element_2):
            temp = element_1
            element_1 = element_2
            element_2 = temp
            return element_1, element_2
        child_1 = []
        child_2 = []
        for i in range(len(parent1)):
            # Random a number in 0~1 to decide doing Crossover or not
            z1 = random.uniform(0,1)
            if z1 < self.cr:
                z2 = random.uniform(0,1)
                # Decide a point to do Crossover
                cross_location = math.ceil(z2*(len(parent1[i])-1))
                # Crossover
                parent1[i][:cross_location], parent2[i][:cross_location] = swap_machine(parent1[i][:cross_location], \
                    parent2[i][:cross_location])
                p_list = [parent1[i], parent2[i]]
                # Random a number in 0~1 to decide doing Mutation or not
                for i in range(len(p_list)):
                    # Add a while loop to check the intensity is in the range or not
                    a = True  
                    while(a == True):  
                        z3 = random.uniform(0,1)
                        if z3 < self.mr:
                            # Decide a number to do Mutation
                            z4 = random.uniform(0,1)
                            temp_location = z4*(len(p_list[i])-1)
                            mutation_location = 0 if temp_location < 0.5 else math.ceil(temp_location)
                            p_list[i][mutation_location] = 0 if p_list[i][mutation_location] == 1 else 1
                        if(self.check_range(self.B2D(p_list[i])) == True):
                                a = False
                child_1.append(p_list[0])
                child_2.append(p_list[1])
                
            else:
                child_1.append(parent1[i])
                child_2.append(parent2[i])
        return child_1,child_2

def run_main(weight, intensity, duration, calories):
    ga = GeneticAlgorithm(weight, intensity, duration, calories)
    print(ga.N, ga.D, ga.B)
    pop_bin = ga.generatePopulation()
    pop_dec = []
    for i in range(ga.N):
        chrom_rv = []
        for j in range(ga.D):
            chrom_rv.append(ga.B2D(pop_bin[i][j]))
        pop_dec.append(chrom_rv)
    fitness = ga.fun(pop_dec)
    
    best_fitness = min(fitness)
    arr = fitness.index(best_fitness)
    best_dec = pop_dec[arr]
    
    best_rvlist = []
    best_valuelist = []

    it = 0
    while it < ga.max_iter:
        Parents_list = ga.Selection(pop_bin, fitness)
        Offspring_list = []
        for i in range(int((ga.N-ga.n)/2)):
            candidate = [Parents_list[random.randint(0,len(Parents_list)-1)] for i in range(2)]
            after_cr_mu = ga.Crossover_Mutation(candidate[0], candidate[1])
            offspring1, offspring2 = after_cr_mu[0], after_cr_mu[1]
            Offspring_list.append(offspring1)
            Offspring_list.append(offspring2)

        final_bin = Parents_list + Offspring_list
        final_dec = []
        for i in range(ga.N):
            rv = []
            for j in range(ga.D):
                rv.append(ga.B2D(final_bin[i][j]))
            final_dec.append(rv)

        # Final fitness
        final_fitness = ga.fun(final_dec)

        # Take the best value in this iteration
        smallest_fitness = min(final_fitness)
        index = final_fitness.index(smallest_fitness)
        smallest_dec = final_dec[index]

        # Store the best fitness in the list
        best_rvlist.append(smallest_dec)
        best_valuelist.append(smallest_fitness)

        #Parameters back to the initial
        pop_bin = final_bin 
        pop_dec = final_dec
        fitness = final_fitness

        it += 1
    
    #Store best result
    every_best_value = []
    every_best_value.append(best_valuelist[0])
    for i in range(ga.max_iter-1):
        if every_best_value[i] >= best_valuelist[i+1]:
            every_best_value.append(best_valuelist[i+1])

        elif every_best_value[i] <= best_valuelist[i+1]:
            every_best_value.append(every_best_value[i])

    print('The best fitness: ', min(best_valuelist))
    best_index = best_valuelist.index(min(best_valuelist))
    print('Best item list: ')
    print(best_rvlist[best_index])

    return(min(best_valuelist), best_rvlist[best_index])

if __name__ == '__main__':
    run_main()