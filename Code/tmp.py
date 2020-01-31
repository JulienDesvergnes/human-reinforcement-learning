class GoToTheGoalEnv2D :

    def __init__(self):
        self.state = State()
        #self.state_size = 7
        self.state_size = 4
        self.action_size = 4
        self.name = "GoToTheGoalEnv2D"
        self.rewardMovement = - 1.0 /  200
        self.rewardWin = 203.0 / 200
        self.rewardLose = - 20.0 / 200
        self.reward = [("rewardMovement",self.rewardMovement), ("rewardWin", self.rewardWin), ("rewardLose", self.rewardLose)]
        self.elemPerso = 0
        self.canvas = 0
        self.canvasMap = 0

    def reset(self):
        self.state = State()
        return self.state.convertInNumpy()

    def step(self, action):
        ## Perform movement
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

        continueP = True
        ## Calculate reward
        mind = 0.001
        #if (abs(self.state.x - self.state.goalx) < mind and abs(self.state.y - self.state.goaly) < mind):
        if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
            r = self.rewardWin
        #elif (self.state.x == self.state.bombx and self.state.y == self.state.bomby):
            #r = -20
        elif( self.state.x <= 0 or self.state.x >= self.state.grid_size - 1 or self.state.y <= 0 or self.state.y >= self.state.grid_size - 1):
            r = self.rewardLose
            continueP = False
            done = True
        else:
            r = self.rewardMovement

        if(continueP):
            ## Verify done
            # or self.state.x == self.state.bombx and self.state.y == self.state.bomby
            if (self.state.x == self.state.goalx and self.state.y == self.state.goaly):
                done = True
            else:
                done = False

        return (self.state.convertInNumpy(), r, done)

    def render(self):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                if(self.state.bombx == i and self.state.bomby == j):
                    print("B",end = '')
                elif(self.state.x == i and self.state.y == j):
                    print("X",end = '')
                elif(self.state.goalx == i and self.state.goaly == j):
                    print("G",end = '')
                else:
                    print(" ",end = '')
            print(" ")
        print(" ")

    def showResultsFromLearning(self, agent):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                #v = np.array([self.state.grid_size, i, j, self.state.goalx, self.state.goaly, self.state.bombx, self.state.bomby])
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                actions = agent.model.predict(v)
                print("Position : ", i, "Direction : ", actions)
            

    def writeResultsFromLearning(self, agent, file):
        for i in range(self.state.grid_size):
            for j in range(self.state.grid_size):
                #v = np.array([self.state.grid_size, i, j, self.state.goalx, self.state.goaly, self.state.bombx, self.state.bomby])
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                actions = agent.model.predict(v)
                file.write("Position : " + str(i) + " Direction : " + str(actions[0][0]) + ", " + str(actions[0][1]) + ", " + str(actions[0][2]) + ", " + str(actions[0][3]) + "\n")
            file.write("\n")

    def majCanvas(self, action):
        W = 400
        H = 400
        gridSize = self.state.grid_size
        x0 = 1 + (self.state.x) * (W + 1) / gridSize
        y0 = 1 + (self.state.y) * (H + 1) / gridSize
        if (self.state.x == 0):
            x0 = 3 + (self.state.x) * (W + 1) / gridSize
        if (self.state.y == 0):
            y0 = 3 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvas.coords(self.elemPerso,x0,y0,x1,y1)

    def drawPath(self,agent):
        self.canvasMap.delete("all")
        W = 200
        H = 200
        gridSize = self.state.grid_size
        self.canvasMap.create_line(1, 2, H + 2, 2, fill = 'black')
        self.canvasMap.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                self.canvasMap.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                self.canvasMap.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add Path
        alreadyDone = []
        px = deepcopy(self.state.x)
        py = deepcopy(self.state.y)
        for i in range(200):
            v = np.array([px / float(self.state.grid_size), py / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
            v = np.reshape(v,[1,self.state_size])
            act_values = agent.model.predict(v)
            action = np.argmax(act_values[0])

            alreadyDone.append((px,py))

            if(action == 0):
                px = px - 1
            if (action == 1):
                px = px + 1
            if(action == 2):
                py = py - 1
            if (action == 3):
                py = py + 1

            if((px,py) not in alreadyDone):
                if (px == 0 or py == 0):
                    x0 = 1 + (px) * (W + 1) / gridSize
                    y0 = 1 + (py) * (H + 1) / gridSize
                if (px == 0):
                    x0 = 3 + (px) * (W + 1) / gridSize
                if (py == 0):
                    y0 = 3 + (py) * (H + 1) / gridSize
                else :
                    x0 = 1 + (px) * (W + 1) / gridSize
                    y0 = 1 + (py) * (H + 1) / gridSize
                x1 = (px + 1) * (W + 1) / gridSize
                y1 = (py + 1) * (H + 1) / gridSize
                self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'PaleGreen2', outline = "")

            if((px < 0) or (px > float(self.state.grid_size)) or (py < 0) or (py > float(self.state.grid_size)) or (px == self.state.goalx and py == self.state.goaly)):
                break


        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')


    def calculatePredictionMapActionFromEnv(self,agent):
        self.canvasMap.delete("all")
        W = 200
        H = 200
        gridSize = self.state.grid_size
        self.canvasMap.create_line(1, 2, H + 2, 2, fill = 'black')
        self.canvasMap.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                self.canvasMap.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                self.canvasMap.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        self.canvasMap.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    self.canvasMap.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    self.canvasMap.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    self.canvasMap.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    self.canvasMap.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')
        
    
    def buildCanevasPredictionMap(self, frame, agent):
        W = 200
        H = 200
        canvas = Canvas(frame, width=W, height=H, background='dark olive green')
        gridSize = self.state.grid_size
        canvas.create_line(1, 2, H + 2, 2, fill = 'black')
        canvas.create_line(2, 1, 2, W + 2, fill = 'black')
        for i in range (gridSize):
                canvas.create_line(1, (i + 1) * (W + 1) / gridSize, H + 2, (i + 1) * (W + 1) / gridSize, fill = 'black')
                canvas.create_line((i + 1) * (H + 1) / gridSize, 1, (i + 1) * (H + 1) / gridSize,  W + 2, fill = 'black')
        # fill brd with bomb
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                    canvas.create_rectangle(x0,y0,x1,y1, fill = 'red4', outline = "")

        if (self.state.x == 0 or self.state.y == 0):
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
            if (self.state.x == 0):
                x0 = 3 + (self.state.x) * (W + 1) / gridSize
            if (self.state.y == 0):
                y0 = 3 + (self.state.y) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.x) * (W + 1) / gridSize
            y0 = 1 + (self.state.y) * (H + 1) / gridSize
        x1 = (self.state.x + 1) * (W + 1) / gridSize
        y1 = (self.state.y + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'orchid2', outline = "")

        if (self.state.goalx == 0 or self.state.goaly == 0):
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
            if (self.state.goalx == 0):
                x0 = 3 + (self.state.goalx) * (W + 1) / gridSize
            if (self.state.goaly == 0):
                y0 = 3 + (self.state.goaly) * (H + 1) / gridSize
        else :
            x0 = 1 + (self.state.goalx) * (W + 1) / gridSize
            y0 = 1 + (self.state.goaly) * (H + 1) / gridSize
        x1 = (self.state.goalx + 1) * (W + 1) / gridSize
        y1 = (self.state.goaly + 1) * (H + 1) / gridSize
        canvas.create_rectangle(x0,y0,x1,y1, fill = 'royalblue3', outline = "")
        #Add arrows
        for i in range (gridSize) :
            for j in range (gridSize) :
                if (j == 0 or i == 0):
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                    if (i == 0):
                        x0 = 3 + (i) * (W + 1) / gridSize
                    if (j == 0):
                        y0 = 3 + (j) * (H + 1) / gridSize
                else :
                    x0 = 1 + (i) * (W + 1) / gridSize
                    y0 = 1 + (j) * (H + 1) / gridSize
                x1 = (i + 1) * (W + 1) / gridSize
                y1 = (j + 1) * (H + 1) / gridSize
                #if(i == 0 or i == gridSize - 1 or j == 0 or j == gridSize - 1):
                v = np.array([i / float(self.state.grid_size), j / float(self.state.grid_size), self.state.goalx / float(self.state.grid_size), self.state.goaly / float(self.state.grid_size)])
                v = np.reshape(v,[1,self.state_size])
                act_values = agent.model.predict(v)
                action = np.argmax(act_values[0])
                if(action == 0):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (1 / 4) * x1 + (3 / 4) * x0
                    by1 = y0
                    bx2 = (1 / 4) * x1 + (3 / 4) * x0
                    by2 = y1
                    canvas.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    canvas.create_line(x0 + 1,my,bx1 + 5,by1 + 5, fill = 'yellow')
                    canvas.create_line(x0 + 1,my,bx2 + 5,by2 - 5, fill = 'yellow')
                if(action == 1):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = (3 / 4) * x1 + (1 / 4) * x0
                    by1 = y0
                    bx2 = (3 / 4) * x1 + (1 / 4) * x0
                    by2 = y1
                    canvas.create_line(x0 + 1,my,x1 - 1,my, fill = 'yellow')
                    canvas.create_line(x1 - 1,my,bx1 - 5,by1 + 5, fill = 'yellow')
                    canvas.create_line(x1 - 1,my,bx2 - 5,by2 - 5, fill = 'yellow')
                if(action == 2):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (1 / 4) * y1 + (3 / 4) * y0
                    bx2 = x1
                    by2 = (1 / 4) * y1 + (3 / 4) * y0
                    canvas.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    canvas.create_line(mx,y0 + 1,bx1 + 5,by1 + 5 , fill = 'yellow')
                    canvas.create_line(mx,y0 + 1,bx2 - 5,by2 + 5, fill = 'yellow')
                if (action == 3):
                    mx = (x0 + x1) / 2
                    my = (y0 + y1) / 2
                    bx1 = x0
                    by1 = (3 / 4) * y1 + (1 / 4) * y0
                    bx2 = x1
                    by2 = (3 / 4) * y1 + (1 / 4) * y0
                    canvas.create_line(mx,y0 + 1,mx,y1 - 1 , fill = 'yellow')
                    canvas.create_line(mx,y1 - 1,bx1 + 5,by1 - 5 , fill = 'yellow')
                    canvas.create_line(mx,y1 - 1,bx2 - 5,by2 - 5, fill = 'yellow')
        self.canvasMap = canvas
        return canvas