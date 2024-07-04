import sys
from PyQt6.QtWidgets import QApplication
from ImageDuplicateFinder.view.mainWindow import DuplicateImageFinderGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DuplicateImageFinderGUI()
    window.show()
    sys.exit(app.exec())
