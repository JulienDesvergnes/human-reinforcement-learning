from tkinter import *
from Vue.FrameDescription import FrameDescription
from Vue.FrameVisualisation import FrameVisualisation
from Vue.FrameEcranControle import FrameEcranControle

class FramePrincipale(Frame):
    
    def __init__(self, fenetre, env, agent, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.agent = agent
        self.env = env
        
        fenetre['bg']='white'

        # Frame de description
        self.FrameDescription = FrameDescription(fenetre, self.env, self.agent, self)

        # Frame de visualisation
        self.FrameVisualisation = FrameVisualisation(fenetre, self.env, self.agent, self)

        # Ecran de controle
        self.FrameEcranControle = FrameEcranControle(fenetre, self.env, self.agent, self)