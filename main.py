from PyQt6.QtWidgets import QInputDialog, QMainWindow, QApplication, QMenuBar, QMenu, QFileDialog, QTextEdit, QHBoxLayout
from PyQt6.QtGui import QAction, QTextCursor, QColor
from PyQt6.QtCore import Qt
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Notepad")
        self.setGeometry(100, 100, 400, 300)

        self.currentFile = None

        # THE EDITFIELD
        self.editField = QTextEdit(self)
        self.setCentralWidget(self.editField)

        # THE MENUBAR
        menubar = QMenuBar(self)
        menubar.setNativeMenuBar(False)
        self.setMenuBar(menubar)

        # FILE MENU
        fileMenu = QMenu("File", self)
        menubar.addMenu(fileMenu)

        # CREATE ACTIONS
        newAction = QAction("New", self)
        fileMenu.addAction(newAction)
        newAction.triggered.connect(self.newFile)

        openAction = QAction("Open", self)
        fileMenu.addAction(openAction)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction("Save", self)
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.saveFile)

        saveAsAction = QAction("Save As", self)
        fileMenu.addAction(saveAsAction)
        saveAsAction.triggered.connect(self.saveFileAs)

        # CREATE EDIT MENU
        editMenu = QMenu("Edit", self)
        menubar.addMenu(editMenu)

        undoAction = QAction("Undo", self)
        editMenu.addAction(undoAction)
        undoAction.triggered.connect(self.editField.undo)

        redoAction = QAction("Redo", self)
        editMenu.addAction(redoAction)
        redoAction.triggered.connect(self.editField.redo)

        cutAction = QAction("Cut", self)
        editMenu.addAction(cutAction)
        cutAction.triggered.connect(self.editField.cut)

        pasteAction = QAction("Paste", self)
        editMenu.addAction(pasteAction)
        pasteAction.triggered.connect(self.editField.paste)

        copyAction = QAction("Copy", self)
        editMenu.addAction(copyAction)
        copyAction.triggered.connect(self.editField.copy)

        findAction = QAction("Find", self)
        editMenu.addAction(findAction)
        findAction.triggered.connect(self.findText)


    def newFile(self):
        print("Creating new file")
        self.editField.clear()
        self.currentFile = None

    def openFile(self):
        print("Opening a file")
        filePath, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);; Python Files (*.py)")
        with open(filePath, "r") as file:
            text = file.read()
            self.editField.setText(text)

    def saveFileAs(self):
        print("Saving file as")
        filePath, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*);; Python Files (*.py)")
        if filePath:
            with open(filePath, "w") as file:
                file.write(self.editField.toPlainText())  # Write notepad contents to file
            self.currentFile = filePath

    def saveFile(self):
        print("Saving file")
        if self.currentFile:
            with open(self.currentFile, "w") as file:
                file.write(self.editField.toPlainText())
        else:
            self.saveFileAs()

    def findText(self):
        print("Finding text")
        searchTerm, ok = QInputDialog.getText(self, "Find text", "Search for")
        if ok:
            matchingWords = []  # To hold info about the selected text
            self.editField.moveCursor(QTextCursor.MoveOperation.Start)  # Put cursor to beginning of text
            highlightColor = QColor(Qt.GlobalColor.yellow)
            while self.editField.find(searchTerm):  # Finds text(s) that user is looking for
                # Highlight matches with yellow color
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(highlightColor)
                selection.cursor = self.editField.textCursor()

                matchingWords.append(selection)
            self.editField.setExtraSelections(matchingWords)



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
