from PySide6.QtWidgets import QApplication
from gui import DocumentUploader

if "__main__":
    app = QApplication([])
    window = DocumentUploader()
    window.show()
    app.exec()

