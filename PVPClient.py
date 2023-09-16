import socket
import pygame
import PySimpleGUI as sg

class PVPClient:

    def __init__(self):

        self.oPicture = pygame.image.load('Images/oPicture.png')
        self.xPicture = pygame.image.load('Images/xPicture.png')

        self.xTurn = True
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.2.100"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.playerX = True  # this should be reassigned later depeneding on which player it is

        if self.connect()[-1] == "2":
            self.playerX = False

        self.gameStart()


    def connect(self):
        try:
            self.client.connect(self.addr)
            self.send("connected")
            return self.client.recv(2048).decode()  #once it connects, we want to send information back to the connecting object
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()

        except socket.error as e:
            print(e)



    def drawBoard(self, gameWindow):
        pygame.draw.rect(gameWindow, (225, 225, 225), (0, 0, 600, 600)) #draws background

        for i in range(3):  # this loop draws all the light colored rectangles on the board
            for j in range(3):
                if i % 2 == 0:
                    if j % 2 == 0:
                        pygame.draw.rect(gameWindow, (225, 198, 153), (j * 200, i * 200, 200, 200))
                elif i % 2 != 0:
                    if j % 2 != 0:
                        pygame.draw.rect(gameWindow, (225, 198, 153), (j * 200, i * 200, 200, 200))

        #draws x's and o's that have already been played
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "x":
                    gameWindow.blit(self.xPicture, (j * 200, i * 200))
                elif self.board[i][j] == "o":
                    gameWindow.blit(self.oPicture, (j * 200, i * 200))

    def determineSquare(self, x, y):
        result = [0,0]
        if y >= 0 and y <= 200:  # first row
            result[0] = 0
            if x >= 0 and x <= 200:  # first column
                result[1] = 0
            elif x > 200 and x <= 400:  # second column
                result[1] = 1
            elif x > 400 and x <= 600:  # third column
                result[1] = 2

        if y > 200 and y <= 400:  # second row
            result[0] = 1
            if x >= 0 and x <= 200:  # first column
                result[1] = 0
            elif x > 200 and x <= 400:  # second column
                result[1] = 1
            elif x > 400 and x <= 600:  # third column
                result[1] = 2

        if y > 400 and y <= 600:  # third row
            result[0] = 2
            if x >= 0 and x <= 200:  # first column
                result[1] = 0
            elif x > 200 and x <= 400:  # second column
                result[1] = 1
            elif x > 400 and x <= 600:  # third column
                result[1] = 2

        return result

    def isBoardFull(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    def checkForWinner(self):
        for player in ["x","o"]:
            if self.board[0][0] == player:
                if self.board[0][1] == player: #first row
                    if self.board[0][2] == player:
                        return True
                if self.board[1][1] == player: #downward diagonal
                    if self.board[2][2] == player:
                        return True
                if self.board[1][0] == player: #first column
                    if self.board[2][0] == player:
                        return True

            if self.board[1][0] == player:  # second row
                if self.board[1][1] == player:
                    if self.board[1][2] == player:
                        return True

            if self.board[0][1] == player:  # second column
                if self.board[1][1] == player:
                    if self.board[2][1] == player:
                        return True

            if self.board[2][0] == player:  # upward diagonal
                if self.board[1][1] == player:
                    if self.board[0][2] == player:
                        return True

            if self.board[2][2] == player:
                if self.board[2][1] == player: #third row
                    if self.board[2][0] == player:
                        return True
                if self.board[1][2] == player:
                    if self.board[0][2] == player:
                        return True

        return False

    def readStr(self, str): #converts string to a board array. "[0,0,x][0,0,o][0,0,0]" --> [[0,0,x][0,0,o][0,0,0,]]
        board = [[],[],[]]

        newStr = str[1: len(str)-1] #gets rid of first and last sqaure brackets
        newArr = newStr.split("][")  #creates an array with 3 strings, each being a row of the board

        for i in range(3):
            for item in newArr[i].split(","):
                if item == "0":
                    board[i].append(0)
                else:
                    board[i].append(item)

        return board

    def readBoard(self): #converts self.board to a string to send to the server. [[0,0,x][0,0,o][0,0,0,]] --> "[0,0,x][0,0,o][0,0,0]"
        myString = ""

        for i in range(3):
            myString += "["
            for j in range(3):
                myString += str(self.board[i][j])
                if j < 2:
                    myString += ","
            myString += "]"

        return myString

    def endGame(self, winner):

        sg.theme("LightGreen4")

        layout = [
            [sg.Text("Game Over!")],
            [sg.Text('Winner: ' + winner)],
            [sg.Button("Exit")]
        ]

        gameOverScreen = sg.Window("TicTacToe", layout, size=(350, 250), margins=(0, 75), element_justification="center")

        while True:
            event, values = gameOverScreen.read()

            if event == "Exit" or event == sg.WIN_CLOSED:
                self.running = False
                
                gameOverScreen.close()
                break

    def gameStart(self):

        print(f"Game Starting, I am player \"X\": {self.playerX}")
        pygame.init()
        gameWindow = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Online PvP")

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if event.type == pygame.MOUSEBUTTONDOWN:  #if a mouse click occurs
                    mx, my = pygame.mouse.get_pos()  #sets mx,my to mouse coordinates

                    squarePressed = self.determineSquare(mx, my)  #determines which square was pressed
                    row = squarePressed[0]
                    column = squarePressed[1]
                    if self.board[row][column] == 0: #if the sqaure is empty, places a symbol of whoever's turn it is

                        if self.playerX and self.xTurn: #it is x's turn
                            self.board[row][column] = "x"
                            self.xTurn = False

                            self.send(self.readBoard()) #after making a move, sends the updated board to the server

                            while True:
                                connection, addr = self.client.accept()
                                response = connection.recv(2048).decode("utf-8")
                                if response:
                                    self.board = self.readStr(response)
                                    break

                        elif not self.playerX and not self.xTurn: #it is o's turn
                            self.board[row][column] = "o"
                            self.xTurn = True

                            self.send(self.readBoard()) #after making a move, sends the updated board to the server

                            while True:
                                connection, addr = self.client.accept()
                                response = connection.recv(2048).decode("utf-8")
                                if response:
                                    self.board = self.readStr(response)
                                    break



            self.drawBoard(gameWindow)
            pygame.display.update()

            if self.checkForWinner():  #checks if the game is over
                if self.xTurn:  #if it is x's turn, the last move played was by o, therefore o wins
                    winner = "o"
                else:  #otherwise x wins
                    winner = "x"
                self.endGame(winner)  #create the end game screen

            elif self.isBoardFull():
                self.endGame("Tie!")


        pygame.quit()



c = PVPClient()