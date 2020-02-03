import gym
import tensorflow as tf
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.messagebox import *
import matplotlib
matplotlib.use("TkAgg")
import os
from PIL import ImageGrab

from Modele.Agent.DQNAgent import DQNAgent
from Modele.Environnement.State import State
from Modele.Environnement.Action import *
from Modele.Environnement.Environnement import GoToTheGoalEnv2D
from Vue.FramePrincipale import FramePrincipale



def simuPostLearning(agent):
    env = GoToTheGoalEnv2D()
    state_size = env.state_size
    action_size = env.action_size
    #state = np.array([env.state.grid_size, env.state.x, env.state.y, env.state.goalx, env.state.goaly, env.state.bombx, env.state.bomby])
    state = np.array([env.state.x / float(env.state.grid_size), env.state.y/ float(env.state.grid_size), env.state.goalx/ float(env.state.grid_size), env.state.goaly/ float(env.state.grid_size)])
    state = np.reshape(state,[1,4])
    score_cumul = 0
    for time in range(200):
        act_values = agent.model.predict(state)
        action = np.argmax(act_values[0])
        next_state, reward, done = env.step(action)
        score_cumul += reward
        state = next_state * (1/env.state.grid_size)
        state = np.reshape(state,[1,4])
        if done:
            break
    return score_cumul

class HRLView(Frame):
	"""docstring for HRLVIEW"""
	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
		

