import numpy as np
import random

class Neural:

    def __init__(self, genome):

        # One Hidden Layer Model consists of (3, 6, 1) plus bias terms

        self.INPUT_LAYER = 3
        self.HIDDEN_LAYER = 6
        self.OUTPUT_LAYER = 1

        self.w1 = np.random.uniform(-1,1,(self.HIDDEN_LAYER, self.INPUT_LAYER + 1))
        self.w2 = np.random.uniform(-1,1,(self.OUTPUT_LAYER,self.HIDDEN_LAYER + 1))

        if genome is not None:

            self.decode(genome)

    def __sigmoid(self, z):

        return 1/(1 + np.exp(-1*z))


    def __regularize(self, input):

        sumVal = np.sum(abs(input))

        for val in input:

            if sumVal == 0:
                val[0] = 0
            else:
                val[0] = val[0]/sumVal


    # Input must be of shape (3,1)
    def feedforward(self,input):

        # Regularize  the Input for val to be between -1 to 1
        self.__regularize(input)

        # Add bias term for functionality changes shape to (4,1)
        input_new = np.concatenate((np.array([[1]]), input), axis = 0)
        hidden_layer = self.w1@input_new

        hidden_layer = self.__sigmoid(hidden_layer)
        hidden_layer_new =  np.concatenate((np.array([[1]]), hidden_layer), axis = 0)

        output_layer = self.w2@hidden_layer_new

        return self.__sigmoid(output_layer)

    # Convert complete two matrix of weights in single list
    def encode(self):

        flat_list = self.w1.flatten()
        flat_list = flat_list.tolist()

        out_list = self.w2.flatten().tolist()

        flat_list.extend(out_list)

        return flat_list

    # Convert back list to two matrix
    def decode(self, genome):

        for i in range(self.HIDDEN_LAYER):
            for j in range(self.INPUT_LAYER + 1):
                self.w1[i][j] = genome[i*(self.INPUT_LAYER + 1) + j]

        for i in range(self.OUTPUT_LAYER):
            for j in range(self.HIDDEN_LAYER + 1):
                self.w2[i][j] = genome[(i*(self.HIDDEN_LAYER + 1)) + j + self.HIDDEN_LAYER*(self.INPUT_LAYER+1)]


    # This takes Neural object list as input and create new eltie birds
    @classmethod
    def selection(cls,neural_list):

        SELECTION_PERCENTAGE = 0.04
        POPULATION = 250

        elite_birds_copy = []
        elite_birds = neural_list[0:round(SELECTION_PERCENTAGE*POPULATION)]

        # Get elite birds and ecode their weights and insert it to copy
        for bird in elite_birds:
            gen = bird.encode()
            elite_birds_copy.append(Neural(gen))

        return elite_birds_copy

    @classmethod
    def mutation(cls,neural_object):

        MUTATION_RATE = 0.04
        gen = neural_object.encode()

        for i in range(len(gen)):
            if np.random.rand(0,100) < MUTATION_RATE*100:
                gen[i] = np.random.uniform(-1,1)

        new_object = Neural(gen)

        return new_object

    @classmethod
    def crossover(cls,object1, object2):

        CROSSOVER_RATE = 0.04
        gen1 = object1.encode()
        gen2 = object2.encode()

        for val in range(len(gen1)):
            if np.random.rand(0,100) < CROSSOVER_RATE*100:
                gen1[val], gen2[val] = gen2[val], gen1[val]

        return [Neural(gen1), Neural(gen2)]

    @classmethod
    def create_new_generation(cls, neural_list):

        MUTATION_RATE = 0.04
        CROSSOVER_RATE = 0.04
        POPULATION = 250
        new_generation = []

        elite_neural = Neural.selection(neural_list)
        new_generation.extend(elite_neural)

        # Apply Mutation for some birds
        for i in range(round(MUTATION_RATE*100/POPULATION)):
            new_generation.append(Neural.mutation(neural_list[i]))

        # Apply Crossover
        for i in range(round((MUTATION_RATE * 100 / POPULATION)),
                       round(((MUTATION_RATE * 100 / POPULATION) + (CROSSOVER_RATE * 100 / POPULATION)))):
            new_generation.append(Neural.crossover(neural_list[i], elite_neural[random.randint(0,len(elite_neural) -1)])[0])

        for i in range(POPULATION - len(new_generation)):
            new_generation.append(Neural(None))

        return new_generation
