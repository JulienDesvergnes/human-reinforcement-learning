from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FrameEcranControle(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameControle = LabelFrame(frame, text = "Ecran de controle", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameControle.pack(side=LEFT, padx=5, pady=5, fill="both", expand="yes")

        self.FrameRecompensesCumulees = LabelFrame(self.FrameControle, text = "Recompenses cumulees", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameRecompensesCumulees.pack(side=TOP, padx=5, pady=5, fill="both", expand="yes")

        ## Courbes des recompenses cumulees
        self.FigureRecompensesCumulees = Figure(figsize=(4,3), dpi=100)
        self.FigureRecompensesCumuleesSubPlot = self.FigureRecompensesCumulees.add_subplot(111)

        self.CourbeRecompensesCumulees = FigureCanvasTkAgg(self.FigureRecompensesCumulees, self.FrameRecompensesCumulees)
        self.CourbeRecompensesCumulees.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True) 

        self.indicesFigures = [0]
        self.scoreCumule = [0]



        

        