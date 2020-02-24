from tkinter import *
from Vue.FrameQMap import FrameQMap
from Vue.FrameDescription import FrameDescription

class FrameSecondaire(Frame):
    
    def __init__(self, fenetre, env, agent, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.agent = agent
        self.env = env
        
        fenetre['bg']='white'

        # Frame de description
        self.FrameDescription = FrameDescription(fenetre, self.env, self.agent, self)