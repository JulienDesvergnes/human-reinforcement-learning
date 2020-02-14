from Modele.Environnement.State import State

class GoToTheGoalEnv2D :

    def __init__(self):
        ## L'etat de l'environnement ##
        self.state = State()
        ## La nombre d'elements decrivants un etat, ici 4 car un etat est decrit par la position du personnage et la position de la cible ##
        self.state_size = 4
        ## Le nombre d'action possibles ##
        self.action_size = 4
        ## Le nom de l'environnement ##
        self.name = "GoToTheGoalEnv2D"

        ## Les recompenses renforcement classique ##
        # self.rewardMovement = - 1.0 /  200
        # self.rewardWin = 203.0 / 200
        # self.rewardLose = - 20.0 / 200
        # self.reward = [("rewardMovement",self.rewardMovement), ("rewardWin", self.rewardWin), ("rewardLose", self.rewardLose)]

        ## Les recompenses renforcement humain ##
        self.rewardMovement = - 1 /  239
        self.rewardWin = 251 / 239
        self.rewardLose = -3 / 239
        self.reward = [("rewardMovement",self.rewardMovement), ("rewardWin", self.rewardWin), ("rewardLose", self.rewardLose)]

    ## Remet l'etat de l'environnement a celui du depart ##
    def reset(self):
        self.state = State()
        return self.state.convertInNumpy()

    ## Effectue une action sur l'environnement ##
    def step(self, action):

        if(action == 0):
            self.state.x -= 1
        elif(action == 1):
            self.state.x += 1
        elif(action == 2):
            self.state.y -= 1
        elif(action == 3):
            self.state.y += 1
        else:
            self.state.x += 0

        ## Sert a savoir si on a atteint la fin de la simulation au coup suivant ##
        continueVar = True
        ## Calculate reward ##
        if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
            r = self.rewardWin
        elif( self.state.x <= 0 or self.state.x >= self.state.grid_size - 1 or self.state.y <= 0 or self.state.y >= self.state.grid_size - 1):
            r = self.rewardLose
            continueVar = False
            done = True
        else:
            r = self.rewardMovement

        if(continueVar):
            if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
                done = True
            else:
                done = False

        ## On retourne le nouvel etat, la recompense et un booleen qui denote la terminaison de la simulation courante ##
        return (self.state.convertInNumpy(), r, done)

    ## Methode de rendu interne a ameliorer dans la vue fenetre ##
    def render(self):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                if(self.state.x == i and self.state.y == j):
                    print("X",end = '')
                elif(self.state.goalx == i and self.state.goaly == j):
                    print("G",end = '')
                else:
                    print("-",end = '')
            print(" ")
        print(" ")