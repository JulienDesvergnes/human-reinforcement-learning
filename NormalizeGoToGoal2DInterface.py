import random
from enum import Enum
import gym
import numpy as np
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.animation as animation
import time
import os
from PIL import ImageGrab
from copy import deepcopy
        
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999
        self.learning_rate = 0.0001
        self.model = self._build_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(10, input_dim=self.state_size, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(10, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            a = random.randrange(self.action_size)
            return a
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

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

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

class State:
    def __init__(self):
        self.grid_size = 10
        self.x = 5.0 
        self.y = 5.0 
        self.goalx = 7.0 
        self.goaly = 7.0
        #self.bombx = 8 / self.grid_size
        #self.bomby = 2 / self.grid_size

    def normalize(self):
        s = deepcopy(self)
        s.x = self.x / self.grid_size
        s.y = self.y / self.grid_size
        s.goalx = self.goalx / self.grid_size
        s.goaly = self.goaly / self.grid_size
        return s

    def convertInNumpy(self):
        # return np.array([self.grid_size, self.x, self.y, self.goalx, self.goaly, self.bombx, self.bomby])
        return np.array([self.x, self.y, self.goalx, self.goaly])

class Action(Enum):
    Left = 0,
    Right = 1,
    Up = 2,
    Down = 3

def int2Action2String(integer):
    if(integer == 0) : return "LEFT"
    if(integer == 1) : return "RIGHT"
    if(integer == 2) : return "UP"
    if(integer == 3) : return "DOWN"
    print("ERREUR DE CONVERSION : int2Action2String → EXIT")
    exit(0)

def int2Action2String1Char(integer):
    if(integer == 0) : return "L"
    if(integer == 1) : return "R"
    if(integer == 2) : return "U"
    if(integer == 3) : return "D"
    print("ERREUR DE CONVERSION : int2Action2String1Char → EXIT")
    exit(0)

def int2Action(integer):
    if(integer == 0) : return Action.Left
    if(integer == 1) : return Action.Right
    if(integer == 2) : return Action.Up
    if(integer == 3) : return Action.Down
    print("ERREUR DE CONVERSION : int2Action → EXIT")
    exit(0)

class GoToTheGoalEnv2D :

    def __init__(self):
        self.state = State()
        #self.state_size = 7
        self.state_size = 4
        self.action_size = 4
        self.name = "GoToTheGoalEnv2D"
        self.rewardMovement = - 1.0 /  200
        self.rewardWin = 203.0 / 200
        self.rewardLose = - 20.0 / 200
        self.reward = [("rewardMovement",self.rewardMovement), ("rewardWin", self.rewardWin), ("rewardLose", self.rewardLose)]
        self.elemPerso = 0
        self.canvas = 0
        self.canvasMap = 0

    def reset(self):
        self.state = State()
        return self.state.convertInNumpy()

    def step(self, action):
        ## Perform movement
        if(action == 0):
            self.state.x -= 1
        elif(action == 1):
            self.state.x += 1
        elif(action == 2):
            self.state.y -= 1
        elif(action == 3):
            self.state.y += 1
        else:
            self.state.x += 0

        continueP = True
        ## Calculate reward
        mind = 0.001
        #if (abs(self.state.x - self.state.goalx) < mind and abs(self.state.y - self.state.goaly) < mind):
        if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
            r = self.rewardWin
        #elif (self.state.x == self.state.bombx and self.state.y == self.state.bomby):
            #r = -20
        elif( self.state.x <= 0 or self.state.x >= self.state.grid_size - 1 or self.state.y <= 0 or self.state.y >= self.state.grid_size - 1):
            r = self.rewardLose
            continueP = False
            done = True
        else:
            r = self.rewardMovement

        if(continueP):
            ## Verify done
            # or self.state.x == self.state.bombx and self.state.y == self.state.bomby
            if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
                done = True
            else:
                done = False

        return (self.state.convertInNumpy(), r, done)

    def render(self):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                if(self.state.bombx == i and self.state.bomby == j):
                    print("B",end = '')
                elif(self.state.x == i and self.state.y == j):
                    print("X",end = '')
                elif(self.state.goalx == i and self.state.goaly == j):
                    print("G",end = '')
                else:
                    print(" ",end = '')
            print(" ")
        print(" ")

    def showResultsFromLearning(self, agent):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                #v = np.array([self.state.grid_size, i, j, self.state.goalx, self.state.goaly, self.state.bombx, self.state.bomby])
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                actions = agent.model.predict(v)
                print("Position : ", i, "Direction : ", actions)
            

    def writeResultsFromLearning(self, agent, file):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                #v = np.array([self.state.grid_size, i, j, self.state.goalx, self.state.goaly, self.state.bombx, self.state.bomby])
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                actions = agent.model.predict(v)
                file.write("Position : " + str(i) + " Direction : " + str(actions[0][0]) + ", " + str(actions[0][1]) + ", " + str(actions[0][2]) + ", " + str(actions[0][3]) + "\n")
            file.write("\n")

    def majCanvas(self, action):
        W = 400
        H = 400
        gridSize = self.state.grid_size
        x0 = 1 + (self.state.x) * (W + 1) / gridSize
        y0 = 1 + (self.state.y) * (H + 1) / gridSize
        if (self.state.x == 0):
            x0 = 3 + (self.state.x) * (W + 1) / gridSize
        if (self.state.y == 0):
            y0 = 3 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvas.coords(self.elemPerso,x0,y0,x1,y1)

    def drawPath(self,agent):
        self.canvasMap.delete("all")
        W = 200
        H = 200
        gridSize = self.state.grid_size
        self.canvasMap.create_line(1, 2, H + 2, 2, fill = 'black')
        self.canvasMap.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                self.canvasMap.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                self.canvasMap.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add Path
        alreadyDone = []
        px = deepcopy(self.state.x)
        py = deepcopy(self.state.y)
        for i in range(200):
            v = np.array([px / float(self.state.grid_size), py / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
            v = np.reshape(v,[1,self.state_size])
            act_values = agent.model.predict(v)
            action = np.argmax(act_values[0])

            alreadyDone.append((px,py))

            if(action == 0):
                px = px - 1
            if (action == 1):
                px = px + 1
            if(action == 2):
                py = py - 1
            if (action == 3):
                py = py + 1

            if((px,py) not in alreadyDone):
                if (px == 0 or py == 0):
                    x0 = 1 + (px) * (W + 1) / gridSize
                    y0 = 1 + (py) * (H + 1) / gridSize
                if (px == 0):
                    x0 = 3 + (px) * (W + 1) / gridSize
                if (py == 0):
                    y0 = 3 + (py) * (H + 1) / gridSize
                else :
                    x0 = 1 + (px) * (W + 1) / gridSize
                    y0 = 1 + (py) * (H + 1) / gridSize
                x1 = (px + 1) * (W + 1) / gridSize
                y1 = (py + 1) * (H + 1) / gridSize
                self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'PaleGreen2', outline = "")

            if((px < 0) or (px > float(self.state.grid_size)) or (py < 0) or (py > float(self.state.grid_size)) or (px == self.state.goalx and py == self.state.goaly)):
                break


        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')


    def calculatePredictionMapActionFromEnv(self,agent):
        self.canvasMap.delete("all")
        W = 200
        H = 200
        gridSize = self.state.grid_size
        self.canvasMap.create_line(1, 2, H + 2, 2, fill = 'black')
        self.canvasMap.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                self.canvasMap.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                self.canvasMap.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')
        
    def buildCanevas(self,frame) :
        W = 400
        H = 400
        canvas = Canvas(frame, width=W, height=H, background='dark olive green')
        gridSize = self.state.grid_size
        canvas.create_line(1, 2, H + 2, 2, fill = 'black')
        canvas.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                canvas.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                canvas.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    canvas.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.elemPerso = canvas.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        self.canvas = canvas
        return canvas

    def buildCanevasPredictionMap(self, frame, agent):
        W = 200
        H = 200
        canvas = Canvas(frame, width=W, height=H, background='dark olive green')
        gridSize = self.state.grid_size
        canvas.create_line(1, 2, H + 2, 2, fill = 'black')
        canvas.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                canvas.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                canvas.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    canvas.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    canvas.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    canvas.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    canvas.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    canvas.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    canvas.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    canvas.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    canvas.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    canvas.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    canvas.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    canvas.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    canvas.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    canvas.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')
        self.canvasMap = canvas
        return canvas

def simuPostLearning(agent):
    env = GoToTheGoalEnv2D()
    state_size = env.state_size
    action_size = env.action_size
    #state = np.array([env.state.grid_size, env.state.x, env.state.y, env.state.goalx, env.state.goaly, env.state.bombx, env.state.bomby])
    state = np.array([env.state.x / float(env.state.grid_size), env.state.y/ float(env.state.grid_size), env.state.goalx/ float(env.state.grid_size), env.state.goaly/ float(env.state.grid_size)])
    state = np.reshape(state,[1,4])
    score_cumul = 0
    for time in range(200):
        act_values = agent.model.predict(state)
        action = np.argmax(act_values[0])
        next_state, reward, done = env.step(action)
        score_cumul += reward
        state = next_state * (1/env.state.grid_size)
        state = np.reshape(state,[1,4])
        if done:
            break
    return score_cumul

class HRLView(Frame):
	"""docstring for HRLVIEW"""
	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
		

class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, env, agent, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.agent = agent
        self.env = env
        
        fenetre['bg']='white'

        # frame 1
        Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame1.pack(side=LEFT, padx=30, pady=30)

        # frame 2
        Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame2.pack(side=LEFT, padx=10, pady=10)

        # frame 3 dans frame 2
        #Frame3 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        #Frame3.pack(side=RIGHT, padx=5, pady=5)

        # frame 4 dans frame 1
        Frame5 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame5.pack(side=BOTTOM, padx=5, pady=5)

        Frame4 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame4.pack(side=BOTTOM, padx=5, pady=5)

        Frame6 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame6.pack(side=BOTTOM, padx=5, pady=5)

        Frame8 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame8.pack(side=BOTTOM, padx=5, pady=5)

        Frame9 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame9.pack(side=BOTTOM, padx=5, pady=5)

        Frame9tmp = Frame(Frame9, bg="gray", borderwidth=2, relief=FLAT)
        Frame9tmp.pack(side=BOTTOM, padx=5, pady=5)

        Frame10 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame10.config(width=250, height=40)
        Frame10.pack(side=LEFT, padx=5, pady=5, fill =BOTH)
        Frame10.pack_propagate(0)

        Frame12 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame12.pack(side=LEFT, padx=5, pady=5, fill =BOTH)

        Frame11 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame11.config(width=250, height=40)
        Frame11.pack(side=LEFT, padx=5, pady=5, fill =BOTH)
        Frame11.pack_propagate(0)

        Frame7 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame7.pack(side=BOTTOM, padx=5, pady=5)

        Frame14 = Frame(fenetre, bg="seashell3", borderwidth=2, relief=GROOVE)
        Frame14.pack(side=LEFT, padx=5, pady=5)

        Frame17 = Frame(fenetre, bg="mistyrose3", borderwidth=2, relief=GROOVE)
        Frame17.pack(side=LEFT, padx=5, pady=5)

        Frame24 = Frame(fenetre, bg="mistyrose2", borderwidth=2, relief=GROOVE)
        Frame24.pack(side=LEFT, padx=5, pady=5)

        Frame15 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        Frame15.config(width=250, height=250)
        Frame15.pack(side=BOTTOM, padx=5, pady=5, expand=True, fill =BOTH)
        Frame15.pack_propagate(0)

        Frame16 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        Frame16.config(width=200, height=75)
        Frame16.pack(side=BOTTOM, padx=5, pady=5)
        Frame16.pack_propagate(0)

        self.Frame13 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        self.Frame13.pack(side=BOTTOM, padx=5, pady=5)

        Frame21 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame21.pack(side=BOTTOM, padx=5, pady=5)

        Frame23 = LabelFrame(Frame21, text = "Actions", bg="white", borderwidth=2, relief=GROOVE)
        Frame23.pack(side=BOTTOM, padx=5, pady=5, fill="both", expand="yes")

        Frame22 = LabelFrame(Frame21, bg="white", borderwidth=2, relief=GROOVE)
        Frame22.pack(side=BOTTOM, padx=5, pady=5, fill="both", expand="yes")

        Frame19 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame19.config(width=250, height=80)
        Frame19.pack(side=BOTTOM, padx=5, pady=5, fill =BOTH)
        Frame19.pack_propagate(0)

        Frame20 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame20.config(width=250, height=250)
        Frame20.pack(side=BOTTOM, padx=5, pady=5, fill =BOTH)
        Frame20.pack_propagate(0)

        Frame18 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame18.config(width=250, height=150)
        Frame18.pack(side=BOTTOM, padx=5, pady=5 ,fill =BOTH)
        Frame18.pack_propagate(0)


        # Ajout de labels
        Label(Frame1, text="Description").pack(padx=10, pady=10)
        Label(Frame2, text="Simulation").pack(padx=10, pady=10)
        # Label(Frame3, text="Frame 3",bg="white").pack(padx=10, pady=10)
        Label(Frame4, text="Agent",bg="white").pack(padx=10, pady=10)
        Label(Frame5, text="Network",bg="white").pack(padx=10, pady=10)
        Label(Frame6, text="Environment : " + env.name,bg="white").pack(padx=10, pady=10)
        Label(Frame7, text="Visualization : " + env.name,bg="white").pack(padx=10, pady=10)
        Label(Frame8, text="Control Movement : ",bg="white").pack(padx=10, pady=10)
        Label(Frame9, text="Evolution of State",bg="white").pack(padx=10, pady=10)
        Label(Frame10, text="Previous state",bg="white").pack(padx=10, pady=10)
        Label(Frame11, text="Current state",bg="white").pack(padx=10, pady=10)
        Label(Frame12, text="→→ Action Performed →→",bg="white").pack(padx=10, pady=10)
        Label(self.Frame13, text="Cumulative Reward",bg="white").pack(padx=10, pady=10)
        Label(Frame14, text="Control Screen",bg="seashell3").pack(padx=10, pady=10)
        Label(Frame15, text="Simulation list",bg="white").pack(padx=10, pady=10)
        Label(Frame16, text="Reset Simulation",bg="white").pack(padx=10, pady=10)
        Label(Frame17, text="RL Screen",bg="mistyrose3").pack(padx=10, pady=10)
        Label(Frame18, text="Predict Action From State",bg="white").pack(padx=10, pady=10)
        Label(Frame19, text="Launch Traning",bg="white").pack(padx=10, pady=10)
        Label(Frame20, text="Learning list",bg="white").pack(padx=10, pady=10)
        Label(Frame21, text="Prediction Map",bg="white").pack(padx=10, pady=10)
        Label(Frame24, text="HRL Screen",bg="mistyrose2").pack(padx=10, pady=10)

        # Descriptif agent
        s = "State size / Input size = " + str(self.env.state_size) + " \n" + \
        "Action size / Output size = " + str(self.env.action_size) + " \n" + \
        "Memory = deque(" + str(self.agent.memory.maxlen) + ") \n" + \
        "Discount rate (gamma) = " + str(self.agent.gamma) + " \n" + \
        "Exploration rate (epsilon) = " + str(self.agent.epsilon) + " \n" + \
        "Exploration rate minimum = " + str(self.agent.epsilon_min) + "\n" + \
        "Exploration rate decay = " + str(self.agent.epsilon_decay) + "\n" + \
        "Learning rate (alpha) = " + str(self.agent.learning_rate) + " \n"

        # Descriptif NN
        bagent = Label(Frame4, text=s, bg="white", justify="left")
        bagent.pack()
        config = self.agent.model.get_config()
        k,v = config.items()
        net = "Input Layer : " + str(v[1][0].get('config').get('batch_input_shape')[1]) + "\n"
        for i in range (len(v[1])):
            name = str((v[1][i].get('class_name')))
            nb_neural  = str((v[1][i].get('config').get('units')))
            factivation = str((v[1][i].get('config').get('activation')))
            net = net + "Hidden Layer " + str(i+1) + " : " + name + " " + nb_neural + \
            " - Activation = " + factivation + "\n"
        
        network = Label(Frame5, text=net, bg="white", justify="left")
        network.pack()

        # Descriptif Env
        s = ""
        for n,v in env.reward :
            s += n + " : " + str(v) + "\n"
        envText = Label(Frame6, text=s, bg="white", justify="left")
        envText.pack()

        # Visualisation Env
        self.canvas = env.buildCanevas(Frame7)
        self.canvas0 = self.canvas
        self.canvas.pack()

        ### Simulation
        # Touches directionnelles
        self.upButton = Button(Frame8, text="UP ↑", command=self.UpAction)
        self.upButton.pack(side="left")

        self.downButton = Button(Frame8, text="DOWN ↓", command=self.DownAction)
        self.downButton.pack(side="left")

        self.leftButton = Button(Frame8, text="LEFT ←", command=self.LeftAction)
        self.leftButton.pack(side="left")

        self.rightButton = Button(Frame8, text="RIGHT →", command=self.RightAction)
        self.rightButton.pack(side="left")
        
        self.previousStateLabel = StringVar()
        self.previousStateLabel.set("                                       ")
        self.labelps = Label(Frame10, textvariable=self.previousStateLabel, bg="white", justify="left")
        self.labelps.pack()

        self.currentStateLabel = StringVar()
        self.currentStateLabel.set("Position du mobile de déplacement : (" + str(env.state.x + 1) + ", " + str(env.state.y + 1) + ")")
        self.labelcps = Label(Frame11, textvariable=self.currentStateLabel, bg="white", justify="left")
        self.labelcps.pack()

        self.actionperformedlabel = StringVar()
        self.actionperformedlabel.set("No action FTM")
        self.labelapl = Label(Frame12, textvariable=self.actionperformedlabel, bg="white", justify="left")
        self.labelapl.pack()

        self.rewardObtenue = StringVar()
        self.rewardObtenue.set("No reward FTM")
        self.labelrwl = Label(Frame12, textvariable=self.rewardObtenue, bg="white", justify="left")
        self.labelrwl.pack()

        self.figurecr = Figure(figsize=(4,3), dpi=100)
        self.figuresubplotcr = self.figurecr.add_subplot(111)

        self.indicesFigures = [0]
        self.scoreCumule = [0]
        self.actionSequence = []

        self.canvasFigure = FigureCanvasTkAgg(self.figurecr, self.Frame13)
        self.canvasFigure.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True) 

        self.replayGamesList = Listbox(Frame15)
        self.replayGamesList.pack(fill =BOTH)
        self.replayGamesList.pack_propagate(0)
        self.replayGamesList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))

        self.resetSimuButton = Button(Frame16, text ='RESET', command=self.resetRender)
        self.resetSimuButton.pack()

        self.launchTrainingButton = Button(Frame19, text ='GOGOGO !!!', command=self.launchTrainingAction)
        self.launchTrainingButton.pack(side="bottom")

        self.replayGamesLearningList = Listbox(Frame20)
        self.replayGamesLearningList.pack(fill =BOTH)
        self.replayGamesLearningList.pack_propagate(0)
        self.replayGamesLearningList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))
    
        self.inReplayMode = False

        self.calculatePredictionMapButton = Button(Frame23, text ='Calculate Map', command=self.calculatePredictionMapAction)
        self.calculatePredictionMapButton.pack(side="left")

        self.savePredictionMapButton = Button(Frame23, text ='Save Map', command=self.saveAction)
        self.savePredictionMapButton.pack(side="left")

        self.drawPathButton = Button(Frame23, text ='Draw Path', command=self.drawPathAction)
        self.drawPathButton.pack(side="left")

        self.loadWeightButton = Button(Frame18, text ='Load Weights', command=self.loadWeightAction)
        self.loadWeightButton.pack(side="left")

        self.canvasPredictionMap = env.buildCanevasPredictionMap(Frame22, self.agent)
        self.canvasPredictionMap.pack()

        self.OpenHRLView = Button(Frame24, text ='OpenHRLView', command=self.OpenHRLViewAction)
        self.OpenHRLView.pack()

    def OpenHRLViewAction(self):
    	self.HRLFenetre = Tk()
    	self.HRLFenetre.title('HRL View')

    	self.HRLFrame = HRLView(self.HRLFenetre)
    	self.HRLFrame.mainloop()


    def loadWeightAction(self):
        self.agent.load("Weights_Model.wm")
        showinfo('OK', 'Succesfully loaded !')

    def drawPathAction(self):
        self.env.drawPath(self.agent)

    def saveAction(self, path ="PredictionMap.png"):
        x=self.canvasPredictionMap.winfo_rootx()
        y=self.canvasPredictionMap.winfo_rooty()
        x1=x+self.canvasPredictionMap.winfo_width()
        y1=y+self.canvasPredictionMap.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("PredictionMap.png")

    def onselect(self,evt):
        w = evt.widget
        if (len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            value = w.get(index)
            print("You selected " + str(index) + ", " + str(value))
            self.replaySimulationQuestion(value)

    def calculatePredictionMapAction(self):
        self.env.calculatePredictionMapActionFromEnv(self.agent)

    def replaySimulationAction(self,value):
        deltaTime = 0.5
        for c in value:
            if(c == "R"):
                self.RightAction()
            if(c == "D"):
                self.DownAction()
            if(c == "U"):
                self.UpAction()
            if(c == "L"):
                self.LeftAction()
            self.update()
            time.sleep(deltaTime)

    def replaySimulationQuestion(self,value):
        if askyesno('Replay Simulation', "Replay Simulation ?"):
            #r = Replayeur(self,value)
            #r.start()
            self.inReplayMode = True
            self.resetRender()
            self.rewardObtenue.set("")
            self.actionperformedlabel.set("")
            self.currentStateLabel.set("")
            self.replaySimulationAction(value)
            self.inReplayMode = False

    def resetRender(self):
        self.indicesFigures = [0]
        self.scoreCumule = [0]
        self.actionSequence = []
        self.rewardObtenue.set("No reward FTM")
        self.actionperformedlabel.set("No action FTM")
        self.env.state.x = 5.0
        self.env.state.y = 5.0
        self.env.majCanvas(0)
        self.previousStateLabel.set("                                       ")
        self.currentStateLabel.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.figuresubplotcr.clear()
        self.figuresubplotcr.plot(self.indicesFigures, self.scoreCumule)
        self.canvasFigure.draw()


    def MajRewardCumules(self,reward):
        self.scoreCumule.append(self.scoreCumule[-1] + reward)
        self.indicesFigures.append(self.indicesFigures[-1] + 1)
        self.figuresubplotcr.clear()
        self.figuresubplotcr.plot(self.indicesFigures, self.scoreCumule)
        self.canvasFigure.draw()

    def MajLabels(self,noAction):
        next_state, reward, done = self.env.step(noAction)
        self.MajRewardCumules(reward)
        self.env.majCanvas(noAction)
        self.previousStateLabel.set(self.currentStateLabel.get())
        self.currentStateLabel.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.actionperformedlabel.set(int2Action2String(noAction))
        self.rewardObtenue.set(str(reward))
        self.actionSequence.append(noAction)
        if (done and not self.inReplayMode):
            self.replayGamesList.insert(END,self.stringfromActionSequence(False))
            self.resetRender()
            
    def stringfromActionSequence(self,train):
        s = "Sim " + str(self.replayGamesList.size()) + " : "
        if (train):
            s = "Sim " + str(self.replayGamesLearningList.size()) + " : "
        for i in self.actionSequence:
            s += (int2Action2String1Char(i))
        return s

    def UpAction(self):
        self.MajLabels(2)
    def DownAction(self):
        self.MajLabels(3)
    def LeftAction(self):
        self.MajLabels(0)
    def RightAction(self):
        self.MajLabels(1)

    def launchTrainingAction(self):

        state_size = self.env.state_size
        self.resetRender()

           #try:
        #    self.agent.load("Weights_Model.wm")
        #except:
        #    print("ERROR launchTrainingAction : LOAD MODEL WEIGHT")

        if (os.path.exists("Weights_Model.wm")):
            self.agent.load("Weights_Model.wm")

        done = False
        batch_size = 2
        Episodes = 50
        scores_app = []
        scores_evo = []

        #filename = "predictions.txt"
        #filename_scores = "scores.txt"
        #myfile = open(filename, 'w')
        #myfile_scores = open(filename_scores, 'w')
        #self.env.writeResultsFromLearning(self.agent, myfile)

        for e in range(Episodes):
            score_cumul = 0
            state = self.env.reset()
            state = state * (1 / float(self.env.state.grid_size))
            state = np.reshape(state, [1, state_size])
            self.indicesFigures = [0]
            self.scoreCumule = [0]
            self.actionSequence = []

            #print("### DEBUT EPOQUE " + str(e) + " ###")
            for time in range(200):
                # env.render()
                #print("POSITION JOUEUR " + str(env.state.x) + ", " + str(env.state.y) + " --- POSITION CIBLE " + str(env.state.goalx) + ", " + str(env.state.goaly))
                action = self.agent.act(state)
                #print("ACTION CHOISIE : " + str(action))
                next_state, reward, done = self.env.step(action)
                self.scoreCumule.append(self.scoreCumule[-1] + reward)
                self.indicesFigures.append(self.indicesFigures[-1] + 1)
                self.rewardObtenue.set(str(reward))
                self.actionSequence.append(action)    
                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])
                self.agent.remember(state, action, reward, next_state, done)
                score_cumul += reward
                #print("REWARD " + str(reward) + " --- CUMUL_REWARD " + str(score_cumul))
                state = next_state
                if done:
                    self.replayGamesLearningList.insert(END,self.stringfromActionSequence(True))
                    print("episode: {}/{}, score: {}, e: {:.5}"
                          .format(e + 1, Episodes, score_cumul, self.agent.epsilon))
                    break
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                    self.agent.memory.clear()
            scores_app.append(score_cumul)
            scores_evo.append(simuPostLearning(self.agent))
            # # # # env.writeResultsFromLearning(agent, myfile)
            #myfile_scores.write(str(scores_evo[-1]) + "\n")
            #myfile_scores.flush()

            if(e % 15 == 0):
                self.calculatePredictionMapAction()
                self.update()
        #myfile.close()

        try:
            self.agent.save("Weights_Model.wm")
        except:
            print("ERROR launchTrainingAction : SAVE MODEL WEIGHT")

        plt.plot(scores_evo, 'b+')    
        plt.show()    

if __name__ == "__main__":

    fenetre = Tk()
    fenetre.title('Interface HRL')

    env_ = GoToTheGoalEnv2D()
    state_size = env_.state_size
    action_size = env_.action_size
    agent_ = DQNAgent(state_size, action_size)

    interface = Interface(fenetre, env_, agent_)
    interface.mainloop()