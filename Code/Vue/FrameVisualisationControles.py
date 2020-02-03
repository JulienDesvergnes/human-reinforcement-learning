from tkinter import *
from Modele.Environnement.Action import int2Action2String

class FrameVisualisationControles(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameVisualisationControleMap = LabelFrame(frame, text = "Controles", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationControleMap.pack(side=TOP, padx=5, pady=5)

        UPButton = Button(self.FrameVisualisationControleMap, text='Haut', command = self.UPAction)
        DOWNButton = Button(self.FrameVisualisationControleMap, text='Bas', command = self.DOWNAction)
        LEFTButton = Button(self.FrameVisualisationControleMap, text='Gauche', command = self.LEFTAction)
        RIGHTButton = Button(self.FrameVisualisationControleMap, text='Droite', command = self.RIGHTAction)

        UPButton.grid(row=0, column=1, sticky="nsew")
        LEFTButton.grid(row=1, column=0, sticky="nsew")
        RIGHTButton.grid(row=1, column=2, sticky="nsew")
        DOWNButton.grid(row=2, column=1, sticky="nsew")

    def UPAction(self):
        ActionUpInt = 2
        self.UpdateAll(ActionUpInt)
    def DOWNAction(self):
        ActionDownInt = 3
        self.UpdateAll(ActionDownInt)
    def LEFTAction(self):
        ActionLeftInt = 0
        self.UpdateAll(ActionLeftInt)
    def RIGHTAction(self):
        ActionRightInt = 1
        self.UpdateAll(ActionRightInt)

    def UpdateAll(self,numeroAction):

        # On fait un pas de simulation
        next_state, reward, done = self.env.step(numeroAction)

        # Mise a jour des donnees de la frame de visualisation des etats
        EtatAvant = self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatAvant
        EtatApres = self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatApres
        ActionRealisee = self.framePrincipale.FrameVisualisation.FrameVisualisationState.ActionRealisee
        Recompense = self.framePrincipale.FrameVisualisation.FrameVisualisationState.Recompense

        EtatAvant.set(EtatApres.get())
        EtatApres.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        ActionRealisee.set(int2Action2String(numeroAction))
        Recompense.set(str(reward))

        # On met a jour l'affichage graphique
        self.framePrincipale.FrameVisualisation.UpdateCanvas(numeroAction)
        self.framePrincipale.FrameEcranControle.AjouteScore(reward)
        self.framePrincipale.FrameEcranControle.Update()

        # On ajoute cette action a la liste des actions realisees sur cette simulation
        self.framePrincipale.FrameEcranControle.AccumulateurActions.append(numeroAction)

        # Si la simulation est finie, on enregistre celle ci dans la liste des simus et on reset le simulateur
        if (done and not self.framePrincipale.FrameEcranControle.inSimulation):
            self.framePrincipale.FrameEcranControle.AddSimuInList()
            self.framePrincipale.FrameEcranControle.ResetAction()