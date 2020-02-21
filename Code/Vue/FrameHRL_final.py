from tkinter import *
import os
from tkinter.messagebox import *
import numpy as np
from Modele.Environnement.Action import int2Action2String1Char
import matplotlib.pyplot as plt
from Modele.Environnement.Environnement import GoToTheGoalEnv2D
import time as tm

class FrameHRL_final(Frame):
    
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

        # self.FrameReplayLearningList = LabelFrame(self.FrameRenforcement, text = "Liste simulations", bg="white", borderwidth=2, relief=GROOVE)
        # self.FrameReplayLearningList.config(width=250, height=250)
        # self.FrameReplayLearningList.pack(side=TOP, padx=5, pady=5, expand=True, fill = BOTH)
        # self.FrameReplayLearningList.pack_propagate(0)

        self.FramePredictionMap = LabelFrame(self.FrameRenforcement, text = "Carte de prediction", bg="white", borderwidth=2, relief=GROOVE)
        self.FramePredictionMap.config(width=250, height=250)
        # self.FramePredictionMap.pack(side=TOP, padx=5, pady=5, expand=True, fill = BOTH)
        # self.FramePredictionMap.pack_propagate(0)

        self.FramePMActions = LabelFrame(self.FrameRenforcement, text = "Actions Prediction Map", bg="white", borderwidth=2, relief=GROOVE)
        self.FramePMActions.pack(side=TOP, padx=2, pady=2)

        self.FrameHumanAction = LabelFrame(self.FrameRenforcement, text = "Human Action", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameHumanAction.config(width=150, height=150)
        self.FrameHumanAction.pack(side=TOP, padx=5, pady=5)

        self.var = DoubleVar()
        self.HumanActionButton1 = Button(self.FrameHumanAction, text='Oui', command=lambda: self.var.set(1))
        self.HumanActionButton2 = Button(self.FrameHumanAction, text='Non', command=lambda: self.var.set(2))
        self.HumanActionButton3 = Button(self.FrameHumanAction, text='JSP', command=lambda: self.var.set(3))
        # HumanActionButton.place(x=75,y=1)
        # HumanActionButton.place(x=75,y=5)
        # HumanActionButton.place(x=75,y=30)
        self.HumanActionButton1.grid(row=0, column=0, sticky="nsew",padx=5, pady=5)
        self.HumanActionButton2.grid(row=0, column=2, sticky="nsew",padx=5, pady=5)
        self.HumanActionButton3.grid(row=0, column=4, sticky="nsew",padx=5, pady=5)


        self.FrameResetParam = LabelFrame(self.FrameRenforcement, text="Reset Parametres", bg="white", borderwidth=2,relief=GROOVE)
        self.FrameResetParam.config(width=150, height=150)
        self.FrameResetParam.pack(side=TOP, padx=5, pady=5)
        self.ResetButton = Button(self.FrameResetParam, text='Reset Epsilon', command=self.resetAction)
        self.ResetButton.pack()


        ## Charger les poids
        # self.loadWeightButton = Button(self.FrameLoadW, text ='Charger poids', command=self.chargerPoidsAction)
        # self.loadWeightButton.pack()

        ## Lancer l'entrainement
        self.launchTrainingButton = Button(self.FrameTraining, text ="Lancer l'entrainement !!!", command=self.launchTrainingAction)
        self.launchTrainingButton.pack()

        ## ReplayLearningList
        # self.replayLearningList = Listbox(self.FrameReplayLearningList)
        # self.replayLearningList.pack(fill =BOTH)
        # self.replayLearningList.pack_propagate(0)
        # self.replayLearningList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))
        # scrollbar = Scrollbar(self.replayLearningList,orient="vertical")
        # self.replayLearningList.yscrollcommand = scrollbar.set
        # scrollbar.pack(side="right", fill="y")

        ## PredictionMap
        self.CanvasW = 200
        self.CanvasH = 200
        self.canvasPredictionMap,_ = self.framePrincipale.FrameVisualisation.VisualisationEnvironnementCanvas(self.FramePredictionMap, self.CanvasW, self.CanvasH)
        self.canvasPredictionMap.pack()

        self.calculPredictionMapButton = Button(self.FramePMActions, text ='Calculer Prediction Map', command=self.calulPredictionMap)
        self.calculPredictionMapButton.pack()

        FrameQValuesAnt = LabelFrame(self.FrameRenforcement, text = "Q-values avant récompense humaine", bg="white", borderwidth=2, relief=GROOVE)
        FrameQValuesAnt.pack(side=TOP, padx=5, pady=5)

        FrameQValuesPost = LabelFrame(self.FrameRenforcement, text="Q-values après récompense humaine", bg="white", borderwidth=2,relief=GROOVE)
        FrameQValuesPost.pack(side=BOTTOM, padx=5, pady=5)

        FrameQHautAnt = LabelFrame(FrameQValuesAnt, text="Action Haute", bg="white", borderwidth=2,relief=GROOVE)
        FrameQHautPost = LabelFrame(FrameQValuesPost, text="Action Haute", bg="white", borderwidth=2,relief=GROOVE)

        FrameQGaucheAnt = LabelFrame(FrameQValuesAnt, text="Action Gauche", bg="white", borderwidth=2, relief=GROOVE)
        FrameQGauchePost = LabelFrame(FrameQValuesPost, text="Action Gauche", bg="white", borderwidth=2, relief=GROOVE)

        FrameQDroiteAnt = LabelFrame(FrameQValuesAnt, text="Action Droite", bg="white", borderwidth=2, relief=GROOVE)
        FrameQDroitePost = LabelFrame(FrameQValuesPost, text="Action Droite", bg="white", borderwidth=2, relief=GROOVE)

        FrameQBasAnt = LabelFrame(FrameQValuesAnt, text="Action Bas", bg="white", borderwidth=2, relief=GROOVE)
        FrameQBasPost = LabelFrame(FrameQValuesPost, text="Action Bas", bg="white", borderwidth=2, relief=GROOVE)

        FrameQHautAnt.grid(row=0, column=1, sticky="nsew")
        FrameQHautPost.grid(row=0, column=1, sticky="nsew")
        FrameQGaucheAnt.grid(row=1, column=0, sticky="nsew")
        FrameQGauchePost.grid(row=1, column=0, sticky="nsew")
        FrameQDroiteAnt.grid(row=1, column=2, sticky="nsew")
        FrameQDroitePost.grid(row=1, column=2, sticky="nsew")
        FrameQBasAnt.grid(row=2, column=1, sticky="nsew")
        FrameQBasPost.grid(row=2, column=1, sticky="nsew")

        self.QHautAnt = StringVar()
        self.QGaucheAnt = StringVar()
        self.QDroiteAnt = StringVar()
        self.QBasAnt = StringVar()
        self.QHautPost = StringVar()
        self.QGauchePost = StringVar()
        self.QDroitePost = StringVar()
        self.QBasPost = StringVar()
        
        self.QHautAnt.set(" Q Haut : ")
        Label(FrameQHautAnt, textvariable=self.QHautAnt, bg="white", justify="left").pack()
        self.QGaucheAnt.set(" Q Gauche : ")
        Label(FrameQGaucheAnt, textvariable=self.QGaucheAnt, bg="white", justify="left").pack()
        self.QDroiteAnt.set(" Q Droite : ")
        Label(FrameQDroiteAnt, textvariable=self.QDroiteAnt, bg="white", justify="left").pack()
        self.QBasAnt.set(" Q Bas : ")
        Label(FrameQBasAnt, textvariable=self.QBasAnt, bg="white", justify="left").pack()
        self.QHautPost.set(" Q Haut : ")
        Label(FrameQHautPost, textvariable=self.QHautPost, bg="white", justify="left").pack()
        self.QGauchePost.set(" Q Gauche : ")
        Label(FrameQGauchePost, textvariable=self.QGauchePost, bg="white", justify="left").pack()
        self.QDroitePost.set(" Q Droite : ")
        Label(FrameQDroitePost, textvariable=self.QDroitePost, bg="white", justify="left").pack()
        self.QBasPost.set(" Q Bas : ")
        Label(FrameQBasPost, textvariable=self.QBasPost, bg="white", justify="left").pack()

    def resetAction(self) :
        self.agent.epsilon = 1.0

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
        # print("accumulateur d'actions ", self.framePrincipale.FrameEcranControle.AccumulateurActions)
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

    def simuPostLearning(self,agent):
        state_size = self.envPost.state_size
        action_size = self.envPost.action_size
        state = self.envPost.reset()
        state = state * (1 / float(self.envPost.state.grid_size))
        state = np.reshape(state, [1, state_size])
        score_cumul = 0
        for time in range(200):
            act_values = agent.model.predict(state)
            action = np.argmax(act_values[0])
            next_state, reward, done = self.envPost.step(action)
            score_cumul += reward
            state = next_state * (1 / self.envPost.state.grid_size)
            state = np.reshape(state, [1, 4])
            if done :
                return score_cumul
        return score_cumul

    def distance(self,a):
        return (a[0,0]-a[0,2])**2 + (a[0,1]-a[0,3])**2

    def launchTrainingAction(self):

        self.envPost = GoToTheGoalEnv2D()
        state_size = self.env.state_size
        self.framePrincipale.FrameEcranControle.ResetAction()

        done = False
        batch_size = 2
        Episodes = 200
        scores_app = []
        scores_evo = []

        for e in range(Episodes):
            score_cumul = 0
            state = self.env.reset()
            state = state * (1 / float(self.env.state.grid_size))
            state = np.reshape(state, [1, state_size])
            self.framePrincipale.FrameEcranControle.AccumulateurActions = []
            AccumulateurActionsRL = []
            for time in range(200):
                action = self.agent.act(state)
                predictions = self.agent.model.predict(state)
                next_state, reward, done = self.framePrincipale.FrameVisualisation.FrameVisualisationControles.UpdateAll(action)
                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])

                #next_state, reward, done = self.env.step(action)
                if not done :
                    AccumulateurActionsRL = self.framePrincipale.FrameEcranControle.AccumulateurActions

                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])

                #self.framePrincipale.FrameEcranControle.AccumulateurActions.append(action)

                if done:
                    self.agent.remember(state, action, reward, next_state, done)
                    score_cumul += reward
                    self.framePrincipale.FrameEcranControle.AccumulateurActions = AccumulateurActionsRL
                    # self.replayLearningList.insert(END, self.stringfromAccumulateurActions())
                    # print("episode: {}/{}, score: {}, e: {:.5}".format(e + 1, Episodes, score_cumul, self.agent.epsilon))
                    break

                # self.var.set(0)
                # self.HumanActionButton1.wait_variable(self.var)
                #

                # Juge
                reward_human = 0
                if (self.distance(next_state) < self.distance(state)) :
                    reward_human =  10 / 200
                else :
                    reward_human = -6 / 200

                # reward_human = 0
                # if self.var.get() == 1 :
                #     reward_human  = 10/200
                # elif self.var.get() == 2 :
                #     reward_human = -5/200
                # elif self.var.get() == 3 :
                #     reward_human = 0

                # Mise à jour du score courant dans l'interface

                self.framePrincipale.FrameEcranControle.AjouteScore(reward_human)

                reward += reward_human
                score_cumul += reward
                self.agent.remember(state, action, reward, next_state, done)

                old_state = state
                state = next_state

                # Apprentissage
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                    # self.agent.memory.clear()


                # Q-values for old state before human reward
                self.QGaucheAnt.set(" Q Gauche : " + str(predictions[0][0])[:5])
                self.QDroiteAnt.set(" Q Droite : " + str(predictions[0][1])[:5])
                self.QHautAnt.set(" Q Haut : " + str(predictions[0][2])[:5])
                self.QBasAnt.set(" Q Bas : " + str(predictions[0][3])[:5])

                # # Q-values for old state after human reward
                self.QGauchePost.set(" Q Gauche : " + str(self.agent.model.predict(old_state)[0][0])[:5])
                self.QDroitePost.set(" Q Droite : " + str(self.agent.model.predict(old_state)[0][1])[:5])
                self.QHautPost.set(" Q Haut : " + str(self.agent.model.predict(old_state)[0][2])[:5])
                self.QBasPost.set(" Q Bas : " + str(self.agent.model.predict(old_state)[0][3])[:5])

                self.framePrincipale.update()

                # print("predictions avant : ",predictions)
                # print("predictions après : ",self.agent.model.predict(old_state))

                tm.sleep(3.0)




            scores_app.append(score_cumul)
            scores_evo.append(self.simuPostLearning(self.agent))

            #if(e % 15 == 0):
                #self.calculatePredictionMapAction()
                #self.update()

        try:
            self.agent.save("Weights_Model.wm")
        except:
            showinfo('Not OK', 'Failed at saving weight !')

        plt.plot(scores_app, 'g')
        plt.plot(scores_evo, 'b')
        plt.show()