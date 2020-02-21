from tkinter import * 
import numpy as np

class FrameQMap(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale


        self.FrameQMap = LabelFrame(frame, text = "Test Q map", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameQMap.pack(side=RIGHT, padx=5, pady=5)

        self.blabla = Label(self.FrameQMap, text="blabla")
        self.blabla.pack()

        ## Visualisation de l'environnement ##
        self.GridW = 400
        self.GridH = 400
        print("Avant")
        # label = Label(self.blabla, text="label")
        # label.grid(row=1)
       

        #self.CreateGrid(self.blabla, self.GridW, self.GridH)
        print("Après")
        self.initialize_grid()

        #self.tableau_label[0][0][0].set("tatat")
 
        #self.framePrincipale.update()


    def CreateGrid(self, frame, W, H):
        tableau_label = []
        for i in range(1,self.env.state.grid_size):
            tabtmp = []
            for j in range(1, self.env.state.grid_size):
                tabtmp.append([StringVar(),StringVar(),StringVar(),StringVar()])
            tableau_label.append(tabtmp)

        for i in range(1, self.env.state.grid_size):
            for j in range(1,self.env.state.grid_size):
                newframe = Frame(frame, bg="white",borderwidth = 2, relief = GROOVE)
                newframe.grid(row = i, column = j)

                QvalueLeft = StringVar()
                QvalueLeft.set(str(tableau_label[i-1][j-1][0].get()))
                labelLeft = Label(newframe, textvariable=QvalueLeft)
                labelLeft.grid(row = 2, column = 1)

                QvalueRight= StringVar()
                QvalueRight.set(str(tableau_label[i-1][j-1][1].get()))
                labelRight = Label(newframe, textvariable=QvalueRight)
                labelRight.grid(row = 2, column = 3)

                QvalueUp = StringVar()
                QvalueUp.set(str(tableau_label[i-1][j-1][2].get()))
                labelUp = Label(newframe, textvariable=QvalueUp)
                labelUp.grid(row =1, column = 2)

                QvalueDown = StringVar()
                QvalueDown.set(str(tableau_label[i-1][j-1][3].get()))
                labelDown = Label(newframe, textvariable=QvalueDown)
                labelDown.grid(row = 3, column = 2)

                #print(str(i) + " " + str(j))

                tableau_label[(i-1)%40][(j-1)%40].append([QvalueLeft, QvalueRight, QvalueUp, QvalueDown])
        return tableau_label
    

    def initialize_grid(self):
        self.blabla.destroy()
        self.blabla = Label(self.FrameQMap, text="blabla")
        self.blabla.pack()

        tableau_label = []
        for i in range(1,self.env.state.grid_size+1):
            tabtmp = []
            for j in range(1, self.env.state.grid_size+1):
                tabtmp.append([StringVar(),StringVar(),StringVar(),StringVar()])
            tableau_label.append(tabtmp)


        for i in range(1, self.env.state.grid_size+1):
            for j in range(1, self.env.state.grid_size+1):
                v = np.array([i / float(self.env.state.grid_size), j / float(self.env.state.grid_size), self.env.state.goalx / float(self.env.state.grid_size), self.env.state.goaly / float(self.env.state.grid_size)])
                v = np.reshape(v,[1,self.env.state_size])
                act_values = self.agent.model.predict(v) #Tableau de Q values actvalues[0] = q value left
                
                #print(act_values)
                for k in range(1,5):
                    tableau_label[i-1][j-1][k-1].set(str(round(act_values[0][k-1],2)))
            
                if (i-1==self.env.state.x) and (j-1==self.env.state.y):
                    background = "orchid2"
                else:
                    background = "white"

                newframe = Frame(self.blabla, bg=background,borderwidth = 2, relief = GROOVE)
                newframe.grid(row = i, column = j)

                QvalueLeft = StringVar()
                QvalueLeft.set(str(tableau_label[i-1][j-1][0].get()))
                labelLeft = Label(newframe, textvariable=QvalueLeft)
                labelLeft.grid(row = 2, column = 1)

                QvalueRight= StringVar()
                QvalueRight.set(str(tableau_label[i-1][j-1][1].get()))
                labelRight = Label(newframe, textvariable=QvalueRight)
                labelRight.grid(row = 2, column = 3)

                QvalueUp = StringVar()
                QvalueUp.set(str(tableau_label[i-1][j-1][2].get()))
                labelUp = Label(newframe, textvariable=QvalueUp)
                labelUp.grid(row =1, column = 2)

                QvalueDown = StringVar()
                QvalueDown.set(str(tableau_label[i-1][j-1][3].get()))
                labelDown = Label(newframe, textvariable=QvalueDown)
                labelDown.grid(row = 3, column = 2)

                #print(str(i) + " " + str(j))

                tableau_label[(i-1)%40][(j-1)%40].append([QvalueLeft, QvalueRight, QvalueUp, QvalueDown])
    