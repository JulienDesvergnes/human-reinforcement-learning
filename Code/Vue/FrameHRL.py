from tkinter import *
import os
from tkinter.messagebox import *
import numpy as np
from Modele.Environnement.Action import int2Action2String1Char

class FrameHRL(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        # definition des differentes frames incluses dans la frame HRL
        self.FrameHumanDecision = LabelFrame(frame, text = "Human Decision for HRL", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameHumanDecision.pack(side=TOP, padx=5, pady=5)

        # redimensionnement grille pour centrer les boutons
        self.FrameHumanDecision.grid_rowconfigure(0, weight=1)
        self.FrameHumanDecision.grid_rowconfigure(4, weight=1)
        self.FrameHumanDecision.grid_columnconfigure(0, weight=1)
        self.FrameHumanDecision.grid_columnconfigure(4, weight=1)

        # definition des trois boutons de decision pour l humain
        YESButton = Button(self.FrameHumanDecision, text='YES', command = self.YESAction)
        NOButton = Button(self.FrameHumanDecision, text='NO', command = self.NOAction)
        IDKButton = Button(self.FrameHumanDecision, text='IDK', command = self.IDKAction)

        # placement de ces boutons dans la frame
        YESButton.grid(row=1, column=1, sticky="nsew")
        IDKButton.grid(row=1, column=2, sticky="nsew")
        NOButton.grid(row=1, column=3, sticky="nsew")

    # definition du code de l'action associée à chaque bouton
    # plus tard -> ces actions doivent modifier la valeur de la reward d'apprentissage
    def YESAction(self):
        ActionYESInt = 1
    def NOAction(self):
        ActionNOInt = 1
    def IDKAction(self):
        ActionIDKInt = 0
