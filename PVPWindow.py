import pygame
import PySimpleGUI as sg

class PVPWindow:
    def __init__(self):

        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]

        self.oPicture = pygame.image.load('Images/oPicture.png')
        self.xPicture = pygame.image.load('Images/xPicture.png')

        self.create()


    def create(self):

        xTurn = True #sets turn to "x" player at the start of the game

        pygame.init()
        gameWindow = pygame.display.set_mode((600, 600))
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

                    squarePressed = self.determineSquare(mx, my)  #determines which square was pressed
                    row = squarePressed[0]
                    column = squarePressed[1]
                    if self.board[row][column] == 0: #if the sqaure is empty, places a symbol of whoever's turn it is

                        if xTurn: #it is x's turn
                            self.board[row][column] = "x"
                            xTurn = False
                        else: #it is o's turn
                            self.board[row][column] = "o"
                            xTurn = True


            self.drawBoard(gameWindow)
            pygame.display.update()  #update all visuals

            if self.checkForWinner():  #checks if the game is over
                if xTurn:  #if it is x's turn, the last move played was by o, therefore o wins
                    winner = "o"
                else:  #otherwise x wins
                    winner = "x"
                self.endGame(winner)  #create the end game screen

            elif self.isBoardFull():
                self.endGame("Tie!")

        pygame.quit()

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