class Interface(Frame):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre, env, agent, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.agent = agent
        self.env = env
        
        fenetre['bg']='white'

        # frame 2
        Frame2 = Frame(fenetre, borderwidth=2, relief=GROOVE)
        Frame2.pack(side=LEFT, padx=10, pady=10)

        # frame 3 dans frame 2
        #Frame3 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        #Frame3.pack(side=RIGHT, padx=5, pady=5)

        # frame 4 dans frame 1
        Frame5 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame5.pack(side=BOTTOM, padx=5, pady=5)

        Frame4 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame4.pack(side=BOTTOM, padx=5, pady=5)

        Frame6 = Frame(Frame1, bg="white", borderwidth=2, relief=GROOVE)
        Frame6.pack(side=BOTTOM, padx=5, pady=5)

        Frame8 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame8.pack(side=BOTTOM, padx=5, pady=5)

        Frame9 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame9.pack(side=BOTTOM, padx=5, pady=5)

        Frame9tmp = Frame(Frame9, bg="gray", borderwidth=2, relief=FLAT)
        Frame9tmp.pack(side=BOTTOM, padx=5, pady=5)

        Frame10 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame10.config(width=250, height=40)
        Frame10.pack(side=LEFT, padx=5, pady=5, fill =BOTH)
        Frame10.pack_propagate(0)

        Frame12 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame12.pack(side=LEFT, padx=5, pady=5, fill =BOTH)

        Frame11 = Frame(Frame9tmp, bg="white", borderwidth=2, relief=FLAT)
        Frame11.config(width=250, height=40)
        Frame11.pack(side=LEFT, padx=5, pady=5, fill =BOTH)
        Frame11.pack_propagate(0)

        Frame7 = Frame(Frame2, bg="white", borderwidth=2, relief=GROOVE)
        Frame7.pack(side=BOTTOM, padx=5, pady=5)

        Frame14 = Frame(fenetre, bg="seashell3", borderwidth=2, relief=GROOVE)
        Frame14.pack(side=LEFT, padx=5, pady=5)

        Frame17 = Frame(fenetre, bg="mistyrose3", borderwidth=2, relief=GROOVE)
        Frame17.pack(side=LEFT, padx=5, pady=5)

        Frame24 = Frame(fenetre, bg="mistyrose2", borderwidth=2, relief=GROOVE)
        Frame24.pack(side=LEFT, padx=5, pady=5)

        Frame15 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        Frame15.config(width=250, height=250)
        Frame15.pack(side=BOTTOM, padx=5, pady=5, expand=True, fill =BOTH)
        Frame15.pack_propagate(0)

        Frame16 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        Frame16.config(width=200, height=75)
        Frame16.pack(side=BOTTOM, padx=5, pady=5)
        Frame16.pack_propagate(0)

        self.Frame13 = Frame(Frame14, bg="white", borderwidth=2, relief=GROOVE)
        self.Frame13.pack(side=BOTTOM, padx=5, pady=5)

        Frame21 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame21.pack(side=BOTTOM, padx=5, pady=5)

        Frame23 = LabelFrame(Frame21, text = "Actions", bg="white", borderwidth=2, relief=GROOVE)
        Frame23.pack(side=BOTTOM, padx=5, pady=5, fill="both", expand="yes")

        Frame22 = LabelFrame(Frame21, bg="white", borderwidth=2, relief=GROOVE)
        Frame22.pack(side=BOTTOM, padx=5, pady=5, fill="both", expand="yes")

        Frame19 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame19.config(width=250, height=80)
        Frame19.pack(side=BOTTOM, padx=5, pady=5, fill =BOTH)
        Frame19.pack_propagate(0)

        Frame20 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame20.config(width=250, height=250)
        Frame20.pack(side=BOTTOM, padx=5, pady=5, fill =BOTH)
        Frame20.pack_propagate(0)

        Frame18 = Frame(Frame17, bg="white", borderwidth=2, relief=GROOVE)
        Frame18.config(width=250, height=150)
        Frame18.pack(side=BOTTOM, padx=5, pady=5 ,fill =BOTH)
        Frame18.pack_propagate(0)


        # Ajout de labels
        Label(Frame17, text="RL Screen",bg="mistyrose3").pack(padx=10, pady=10)
        Label(Frame18, text="Predict Action From State",bg="white").pack(padx=10, pady=10)
        Label(Frame19, text="Launch Traning",bg="white").pack(padx=10, pady=10)
        Label(Frame20, text="Learning list",bg="white").pack(padx=10, pady=10)
        Label(Frame21, text="Prediction Map",bg="white").pack(padx=10, pady=10)
        Label(Frame24, text="HRL Screen",bg="mistyrose2").pack(padx=10, pady=10)
        


        self.canvasFigure = FigureCanvasTkAgg(self.figurecr, self.Frame13)
        self.canvasFigure.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True) 

        self.replayGamesList = Listbox(Frame15)
        self.replayGamesList.pack(fill =BOTH)
        self.replayGamesList.pack_propagate(0)
        self.replayGamesList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))

        self.resetSimuButton = Button(Frame16, text ='RESET', command=self.resetRender)
        self.resetSimuButton.pack()

        self.launchTrainingButton = Button(Frame19, text ='GOGOGO !!!', command=self.launchTrainingAction)
        self.launchTrainingButton.pack(side="bottom")

        self.replayGamesLearningList = Listbox(Frame20)
        self.replayGamesLearningList.pack(fill =BOTH)
        self.replayGamesLearningList.pack_propagate(0)
        self.replayGamesLearningList.bind('<<ListboxSelect>>', lambda evt: self.onselect(evt))
    
        self.inReplayMode = False

        self.calculatePredictionMapButton = Button(Frame23, text ='Calculate Map', command=self.calculatePredictionMapAction)
        self.calculatePredictionMapButton.pack(side="left")

        self.savePredictionMapButton = Button(Frame23, text ='Save Map', command=self.saveAction)
        self.savePredictionMapButton.pack(side="left")

        self.drawPathButton = Button(Frame23, text ='Draw Path', command=self.drawPathAction)
        self.drawPathButton.pack(side="left")

        self.loadWeightButton = Button(Frame18, text ='Load Weights', command=self.loadWeightAction)
        self.loadWeightButton.pack(side="left")

        self.canvasPredictionMap = env.buildCanevasPredictionMap(Frame22, self.agent)
        self.canvasPredictionMap.pack()

        self.OpenHRLView = Button(Frame24, text ='OpenHRLView', command=self.OpenHRLViewAction)
        self.OpenHRLView.pack()

    def OpenHRLViewAction(self):
    	self.HRLFenetre = Tk()
    	self.HRLFenetre.title('HRL View')

    	self.HRLFrame = HRLView(self.HRLFenetre)
    	self.HRLFrame.mainloop()


    def loadWeightAction(self):
        self.agent.load("Weights_Model.wm")
        showinfo('OK', 'Succesfully loaded !')

    def drawPathAction(self):
        self.env.drawPath(self.agent)

    def saveAction(self, path ="PredictionMap.png"):
        x=self.canvasPredictionMap.winfo_rootx()
        y=self.canvasPredictionMap.winfo_rooty()
        x1=x+self.canvasPredictionMap.winfo_width()
        y1=y+self.canvasPredictionMap.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save("PredictionMap.png")

    def onselect(self,evt):
        w = evt.widget
        if (len(w.curselection()) > 0):
            index = int(w.curselection()[0])
            value = w.get(index)
            print("You selected " + str(index) + ", " + str(value))
            self.replaySimulationQuestion(value)

    def calculatePredictionMapAction(self):
        self.env.calculatePredictionMapActionFromEnv(self.agent)

    def replaySimulationAction(self,value):
        deltaTime = 0.5
        for c in value:
            if(c == "R"):
                self.RightAction()
            if(c == "D"):
                self.DownAction()
            if(c == "U"):
                self.UpAction()
            if(c == "L"):
                self.LeftAction()
            self.update()
            time.sleep(deltaTime)

    def replaySimulationQuestion(self,value):
        if askyesno('Replay Simulation', "Replay Simulation ?"):
            #r = Replayeur(self,value)
            #r.start()
            self.inReplayMode = True
            self.resetRender()
            self.rewardObtenue.set("")
            self.actionperformedlabel.set("")
            self.currentStateLabel.set("")
            self.replaySimulationAction(value)
            self.inReplayMode = False

    def resetRender(self):
        self.indicesFigures = [0]
        self.scoreCumule = [0]
        self.actionSequence = []
        self.rewardObtenue.set("No reward FTM")
        self.actionperformedlabel.set("No action FTM")
        self.env.state.x = 5.0
        self.env.state.y = 5.0
        self.env.majCanvas(0)
        self.previousStateLabel.set("                                       ")
        self.currentStateLabel.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.figuresubplotcr.clear()
        self.figuresubplotcr.plot(self.indicesFigures, self.scoreCumule)
        self.canvasFigure.draw()


    def MajRewardCumules(self,reward):
        self.scoreCumule.append(self.scoreCumule[-1] + reward)
        self.indicesFigures.append(self.indicesFigures[-1] + 1)
        self.figuresubplotcr.clear()
        self.figuresubplotcr.plot(self.indicesFigures, self.scoreCumule)
        self.canvasFigure.draw()

    def MajLabels(self,noAction):
        next_state, reward, done = self.env.step(noAction)
        self.MajRewardCumules(reward)
        self.env.majCanvas(noAction)
        self.previousStateLabel.set(self.currentStateLabel.get())
        self.currentStateLabel.set("Position du mobile de déplacement : (" + str(self.env.state.x + 1) + ", " + str(self.env.state.y + 1) + ")")
        self.actionperformedlabel.set(int2Action2String(noAction))
        self.rewardObtenue.set(str(reward))
        self.actionSequence.append(noAction)
        if (done and not self.inReplayMode):
            self.replayGamesList.insert(END,self.stringfromActionSequence(False))
            self.resetRender()
            
    def stringfromActionSequence(self,train):
        s = "Sim " + str(self.replayGamesList.size()) + " : "
        if (train):
            s = "Sim " + str(self.replayGamesLearningList.size()) + " : "
        for i in self.actionSequence:
            s += (int2Action2String1Char(i))
        return s

    def launchTrainingAction(self):

        state_size = self.env.state_size
        self.resetRender()

           #try:
        #    self.agent.load("Weights_Model.wm")
        #except:
        #    print("ERROR launchTrainingAction : LOAD MODEL WEIGHT")

        if (os.path.exists("Weights_Model.wm")):
            self.agent.load("Weights_Model.wm")

        done = False
        batch_size = 2
        Episodes = 50
        scores_app = []
        scores_evo = []

        #filename = "predictions.txt"
        #filename_scores = "scores.txt"
        #myfile = open(filename, 'w')
        #myfile_scores = open(filename_scores, 'w')
        #self.env.writeResultsFromLearning(self.agent, myfile)

        for e in range(Episodes):
            score_cumul = 0
            state = self.env.reset()
            state = state * (1 / float(self.env.state.grid_size))
            state = np.reshape(state, [1, state_size])
            self.indicesFigures = [0]
            self.scoreCumule = [0]
            self.actionSequence = []

            #print("### DEBUT EPOQUE " + str(e) + " ###")
            for time in range(200):
                # env.render()
                #print("POSITION JOUEUR " + str(env.state.x) + ", " + str(env.state.y) + " --- POSITION CIBLE " + str(env.state.goalx) + ", " + str(env.state.goaly))
                action = self.agent.act(state)
                #print("ACTION CHOISIE : " + str(action))
                next_state, reward, done = self.env.step(action)
                self.scoreCumule.append(self.scoreCumule[-1] + reward)
                self.indicesFigures.append(self.indicesFigures[-1] + 1)
                self.rewardObtenue.set(str(reward))
                self.actionSequence.append(action)    
                next_state = next_state * (1 / float(self.env.state.grid_size))
                next_state = np.reshape(next_state, [1, state_size])
                self.agent.remember(state, action, reward, next_state, done)
                score_cumul += reward
                #print("REWARD " + str(reward) + " --- CUMUL_REWARD " + str(score_cumul))
                state = next_state
                if done:
                    self.replayGamesLearningList.insert(END,self.stringfromActionSequence(True))
                    print("episode: {}/{}, score: {}, e: {:.5}"
                          .format(e + 1, Episodes, score_cumul, self.agent.epsilon))
                    break
                if len(self.agent.memory) > batch_size:
                    self.agent.replay(batch_size)
                    self.agent.memory.clear()
            scores_app.append(score_cumul)
            scores_evo.append(simuPostLearning(self.agent))
            # # # # env.writeResultsFromLearning(agent, myfile)
            #myfile_scores.write(str(scores_evo[-1]) + "\n")
            #myfile_scores.flush()

            if(e % 15 == 0):
                self.calculatePredictionMapAction()
                self.update()
        #myfile.close()

        try:
            self.agent.save("Weights_Model.wm")
        except:
            print("ERROR launchTrainingAction : SAVE MODEL WEIGHT")

        plt.plot(scores_evo, 'b+')    
        plt.show()    

if __name__ == "__main__":

    fenetre = Tk()
    fenetre.title('Interface HRL')

    env_ = GoToTheGoalEnv2D()
    state_size = env_.state_size
    action_size = env_.action_size
    agent_ = DQNAgent(state_size, action_size)

    FramePrincipale = FramePrincipale(fenetre, env_, agent_)
    FramePrincipale.mainloop()