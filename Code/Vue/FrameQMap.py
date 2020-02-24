from tkinter import * 
import numpy as np

class FrameQMap(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale


        self.FrameQMap = LabelFrame(frame, text = "Test Q map", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameQMap.pack(side=LEFT, padx=5, pady=5)

        self.QMapGrid = Label(self.FrameQMap, text="QMapGrid")
        self.QMapGrid.pack()

        ## Visualisation de l'environnement ##
        self.update_Qmap()

    def update_Qmap(self):
        self.QMapGrid.destroy()
        self.QMapGrid = Label(self.FrameQMap, text="QMapGrid")
        self.QMapGrid.pack()

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
            
                if (j-1==self.env.state.x) and (i-1==self.env.state.y):
                    background = "orchid2"
                else:
                    background = "white"

                newframe = Frame(self.QMapGrid, bg=background,borderwidth = 2, relief = GROOVE)
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

                m = max(act_values[0])
                ind_max = np.argmax(act_values[0])
                if ind_max == 0:
                    labelCenter = Label(newframe, text=" < ", bg = "red")
                elif ind_max == 1:
                    labelCenter = Label(newframe, text=" > ", bg = "green")
                elif ind_max == 2:
                    labelCenter = Label(newframe, text=" ^ ", bg = "yellow")
                elif ind_max == 3:
                    labelCenter = Label(newframe, text=" v ", bg = "orange")

                labelCenter.grid(row = 2, column = 2)

    
