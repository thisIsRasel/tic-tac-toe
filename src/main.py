import sys
from PyQt5 import QtWidgets
from game import Game

def main():
    app = create_app()
    Game()
    sys.exit(app.exec_())

def create_app():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')
    return app

if __name__ == '__main__':
    main()
