from tkinter import *

class FrameDescription(Frame):
    
    def __init__(self, frame, env, agent, framePrincipale, **kwargs):
        self.agent = agent
        self.env = env
        self.framePrincipale = framePrincipale

        self.FrameDescription = LabelFrame(frame, text = "Description", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameDescription.pack(side=LEFT, padx=5, pady=5)

        self.FrameDescriptionAgent = LabelFrame(self.FrameDescription, text = "Agent", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameDescriptionAgent.pack(side=TOP, padx=2, pady=2)

        self.FrameDescriptionReseau = LabelFrame(self.FrameDescription, text = "Reseau", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameDescriptionReseau.pack(side=TOP, padx=2, pady=2)

        self.FrameDescriptionEnv = LabelFrame(self.FrameDescription, text = "Reseau", bg="white", borderwidth=2, relief=GROOVE)
        self.FrameDescriptionEnv.pack(side=TOP, padx=2, pady=2)

        # Descriptif agent
        descriptifAgent = "State size / Input size = " + str(self.env.state_size) + " \n" + \
        "Action size / Output size = " + str(self.env.action_size) + " \n" + \
        "Memory = deque(" + str(self.agent.memory.maxlen) + ") \n" + \
        "Discount rate (gamma) = " + str(self.agent.gamma) + " \n" + \
        "Exploration rate (epsilon) = " + str(self.agent.epsilon) + " \n" + \
        "Exploration rate minimum = " + str(self.agent.epsilon_min) + "\n" + \
        "Exploration rate decay = " + str(self.agent.epsilon_decay) + "\n" + \
        "Learning rate (alpha) = " + str(self.agent.learning_rate)
        # Ajout de la description de l'agent dans un label
        descriptifAgentLabel = Label(self.FrameDescriptionAgent, text=descriptifAgent, bg="white", justify="left")
        descriptifAgentLabel.pack()

        # Descriptif du reseau
        config = self.agent.model.get_config()
        k,v = config.items()
        net = "Input Layer : " + str(v[1][0].get('config').get('batch_input_shape')[1])
        for i in range (len(v[1])):
            net = net + "\n"
            name = str((v[1][i].get('class_name')))
            nb_neural  = str((v[1][i].get('config').get('units')))
            factivation = str((v[1][i].get('config').get('activation')))
            net = net + "Hidden Layer " + str(i+1) + " : " + name + " " + nb_neural + \
            " - Activation = " + factivation
        # Ajout de la description du reseau dans un label
        networkLabel = Label(self.FrameDescriptionReseau, text=net, bg="white", justify="left")
        networkLabel.pack()

        # Descriptif de l'environnement
        descriptionEnvironnement = ""
        for n,v in self.env.reward :
            descriptionEnvironnement += n + " : " + str(v) + "\n"
        descriptionEnvironnement = descriptionEnvironnement[:len(descriptionEnvironnement)-1]
        descriptionEnvironnementLabel = Label(self.FrameDescriptionEnv, text=descriptionEnvironnement, bg="white", justify="left")
        descriptionEnvironnementLabel.pack()