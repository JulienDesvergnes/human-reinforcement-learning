from tkinter import *
import os
from tkinter.messagebox import *
import numpy as np
from Modele.Environnement.Action import int2Action2String1Char
from Modele.Environnement.Action import int2Action2String


class FrameHRL(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        # definition des differentes frames incluses dans la frame HRL
        self.FrameHumanDecision = LabelFrame(frame, text = "Human Decision for HRL", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameHumanDecision.pack(side=RIGHT, padx=5, pady=5)

        #bouton Launch HRL
        LaunchHRLButton = Button(self.FrameHumanDecision, text='Launch Human Learning', command = self.launchHRLAction)
        LaunchHRLButton.grid(row=1, column=1, sticky="nsew")

        self.FrameReplayLearningList = LabelFrame(self.FrameHumanDecision, text = "Liste simulations", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameReplayLearningList.config(width=250, height=250)
        #self.FrameReplayLearningList.pack(side=TOP, padx=5, pady=5, expand=True) #, fill = BOTH)
        #self.FrameReplayLearningList.pack_propagate(0)

        ## ReplayLearningList
        self.replayLearningList = Listbox(self.FrameReplayLearningList)
        self.replayLearningList.pack(fill =BOTH)
        self.replayLearningList.pack_propagate(0)
        self.replayLearningList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))

    def onselect(self,evt):
        w = evt.widget
        if (len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            value = w.get(index)
            self.replaySimulationQuestion(value)

    def stringfromAccumulateurActions(self):
        s = "Sim " + str(self.replayLearningList.size()) + " : "
        for i in self.framePrincipale.FrameEcranControle.AccumulateurActions:
            s += (int2Action2String1Char(i))
        return s

    def launchHRLAction(self) : 
        state_size = self.env.state_size
        self.framePrincipale.FrameEcranControle.ResetAction()

        done = False
        batch_size = 2
        Episodes = 10
        scores_app = []
        scores_evo = []

        for e in range(Episodes):
            score_cumul = 0
            state = self.env.reset()
            state = state * (1 / float(self.env.state.grid_size))
            state = np.reshape(state, [1, state_size])
            self.framePrincipale.FrameEcranControle.AccumulateurActions = []

            for time in range(200):

                # agent execute l'action en fonction de l'état reçu en argument
                action = self.agent.act(state)
                # updateStep realise un step en actualisant la vue et demande au user son avis sur l'action
                next_state, reward, done = self.updateStep(action)

                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])

                self.agent.remember(state, action, reward, next_state, done)

                self.framePrincipale.FrameEcranControle.AccumulateurActions.append(action)    

                score_cumul += reward
                state = next_state

                #if done:
                #    self.replayLearningList.insert(END,self.stringfromAccumulateurActions())
                #    print("episode: {}/{}, score: {}, e: {:.5}"
                #           .format(e + 1, Episodes, score_cumul, self.agent.epsilon))
                #    break
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                    self.agent.memory.clear()
            scores_app.append(score_cumul)
            scores_evo.append(simuPostLearning(self.agent))


            #if(e % 15 == 0):
                #self.calculatePredictionMapAction()
                #self.update()

        try:
            self.agent.save("Weights_Model.wm")
        except:
            showinfo('Not OK', 'Failed at saving weight !')

        #plt.plot(scores_evo, 'b+')    
        #plt.show() 

    def switchReward(self, i):
        switcher={
            0: 0,
            1: 2 / 200,
            2: -10 / 200
        }
        return switcher.get(i,"Invalid reward")
  

    def updateStep(self, numeroAction) : 
        # On fait un pas de simulation
        next_state, reward, done = self.env.step(numeroAction)

        # Mise a jour des donnees de la frame de visualisation des etats
        EtatAvant = self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatAvant
        EtatApres = self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatApres
        ActionRealisee = self.framePrincipale.FrameVisualisation.FrameVisualisationState.ActionRealisee

        EtatAvant.set(EtatApres.get())
        EtatApres.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        ActionRealisee.set(int2Action2String(numeroAction))

        # On met a jour l'affichage graphique
        self.framePrincipale.FrameVisualisation.UpdateCanvas(numeroAction)
        self.framePrincipale.FrameEcranControle.Update()

        # On ajoute cette action a la liste des actions realisees sur cette simulation
        self.framePrincipale.FrameEcranControle.AccumulateurActions.append(numeroAction)

        # Si la simulation est finie, on enregistre celle ci dans la liste des simus et on reset le simulateur
        if (done and not self.framePrincipale.FrameEcranControle.inSimulation):
            self.framePrincipale.FrameEcranControle.AddSimuInList()
            self.framePrincipale.FrameEcranControle.ResetAction()

        # demande à l'utilisateur de juger l'action
        rewardHRL = int(input("Juger l'action : 1 : bien, 0 : je ne sais pas, 2 : nul"))
        rewardHRLNorm = self.switchReward(rewardHRL)
        reward = reward + rewardHRLNorm
        
        Recompense = self.framePrincipale.FrameVisualisation.FrameVisualisationState.Recompense
        Recompense.set(str(reward))
        self.framePrincipale.FrameEcranControle.AjouteScore(reward)
        self.framePrincipale.FrameEcranControle.Update()
        
        return next_state, reward, done