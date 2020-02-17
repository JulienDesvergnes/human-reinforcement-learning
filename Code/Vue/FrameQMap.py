from tkinter import * 

class FrameQMap(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.message = LabelFrame(frame, text="bidule chouette", bg="white", borderwidth=2, relief=GROOVE)
        self.message.pack(side=TOP)
