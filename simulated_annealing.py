import math
import random
import matplotlib.pyplot as plt
import tsp_utils
import animated_visualizer

class SimulatedAnnealing():
    def __init__(self, coords, temp, alpha, stopping_temp, stopping_iter):
        self.coords = coords
        self.sample_size = len(coords)
        self.temp = temp
        self.alpha = alpha
        self.stopping_temp = stopping_temp
        self.stopping_iter = stopping_iter
        self.iteration = 1

        self.dist_matrix = tsp_utils.vectorToMatrix(coords)
        self.curr_solution = tsp_utils.nearestNeighbourSolution(self.dist_matrix)
        self.best_solution = self.curr_solution

        self.solution_history = [self.curr_solution]

        self.curr_weight = self.weight(self.curr_solution)
        self.initial_weight = self.curr_weight
        self.min_weight = self.curr_weight

        self.weight_list = [self.curr_weight]

        print(self.curr_weight)


    def weight(self, sol):
         return (sum([ self.dist_matrix[sol[i-1]][sol[i]] for i in range(1,self.sample_size)])
                    + self.dist_matrix[sol[0]][sol[self.sample_size-1]])

    ''' Acceptance probability as described in: https://stackoverflow.com/questions/19757551/basics-of-simulated-annealing-in-python '''
    def acceptance_probability(self, candidate_weight):
        return math.exp( -abs(candidate_weight - self.curr_weight) / self.temp)


    '''Accept with probability 1 if candidate is better than current, else accept with probability equal to acceptance_probability() '''
    def accept(self, candidate):
        candidate_weight = self.weight(candidate)
        if candidate_weight < self.curr_weight:
            self.curr_weight = candidate_weight
            self.curr_solution = candidate
            if candidate_weight < self.min_weight:
                self.min_weight = candidate_weight
                self.best_solution = candidate

        else:
            if random.random() < self.acceptance_probability(candidate_weight):
                self.curr_weight = candidate_weight
                self.curr_solution = candidate

    def anneal(self):
        while self.temp >= self.stopping_temp and self.iteration < self.stopping_iter:
            candidate = list(self.curr_solution)
            l = random.randint(2, self.sample_size - 1)
            i = random.randint(0, self.sample_size - l)

            candidate[i : (i+l)] = reversed(candidate[i : (i+l)])
            self.accept(candidate)

            self.temp *= self.alpha
            self.iteration += 1

            self.weight_list.append(self.curr_weight)
            self.solution_history.append(self.curr_solution)


        print('Best fitness obtained: ', self.min_weight)
        print('Improvement over greedy heuristic: ',
                round(( self.initial_weight - self.min_weight) / (self.initial_weight),4) * 100, '%')

    def animateSolutions(self):
        animated_visualizer.animateTSP(self.solution_history, self.coords)

    def plotLearning(self):
        plt.plot([i for i in range(len(self.weight_list))], self.weight_list)
        line_init = plt.axhline(y=self.initial_weight, color='r', linestyle='--')
        line_min = plt.axhline(y=self.min_weight, color='g', linestyle='--')
        plt.legend([line_init, line_min], ['Initial weight', 'Optimized weight'])
        plt.ylabel('Weight')
        plt.xlabel('Iteration')
        plt.show()
