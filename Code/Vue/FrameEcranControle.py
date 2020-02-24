from tkinter import *
from tkinter.messagebox import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Modele.Environnement.Action import int2Action2String1Char
from Vue.FrameVisualisationControles import FrameVisualisationControles
import time
from Vue.FrameHRL_final import FrameHRL_final

class FrameEcranControle(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameControle = LabelFrame(frame, text = "Ecran de controle", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameControle.pack(side=LEFT, padx=5, pady=5)

        self.FrameRecompensesCumulees = LabelFrame(self.FrameControle, text = "Recompenses cumulees", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameRecompensesCumulees.pack(side=TOP, padx=5, pady=5)

        ## Courbes des recompenses cumulees
        self.FigureRecompensesCumulees = Figure(figsize=(3,3), dpi=100)
        self.FigureRecompensesCumuleesSubPlot = self.FigureRecompensesCumulees.add_subplot(111)

        self.CourbeRecompensesCumulees = FigureCanvasTkAgg(self.FigureRecompensesCumulees, self.FrameRecompensesCumulees)
        self.CourbeRecompensesCumulees.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True) 

        self.scoresCumules = [0]

        ## Recompense courante
        self.FrameRecompenseCourante = LabelFrame(self.FrameControle, text = "Recompense courante", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameRecompenseCourante.pack(side=TOP, padx=5, pady=5)

        self.ValeurRecompenseCourante = StringVar()
        self.ValeurRecompenseCourante.set("")
        Label(self.FrameRecompenseCourante, textvariable=self.ValeurRecompenseCourante, bg="white", justify="left").pack()

        ## Reset la simulation
        self.FrameResetSimulation = LabelFrame(self.FrameControle, text = "Reset simulation", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameResetSimulation.pack(side=TOP, padx=5, pady=5)

        self.ResetButton = Button(self.FrameResetSimulation, text='Reset', command = self.ResetAction)
        self.ResetButton.pack()

        ## Liste de replays
        self.FrameReplayList = LabelFrame(self.FrameControle, text = "Liste simulations", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameReplayList.config(width=250, height=250)
        self.FrameReplayList.pack(side=TOP, padx=5, pady=5, expand=True, fill = BOTH)
        self.FrameReplayList.pack_propagate(0)

        self.replayList = Listbox(self.FrameReplayList)
        self.replayList.pack(fill =BOTH)
        self.replayList.pack_propagate(0)
        self.replayList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))

        self.AccumulateurActions = []

        ## Booleen qui decrit si on est en simulation ou pas
        self.inSimulation = False

        # Ecran Renfo humain
        self.FrameHRL = FrameHRL_final(self.FrameControle, self.env, self.agent, self.framePrincipale)

    def AddSimuInList(self):
        self.replayList.insert(END,self.stringfromAccumulateurActions())

    def stringfromAccumulateurActions(self):
        s = "Sim " + str(self.replayList.size()) + " : "
        for i in self.AccumulateurActions:
            s += (int2Action2String1Char(i))
        return s

    def onselect(self,evt):
        w = evt.widget
        if (len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            value = w.get(index)
            self.replaySimulationQuestion(value)

    def replaySimulationQuestion(self,value):
        if askyesno('Rejouer Simulation', "Rejouer Simulation ?"):
            self.inSimulation = True
            self.ResetAction()
            self.replaySimulationAction(value)
            self.inSimulation = False

    def AjouteScore(self,score):
        self.scoresCumules.append(self.scoresCumules[-1] + score)

    def AjouterAction(self,action):
        self.AccumulateurActions.append(action)

    def replaySimulationAction(self,value):
        timeStep = 0.5
        for c in value:
            if(c == "R"):
                self.framePrincipale.FrameVisualisation.FrameVisualisationControles.RIGHTAction()
            if(c == "D"):
                self.framePrincipale.FrameVisualisation.FrameVisualisationControles.DOWNAction()
            if(c == "U"):
                self.framePrincipale.FrameVisualisation.FrameVisualisationControles.UPAction()
            if(c == "L"):
                self.framePrincipale.FrameVisualisation.FrameVisualisationControles.LEFTAction()
            self.framePrincipale.update()
            time.sleep(timeStep)

    def Update(self):
        self.FigureRecompensesCumuleesSubPlot.clear()
        self.FigureRecompensesCumuleesSubPlot.plot(self.scoresCumules)
        self.ValeurRecompenseCourante.set(self.scoresCumules[-1])
        self.CourbeRecompensesCumulees.draw()

    def Reset(self):
        self.scoresCumules = [0]
        self.AccumulateurActions = []
        self.FigureRecompensesCumuleesSubPlot.clear()
        self.FigureRecompensesCumuleesSubPlot.plot(self.scoresCumules)
        self.ValeurRecompenseCourante.set(self.scoresCumules[-1])
        self.CourbeRecompensesCumulees.draw()

    def ResetAction(self):

        # Remise a zero du modele
        self.env.reset()

        self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatAvant.set("")
        self.framePrincipale.FrameVisualisation.FrameVisualisationState.EtatApres.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.framePrincipale.FrameVisualisation.FrameVisualisationState.Recompense.set("Pas de recompense pour l'instant")
        self.framePrincipale.FrameVisualisation.FrameVisualisationState.ActionRealisee.set("Pas d'action pour l'instant")

        # Redessiner le canvas et le graphe de scores cumules
        self.Reset()

        self.framePrincipale.FrameVisualisation.ResetCanvas()