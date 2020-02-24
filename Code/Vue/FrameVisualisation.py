from tkinter import *
from Vue.FrameVisualisationState import FrameVisualisationState
from Vue.FrameVisualisationControles import FrameVisualisationControles 
from Vue.FrameDescription import FrameDescription

class FrameVisualisation(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameSimulation = LabelFrame(frame, text = "Simulation : " + self.env.name, bg="white", borderwidth=2, relief=GROOVE)
        self.FrameSimulation.pack(side=LEFT, padx=5, pady=5)

        self.FrameVisualisationEnvironnement = LabelFrame(self.FrameSimulation, text = "Environnement", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameVisualisationEnvironnement.pack(side=TOP, padx=2, pady=2)

        # self.FrameVisualisationState = FrameVisualisationState(self.FrameSimulation, self.env, self.agent, self.framePrincipale)

        # self.FrameVisualisationControles = FrameVisualisationControles(self.FrameSimulation, self.env, self.agent, self.framePrincipale)

        ## Visualisation de l'environnement ##
        self.CanvasW = 400
        self.CanvasH = 400
        self.canvas, self.mobile = self.VisualisationEnvironnementCanvas(self.FrameVisualisationEnvironnement, self.CanvasW, self.CanvasH)
        self.canvas.pack()

        self.FrameDescription = FrameDescription(self.FrameSimulation, self.env, self.agent, self.framePrincipale)

    def VisualisationEnvironnementCanvas(self,frame,W,H) :
    	# Taille du canvas
        canvas = Canvas(frame, width=W, height=H, background='dark olive green')

        gridSize = self.env.state.grid_size

        # Dessin des contours haut et gauche
        canvas.create_line(1, 2, H + 2, 2, fill = 'black')
        canvas.create_line(2, 1, 2, W + 2, fill = 'black')

        # Dessin du quadrillage
        for i in range (gridSize):
                canvas.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                canvas.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')

        # Remplissage du bord avec des rectangles rouges
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
                    canvas.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        # Dessin du mobile
        x0 = 1 + (self.env.state.x) * (W + 1) / gridSize
        y0 = 1 + (self.env.state.y) * (H + 1) / gridSize
        if (self.env.state.x == 0):
            x0 = 3 + (self.env.state.x) * (W + 1) / gridSize
        if (self.env.state.y == 0):
            y0 = 3 + (self.env.state.y) * (H + 1) / gridSize
        x1 = (self.env.state.x + 1) * (W + 1) / gridSize
        y1 = (self.env.state.y + 1) * (H + 1) / gridSize
        # On recupere le rectangle dans la variable mobile pour pouvoir le deplacer plus facilement
        mobile = canvas.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        # Dessin de l'objectif
        x0 = 1 + (self.env.state.goalx) * (W + 1) / gridSize
        y0 = 1 + (self.env.state.goaly) * (H + 1) / gridSize
        if (self.env.state.goalx == 0):
            x0 = 3 + (self.env.state.goalx) * (W + 1) / gridSize
        if (self.env.state.goaly == 0):
            y0 = 3 + (self.env.state.goaly) * (H + 1) / gridSize
        x1 = (self.env.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.env.state.goaly + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        return canvas, mobile

    def UpdateCanvas(self,numeroAction):
        gridSize = self.env.state.grid_size
        x0 = 1 + (self.env.state.x) * (self.CanvasW + 1) / gridSize
        y0 = 1 + (self.env.state.y) * (self.CanvasH + 1) / gridSize
        if (self.env.state.x == 0):
            x0 = 3 + (self.env.state.x) * (self.CanvasW + 1) / gridSize
        if (self.env.state.y == 0):
            y0 = 3 + (self.env.state.y) * (self.CanvasH + 1) / gridSize
        x1 = (self.env.state.x + 1) * (self.CanvasW + 1) / gridSize
        y1 = (self.env.state.y + 1) * (self.CanvasH + 1) / gridSize

        self.canvas.coords(self.mobile,x0,y0,x1,y1)

    def ResetCanvas(self):
        gridSize = self.env.state.grid_size
        x0 = 1 + (self.env.state.x) * (self.CanvasW + 1) / gridSize
        y0 = 1 + (self.env.state.y) * (self.CanvasH + 1) / gridSize
        if (self.env.state.x == 0):
            x0 = 3 + (self.state.x) * (self.CanvasW + 1) / gridSize
        if (self.env.state.y == 0):
            y0 = 3 + (self.env.state.y) * (self.CanvasH + 1) / gridSize
        x1 = (self.env.state.x + 1) * (self.CanvasW + 1) / gridSize
        y1 = (self.env.state.y + 1) * (self.CanvasH + 1) / gridSize

        self.canvas.coords(self.mobile,x0,y0,x1,y1)