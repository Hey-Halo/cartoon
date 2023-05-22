"""The main file that runs the program"""
import sys
from PyQt5.QtWidgets import QApplication
import userInterface as UI


def main():
    """The main function that is used to run the program"""
    app = QApplication(sys.argv)
    ex = UI.App()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
