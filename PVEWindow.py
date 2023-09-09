import pygame
import PySimpleGUI as sg
import random
import time
import copy

class PVEWindow:
    def __init__(self):

        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]

        self.oPicture = pygame.image.load('Images/oPicture.png')
        self.xPicture = pygame.image.load('Images/xPicture.png')

        if random.randint(1,2) == 1: #generates a random integer between 1 and 2 to pick x or o for the player
            self.player = "x"
            self.computer = "o"
        else:
            self.player = "o"
            self.computer = "x"

        self.create()


    def create(self):

        xTurn = True #sets turn to "x" player at the start of the game

        pygame.init()
        gameWindow = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PvP TicTacToe")

        self.drawBoard(gameWindow)

        self.running = True
        while self.running:
            for event in pygame.event.get(): #loops through all current events
                if event.type == pygame.QUIT:  #closes when "x" is pressed
                    self.running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:  #if a mouse click occurs
                    mx, my = pygame.mouse.get_pos()  #sets mx,my to mouse coordinates

                    if mx < 600:  #ensures board interaction doesn't happen if the side menu is pressed
                        squarePressed = self.determineSquare(mx, my)  #determines which square was pressed
                        row = squarePressed[0]
                        column = squarePressed[1]
                        if self.board[row][column] == 0: #if the sqaure is empty, places a symbol of whoever's turn it is

                            if xTurn and self.player == "x": #it is x's turn
                                self.board[row][column] = "x"
                                xTurn = False
                            elif not xTurn and self.player == "o": #it is o's turn
                                self.board[row][column] = "o"
                                xTurn = True

                self.drawBoard(gameWindow)
                pygame.display.update()  # update all visuals

                winner = self.checkForWinner()  # checks if the game is over
                if winner != False:
                    self.endGame(winner)  # create the end game screen
                    break

                if self.isBoardFull():
                    self.endGame("Tie!")
                    break
                #computer's turn:
                if xTurn and self.computer == "x":  # it is x's turn
                    #computer makes a move, in the format of: self.board[row][column] == "x", for whichever row and column the computer chooses
                    moveChosen = self.randomBot()

                    computerRow = moveChosen[0]
                    computerColumn = moveChosen[1]

                    self.board[computerRow][computerColumn] = "x"
                    xTurn = False
                elif not xTurn and self.computer == "o":  # it is o's turn
                    # computer makes a move, in the format of: self.board[row][column] == "o", for whichever row and column the computer chooses
                    moveChosen = self.randomBot()

                    computerRow = moveChosen[0]
                    computerColumn = moveChosen[1]

                    self.board[computerRow][computerColumn] = "o"
                    xTurn = True

        pygame.quit()

    def drawBoard(self, gameWindow):
        pygame.draw.rect(gameWindow, (225, 225, 225), (0, 0, 600, 600)) #draws background
        pygame.draw.rect(gameWindow, (25, 175, 25), (600, 000, 200, 600))  # draws side menu background

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

        font = pygame.font.Font('freesansbold.ttf', 20)   #initializes the font

        playerIndicatorText = font.render('You play as: ' +  self.player, True, (255, 255, 255))  #creates a text to show what the player is playing as
        playerIndicatorTextRect = playerIndicatorText.get_rect()
        playerIndicatorTextRect.center = (700, 200)

        gameWindow.blit(playerIndicatorText, playerIndicatorTextRect)


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
                        return player
                if self.board[1][1] == player: #downward diagonal
                    if self.board[2][2] == player:
                        return player
                if self.board[1][0] == player: #first column
                    if self.board[2][0] == player:
                        return player

            if self.board[1][0] == player:  # second row
                if self.board[1][1] == player:
                    if self.board[1][2] == player:
                        return player

            if self.board[0][1] == player:  # second column
                if self.board[1][1] == player:
                    if self.board[2][1] == player:
                        return player

            if self.board[2][0] == player:  # upward diagonal
                if self.board[1][1] == player:
                    if self.board[0][2] == player:
                        return player

            if self.board[2][2] == player:
                if self.board[2][1] == player: #third row
                    if self.board[2][0] == player:
                        return player
                if self.board[1][2] == player:
                    if self.board[0][2] == player:
                        return player

        return False

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
                pygame.quit()
                gameOverScreen.close()
                break

    #various bot functions (these look at the board and return a move in the form of a coordinate list [x,y]

    def numberOfPossibleMoves(self):
        freeSpaces = 0
        for i in range(3):  # counts the number of available moves
            for j in range(3):
                if self.board[i][j] == 0:
                    freeSpaces += 1
        return freeSpaces

    def randomBot(self):

        freeSpaces = self.numberOfPossibleMoves()

        moveChoice = random.randint(1, freeSpaces) #picks one out of all the available moves
        currentMoveCounter = 0
        for i in range(3):
            for j in range(3): #loops through all avaialbe moves
                if self.board[i][j] == 0:
                    currentMoveCounter += 1
                    if currentMoveCounter == moveChoice: #if the current available move is the randomly chosen one, return it
                        return [i,j]

    def miniMaxBot(self): #x is the maximizing player
        pass


    def evaluate(self): #x winning is positive and o winning is negative
        if self.checkForWinner() == "x":
            return 100
        elif self.checkForWinner() == "o":
            return -100

        #2 sqaures in a row with the third being empty is worth 10 points
        #center sqaure is worth 5 points
        #1 square with 2 empty square beside it (in a line) is worth 1 point

