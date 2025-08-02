from PySide6.QtWidgets import QApplication
from gui import DocumentUploader

if "__main__":
    app = QApplication([])
    window = DocumentUploader()
    window.show()
    app.exec()


## To do

# Improve visualization json - text in output panel
# Implement all the LLM
# Change paths to .env file