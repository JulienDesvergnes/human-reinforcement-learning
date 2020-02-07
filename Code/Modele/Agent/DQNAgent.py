from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

import numpy as np
import random

class DQNAgent:

    ## Initialisation des parametres du reseau ##
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 0.5  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.5 #0.999
        self.learning_rate = 0.0001
        self.model = self._build_model()

    ## Initialisation des differentes couches du reseau ##
    def _build_model(self):
        model = Sequential()
        model.add(Dense(10, input_dim=self.state_size, activation='relu'))
        #model.add(Dense(10, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    ## Fonction de sauvegarde d'un 4-uplet dans la memoire de replay ##
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    ## Choisis une action a effectuer sur l'environnement ##
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            a = random.randrange(self.action_size)
            return a
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    ## Etape d'apprentissage ##
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    ## Chargement des poids ##
    def load(self, name):
        self.model.load_weights(name)

    ## Sauvegarde des poids ##
    def save(self, name):
        self.model.save_weights(name)