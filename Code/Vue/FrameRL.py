from tkinter import *
import os
from tkinter.messagebox import *
import numpy as np
from Modele.Environnement.Action import int2Action2String1Char
import matplotlib.pyplot as plt

class FrameRL(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameRenforcement = LabelFrame(frame, text = "Renforcement Classique", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameRenforcement.pack(side=LEFT, padx=5, pady=5)

        self.FrameLoadW = LabelFrame(self.FrameRenforcement, text = "Charger des poids", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameLoadW.pack(side=TOP, padx=2, pady=2)

        self.FrameTraining = LabelFrame(self.FrameRenforcement, text = "Lancer entrainement", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameTraining.pack(side=TOP, padx=2, pady=2)

        self.FrameReplayLearningList = LabelFrame(self.FrameRenforcement, text = "Liste simulations", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameReplayLearningList.config(width=250, height=250)
        self.FrameReplayLearningList.pack(side=TOP, padx=5, pady=5, expand=True, fill = BOTH)
        self.FrameReplayLearningList.pack_propagate(0)

        self.FramePredictionMap = LabelFrame(self.FrameRenforcement, text = "Carte de prediction", bg="white", borderwidth=2, relief=GROOVE)
        self.FramePredictionMap.config(width=250, height=250)
        self.FramePredictionMap.pack(side=TOP, padx=5, pady=5, expand=True, fill = BOTH)
        self.FramePredictionMap.pack_propagate(0)

        self.FramePMActions = LabelFrame(self.FrameRenforcement, text = "Actions Prediction Map", bg="white", borderwidth=2, relief=GROOVE)
        self.FramePMActions.pack(side=TOP, padx=2, pady=2)

        ## Charger les poids
        self.loadWeightButton = Button(self.FrameLoadW, text ='Charger poids', command=self.chargerPoidsAction)
        self.loadWeightButton.pack()

        ## Lancer l'entrainement
        self.launchTrainingButton = Button(self.FrameTraining, text ="Lancer l'entrainement !!!", command=self.launchTrainingAction)
        self.launchTrainingButton.pack()

        ## ReplayLearningList
        self.replayLearningList = Listbox(self.FrameReplayLearningList)
        self.replayLearningList.pack(fill =BOTH)
        self.replayLearningList.pack_propagate(0)
        self.replayLearningList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))

        ## PredictionMap
        self.CanvasW = 200
        self.CanvasH = 200
        self.canvasPredictionMap,_ = self.framePrincipale.FrameVisualisation.VisualisationEnvironnementCanvas(self.FramePredictionMap, self.CanvasW, self.CanvasH)
        self.canvasPredictionMap.pack()

        self.calculPredictionMapButton = Button(self.FramePMActions, text ='Calculer Prediction Map', command=self.calulPredictionMap)
        self.calculPredictionMapButton.pack()

    def onselect(self,evt):
        w = evt.widget
        if (len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            value = w.get(index)
            self.replaySimulationQuestion(value)

    def replaySimulationQuestion(self,value):
        if askyesno('Rejouer Simulation', "Rejouer Simulation ?"):
            self.framePrincipale.FrameEcranControle.inSimulation = True
            self.framePrincipale.FrameEcranControle.ResetAction()
            self.framePrincipale.FrameEcranControle.replaySimulationAction(value)
            self.framePrincipale.FrameEcranControle.inSimulation = False

    def chargerPoidsAction(self):
        if (os.path.exists("Weights_Model.wm.index")):
            self.agent.load("Weights_Model.wm")
            showinfo('OK', 'Succesfully loaded !')
        else:
            showinfo('Not OK', 'Failed at loading !')

    def stringfromAccumulateurActions(self):
        s = "Sim " + str(self.replayLearningList.size()) + " : "
        for i in self.framePrincipale.FrameEcranControle.AccumulateurActions:
            s += (int2Action2String1Char(i))
        return s

    def calulPredictionMap(self):
        W = self.CanvasW
        H = self.CanvasH
        gridSize = self.env.state.grid_size
        self.canvasPredictionMap.delete("all")

        # Dessin des contours haut et gauche
        self.canvasPredictionMap.create_line(1, 2, H + 2, 2, fill = 'black')
        self.canvasPredictionMap.create_line(2, 1, 2, W + 2, fill = 'black')

        # Dessin du quadrillage
        for i in range (gridSize):
                self.canvasPredictionMap.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                self.canvasPredictionMap.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')

        for i in range (gridSize) :
            for j in range (gridSize) :
                # Premier coin
                x0 = 1 + (i) * (W + 1) / gridSize
                y0 = 1 + (j) * (H + 1) / gridSize
                if (i == 0):
                    x0 = 3 + (i) * (W + 1) / gridSize
                if (j == 0):
                    y0 = 3 + (j) * (H + 1) / gridSize

                # Deuxieme coin
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize

                # Dessin du bord
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    self.canvasPredictionMap.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        # Dessin du mobile
        x0 = 1 + (self.env.state.x) * (W + 1) / gridSize
        y0 = 1 + (self.env.state.y) * (H + 1) / gridSize
        if (self.env.state.x == 0):
            x0 = 3 + (self.env.state.x) * (W + 1) / gridSize
        if (self.env.state.y == 0):
            y0 = 3 + (self.env.state.y) * (H + 1) / gridSize
        x1 = (self.env.state.x + 1) * (W + 1) / gridSize
        y1 = (self.env.state.y + 1) * (H + 1) / gridSize
        self.canvasPredictionMap.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        # Dessin de l'objectif
        x0 = 1 + (self.env.state.goalx) * (W + 1) / gridSize
        y0 = 1 + (self.env.state.goaly) * (H + 1) / gridSize
        if (self.env.state.goalx == 0):
            x0 = 3 + (self.env.state.goalx) * (W + 1) / gridSize
        if (self.env.state.goaly == 0):
            y0 = 3 + (self.env.state.goaly) * (H + 1) / gridSize
        x1 = (self.env.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.env.state.goaly + 1) * (H + 1) / gridSize
        self.canvasPredictionMap.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")

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
                v = np.array([i / float(self.env.state.grid_size), j / float(self.env.state.grid_size), self.env.state.goalx / float(self.env.state.grid_size), self.env.state.goaly / float(self.env.state.grid_size)])
                v = np.reshape(v,[1,self.env.state_size])
                act_values = self.agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    self.canvasPredictionMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasPredictionMap.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    self.canvasPredictionMap.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    self.canvasPredictionMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasPredictionMap.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    self.canvasPredictionMap.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    self.canvasPredictionMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasPredictionMap.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    self.canvasPredictionMap.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    self.canvasPredictionMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasPredictionMap.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    self.canvasPredictionMap.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')

    def simuPostLearning(self, agent):
        self.env.reset()
        state_size = self.env.state_size
        action_size = self.env.action_size
        #state = np.array([env.state.grid_size, env.state.x, env.state.y, env.state.goalx, env.state.goaly, env.state.bombx, env.state.bomby])
        state = np.array([self.env.state.x / float(self.env.state.grid_size), self.env.state.y/ float(self.env.state.grid_size), self.env.state.goalx/ float(self.env.state.grid_size), self.env.state.goaly/ float(self.env.state.grid_size)])
        state = np.reshape(state,[1,4])
        score_cumul = 0
        for time in range(200):
            act_values = agent.model.predict(state)
            action = np.argmax(act_values[0])
            next_state, reward, done = self.env.step(action)
            score_cumul += reward
            state = next_state * (1/self.env.state.grid_size)
            state = np.reshape(state,[1,4])
            if done:
                break
        return score_cumul

    def launchTrainingAction(self):

        state_size = self.env.state_size
        self.framePrincipale.FrameEcranControle.ResetAction()

        done = False
        batch_size = 3
        Episodes = 20
        scores_app = []
        scores_evo = []

        for e in range(Episodes):
            score_cumul = 0
            state = self.env.reset()
            state = state * (1 / float(self.env.state.grid_size))
            state = np.reshape(state, [1, state_size])
            self.framePrincipale.FrameEcranControle.AccumulateurActions = []

            for time in range(200):

                action = self.agent.act(state)
                next_state, reward, done = self.env.step(action)

                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])

                self.agent.remember(state, action, reward, next_state, done)

                self.framePrincipale.FrameEcranControle.AccumulateurActions.append(action)    

                score_cumul += reward
                state = next_state

                if done:
                    self.replayLearningList.insert(END,self.stringfromAccumulateurActions())
                    print("episode: {}/{}, score: {}, e: {:.5}"
                          .format(e + 1, Episodes, score_cumul, self.agent.epsilon))
                    break
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                    self.agent.memory.clear()
            scores_app.append(score_cumul)
            scores_evo.append(self.simuPostLearning(self.agent))


            #if(e % 15 == 0):
                #self.calculatePredictionMapAction()
                #self.update()

        try:
            self.agent.save("Weights_Model.wm")
        except:
            showinfo('Not OK', 'Failed at saving weight !')

        plt.plot(scores_evo, 'b+')    
        plt.show()   