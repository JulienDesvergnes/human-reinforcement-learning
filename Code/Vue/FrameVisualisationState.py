from tkinter import *

class FrameVisualisationState(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameVisualisationStateEvolution = LabelFrame(frame, text = "Evolution de l'etat", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationStateEvolution.pack(side=TOP, padx=5, pady=5)

        self.FrameVisualisationEtatAvant = LabelFrame(self.FrameVisualisationStateEvolution, text = "Etat Avant", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationEtatAvant.config(width=80, height=50)
        self.FrameVisualisationEtatAvant.pack(side=LEFT, padx=2, pady=2)
        self.FrameVisualisationEtatAvant.pack_propagate(0)

        self.FrameVisualisationAction = LabelFrame(self.FrameVisualisationStateEvolution, text = "Action", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationAction.config(width=190, height=65)
        self.FrameVisualisationAction.pack(side=LEFT, padx=2, pady=2)
        self.FrameVisualisationAction.pack_propagate(0)

        self.FrameVisualisationEtatApres = LabelFrame(self.FrameVisualisationStateEvolution, text = "Etat Apres", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationEtatApres.config(width=80, height=50)
        self.FrameVisualisationEtatApres.pack(side=LEFT, padx=2, pady=2)
        self.FrameVisualisationEtatApres.pack_propagate(0)

        # Remplissage des differentes zones
        self.EtatAvant = StringVar()
        self.EtatAvant.set("")
        Label(self.FrameVisualisationEtatAvant, textvariable=self.EtatAvant, bg="white", justify="left").pack()

        self.EtatApres = StringVar()
        # self.EtatApres.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.EtatApres.set("(" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        Label(self.FrameVisualisationEtatApres, textvariable=self.EtatApres, bg="white", justify="left").pack()

        self.Recompense = StringVar()
        self.Recompense.set("Pas de recompense pour l'instant")
        Label(self.FrameVisualisationAction, textvariable=self.Recompense, bg="white", justify="left").pack()

        self.ActionRealisee = StringVar()
        self.ActionRealisee.set("Pas d'action pour l'instant")
        Label(self.FrameVisualisationAction, textvariable=self.ActionRealisee, bg="white", justify="left").pack()