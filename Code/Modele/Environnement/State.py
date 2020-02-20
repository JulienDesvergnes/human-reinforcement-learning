from copy import deepcopy
import numpy as np

class State:

    ## Definition d'un etat de l'environnement ## 
    def __init__(self):
        self.grid_size = 10
        self.x = 5.0 
        self.y = 5.0 
        self.goalx = 7.0 
        self.goaly = 7.0

    ## Normalisation d'un etat ##
    def normalize(self):
        s = deepcopy(self)
        s.x = self.x / self.grid_size
        s.y = self.y / self.grid_size
        s.goalx = self.goalx / self.grid_size
        s.goaly = self.goaly / self.grid_size
        return s

    ## Conversion d'un etat en tableau numpy (pour le replay de l'agent) ##
    def convertInNumpy(self):
        return np.array([self.x, self.y, self.goalx, self.goaly])

