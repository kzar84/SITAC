from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sitac_ui


class SitacApp(QtWidgets.QMainWindow, sitac_ui.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        # Connect the buttons
        self.settingsButton.clicked.connect(lambda: self.goToPage(1)) 
        self.homeButton.clicked.connect(lambda: self.goToPage(0))


    # Functions for the clock
    def goToPage(self, i):
        self.pages.setCurrentIndex(i)


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = SitacApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    sys.exit(app.exec_())                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()
