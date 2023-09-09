import PySimpleGUI as sg
import PVPWindow
import PVEWindow


if __name__ == '__main__':

    sg.theme("LightGreen4")

    layout = [
        [sg.Text("Tic Tac Toe!")],
        [sg.Button("Player VS Player")],
        [sg.Button("Player VS Computer")],
        [sg.Button("Exit")]
    ]

    startScreen = sg.Window("Tic Tac Toe", layout, size=(500, 500), element_padding=5, margins=(0, 150), element_justification="center")

    while True:
        event, values = startScreen.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Player VS Player":
            PVP = PVPWindow.PVPWindow()

        if event == "Player VS Computer":
            PVE = PVEWindow.PVEWindow()