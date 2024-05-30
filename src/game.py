from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QPoint
from functools import partial
from tictactoe import TicTacToe

class Game(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._tictactoe = TicTacToe()

        self.setGeometry(450, 70, 500, 450)

        self.dragging = False
        self.dragStartPosition = QPoint()

        self.setWindowTitle("Tic Tac Toe")
        self.initialize_gui()
        self.show()

    def initialize_gui(self):
        self.page = QtWidgets.QWidget()
        self.page.setStyleSheet("QWidget {background-color: white; border-radius: 5px;}")
        self.vLayout = QtWidgets.QVBoxLayout()

        self.vLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.page.setLayout(self.vLayout)
        self.setCentralWidget(self.page)

        self.gLayout = QtWidgets.QGridLayout()
        self.vLayout.addLayout(self.gLayout)
        self.create_grid()
        self.add_control_buttons()
        self.init_game()

    def init_game(self):
        self.clickList = [''] * 9
        self.win = False
        self._tictactoe.__init__()

    def create_grid(self):
        self.buttons = []
        for index in range(9):
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(
                "QPushButton {background-color: white; border: 2px solid grey; border-radius: 5px;}")
            self.gLayout.addWidget(btn, index // 3, index % 3)
            btn.clicked.connect(partial(self.make_user_move, btn, index))
            self.buttons.append(btn)

    def add_control_buttons(self):
        self.vLayout.addSpacing(10)
        self.buttonLayout = QtWidgets.QHBoxLayout()

        self.playAgainButton = self.create_restart_button()
        self.buttonLayout.addWidget(self.playAgainButton)

        self.vLayout.addLayout(self.buttonLayout)

    def create_restart_button(self):
        button = QtWidgets.QPushButton()
        button.setText("Start a new game")
        button.setFixedSize(190, 48)
        button.clicked.connect(self.new_game)
        button.setStyleSheet(
            "background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; border-radius: 5px; font-size: 16px; font-weight: 700;")
        return button

    def make_user_move(self, btn, index):
        if self.clickList[index] == '':
            self.clickList[index] = 'X'
            self._tictactoe.set_move(index)
            btn.setText("X")
            btn.setStyleSheet("QWidget {background-color: white; border: 2px solid grey; color: blue; font-size: 55px;}")
            btn.setEnabled(False)

            if self.check_game_state():
                return
            
            self.make_computer_move()

    def make_computer_move(self):
        index = self._tictactoe.get_move()
        if index is not None:
            self.clickList[index] = 'O'
            btn = self.buttons[index]
            self._tictactoe.set_move(index)
            btn.setText("O")
            btn.setStyleSheet("QWidget {background-color: white; border: 2px solid grey; color: red; font-size: 55px;}")
            btn.setEnabled(False)

            self.check_game_state()

    def check_game_state(self):
        player = 'X'
        if self._tictactoe.check_winner(player):
            self.game_over(player)
            return True
        
        player = 'O'
        if self._tictactoe.check_winner(player):
            self.game_over(player)
            return True

        if not self._tictactoe.get_empty_positions():
            QMessageBox.information(self, "Result", "It's draw")
            self.disable_buttons()
            return True

        return False

    def game_over(self, player):
        QMessageBox.information(self, "Result", f"Player {player} Won!!")
        self.disable_buttons()
        self.win = True
        self._tictactoe.__init__()

    def enable_buttons(self):
        for btn in self.buttons:
            btn.setEnabled(True)

    def disable_buttons(self):
        for btn in self.buttons:
            btn.setEnabled(False)

    def new_game(self):
        self.init_game()
        self.clear_buttons()
        self.enable_buttons()

    def clear_buttons(self):
        for btn in self.buttons:
            btn.setText("")
            btn.setStyleSheet(
                "QPushButton {background-color: white; border: 2px solid grey; border-radius: 5px;}")

def quit_app():
    QtWidgets.qApp.quit()