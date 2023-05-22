"""A module containing the UI app"""
import os
import cv2 as cv
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton
import cartoonize as ct


class App(QWidget):
    """A class containing the instructions for the user interface"""

    inputFile = ''
    outputFile = ''
    cartoonType = 'Type 1'

    def __init__(self):
        super().__init__()
        self.title = 'Cartoon creator'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.inputVideoTextbox = QLineEdit(self)
        self.inputVideoTextbox.move(50, 50)
        self.inputVideoTextbox.resize(280, 40)

        inputVideoLabel = QLabel('Input video directory', self)
        inputVideoLabel.move(130, 15)

        or1Label = inputVideoLabel = QLabel('or', self)
        or1Label.move(390, 60)

        inputVideoButton = QPushButton('Browse', self)
        inputVideoButton.setToolTip('Search for the file')
        inputVideoButton.move(450, 55)
        inputVideoButton.clicked.connect(self.openFileNameDialog)

        self.outputVideoTextbox = QLineEdit(self)
        self.outputVideoTextbox.move(50, 150)
        self.outputVideoTextbox.resize(280, 40)

        outputVideoLabel = QLabel('Save output as', self)
        outputVideoLabel.move(145, 115)

        or2Label = QLabel('or', self)
        or2Label.move(390, 160)

        outputVideoButton = QPushButton('Browse', self)
        outputVideoButton.setToolTip('Save the file directly')
        outputVideoButton.move(450, 155)
        outputVideoButton.clicked.connect(self.saveFileDialog)

        cartoonizationButton = QPushButton('Options', self)
        cartoonizationButton.setToolTip(
            'Select the type of cartoonization process')
        cartoonizationButton.move(255, 250)
        cartoonizationButton.clicked.connect(self.getChoice)

        cartoonizationLabel = QLabel('Select the type of cartoonization', self)
        cartoonizationLabel.move(210, 225)

        runButton = QPushButton('Run', self)
        runButton.setToolTip('Run the program')
        runButton.move(200, 300)
        runButton.resize(200, 50)
        runButton.clicked.connect(self.run_on_click)

        self.show()

    def run_on_click(self):
        """A function containing the instructions which are executed after pressing the runButton"""
        self.inputFile = self.inputVideoTextbox.text()
        self.outputFile = self.outputVideoTextbox.text()
        self.run()

    def openFileNameDialog(self):
        """A function opening the file explorer in order to load a file"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            self.inputVideoTextbox.setText(fileName)

    def saveFileDialog(self):
        """A function opening the file explorer in order to save a file"""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(
            self, "Save as", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            self.outputVideoTextbox.setText(fileName)

    def getChoice(self):
        """A funtion which allows to choose the processing method"""
        items = ("Type 1", "Type 2", "Type 3",
                 "Pencil sketch 1", "Pencil sketch 2")
        item, okPressed = QInputDialog.getItem(
            self, "Cartoonization choice", "Type:", items, 0, False)
        if okPressed and item:
            print(item)
            self.cartoonType = item

    def run(self):
        """A function containing the main set of instructions which are executed after pressing the runButton"""
        fileExists = os.path.isfile(self.inputFile)

        if fileExists is False:
            print("""Error:File does not exist\n
            Check the spelling of the name, file
            extension or check if the file is in the right directory\n""")
            return None

        __cap = cv.VideoCapture(self.inputFile)

        try:
            __cap.isOpened()
        except:
            print("%s file couldn't be opened" % self.inputFile)

        __height = int(__cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        __width = int(__cap.get(cv.CAP_PROP_FRAME_WIDTH))
        __fps = int(__cap.get(cv.CAP_PROP_FPS))
        __fourcc = cv.VideoWriter_fourcc(*'mp4v')

        try:
            output = cv.VideoWriter(self.outputFile, __fourcc,
                                    __fps, (__width, __height))
        except:
            print("File cannot be saved")

        cv.namedWindow("Video Player")
        cv.resizeWindow("Video Player", 1280, 720)

        while __cap.isOpened():
            __success, __frame = __cap.read()
            if __success:
                __frame = ct.cartoonize(__frame, self.cartoonType)
                cv.imshow("Video Player", __frame)
                output.write(__frame)
            else:
                break

            __quitKey = cv.waitKey(int(1/__fps*1000)) & 0xFF == 27
            __closeButton = cv.getWindowProperty(
                "Video Player", cv.WND_PROP_VISIBLE) < 1

            if __quitKey or __closeButton:
                break

        __cap.release()
        output.release()
        cv.destroyAllWindows()
