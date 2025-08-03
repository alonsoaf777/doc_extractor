import os
import json
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLabel, QFileDialog, QTextEdit, QSizePolicy, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from utils.file_loader import load_file_image, extract_text_from_pdf, extract_and_clean
from ocr.ocr_utils import extract_text_from_rois
from handlers.estate_parser import text_completion

class DocumentUploader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Uploader - Estate & Tax Documents")
        self.setGeometry(300, 300, 900, 500)
        self.init_ui() 

        self.doc_type = None
        self.file_selected = False
        self.processed_data = None
        self.num_pages = None

    def init_ui(self):
        '''
        Create widgets and create the main UI
        '''
        main_layout = QHBoxLayout()  # Principal layout. Left file selection - Right display

        # Left panel: Document info
        self.left_panel = QVBoxLayout()
        self.label_info = QLabel("No file selected.")
        self.label_info.setAlignment(Qt.AlignTop)
        self.label_info.setWordWrap(True)

        #Select document
        self.btn_select_file = QPushButton("Select Document")
        self.btn_select_file.clicked.connect(self.select_file)

        #List
        self.list_select_type = QListWidget()
        self.list_select_type.addItems(["Power of Attorney", "Tax return"])
        self.list_select_type.itemClicked.connect(self.type_file_select)

        #Process file
        self.btn_process_file = QPushButton("Process file")
        self.btn_process_file.clicked.connect(self.process_file)

        #Processing messages
        self.label_time = QLabel("")
        self.label_time.setAlignment(Qt.AlignRight)
        self.label_processing = QLabel("")
        self.label_processing.setStyleSheet("color: gray; font-style: italic;")
        self.label_processing.setVisible(False)

        #Visualization
        self.view_mode = QComboBox()
        self.view_mode.addItems(["JSON", "Text"])
        self.view_mode.currentTextChanged.connect(self.update_output_view)

        ##Add widgets
        self.left_panel.addWidget(self.btn_select_file)
        self.left_panel.addWidget(self.label_info)
        self.left_panel.addWidget(self.list_select_type)
        self.left_panel.addWidget(self.btn_process_file)
        self.left_panel.addWidget(self.label_processing)
        self.left_panel.addStretch()

        # Right panel. Display
        self.right_panel = QVBoxLayout()
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_box.setPlaceholderText("Processed document content will appear here...")

        #Right panel widgets
        self.right_panel.addWidget(self.view_mode)
        self.right_panel.addWidget(self.output_box)
        self.right_panel.addWidget(self.label_time)     

        # Package panels
        main_layout.addLayout(self.left_panel, 1)
        main_layout.addLayout(self.right_panel, 2)

        self.setLayout(main_layout)
    
    def show_error(self, message):
        '''
        Pop up error handler.
        '''
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec()

    def select_file(self):
        '''
        After pressing select document button the path is taken from the
        document and saved.

        This functions asks for just .pdf extensions
        '''
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "PDF Files (*.pdf)"
        )

        if file_path:
            file_info = self.get_file_info(file_path)
            self.file_selected = True
            self.file_path = file_path
            self.label_info.setText(file_info)
            self.output_box.clear()

    def get_file_info(self, path: str) -> str:
        '''
        Obtain the information from the selected file
        '''
        try:
            file_name = os.path.basename(path)
            file_ext = os.path.splitext(path)[1]
            file_size = os.path.getsize(path) / 1024  # KB

            return (
                f"<b>File Name:</b> {file_name}<br>"
                f"<b>Extension:</b> {file_ext}<br>"
                f"<b>Full Path:</b> {path}<br>"
                f"<b>File Size:</b> {file_size:.2f} KB"
            )
        except Exception as e:
            self.show_error(f"Error reading file info: {str(e)}")
            return
    
    def type_file_select(self, item):
        '''
        Saves the type of file for later use
        '''
        self.doc_type = item.text()
    
    def process_file(self):
        '''
        OCR and LLM processing are used here.
        First error validation and cleaning practices.
        After processing the extracted data is saved for further formatting.
        '''
        if not self.doc_type:
            self.show_error("Please select a document type from the list.")
            return
        elif not self.file_selected:
            self.show_error("Select a file for processing.")
            return 
 
        # Clean last json
        self.output_box.clear()
        self.label_time.setText("")

        self.label_processing.setText("Processing... Please wait")
        self.label_processing.setVisible(True)

        self.setEnabled_all(False)
        self.repaint()  # refresh GUI

        start_time = time.time()
        # To do based on type of document
        try:
            if self.doc_type == "Power of Attorney":
                self.num_pages, info = extract_text_from_pdf(self.file_path)
                extracted_data = text_completion(info)
            elif self.doc_type == "Tax return":
                image = load_file_image(self.file_path) #pdf -> image
                extracted_data = extract_text_from_rois(image)

        except Exception as e:
            self.show_error(f"Processing failed: {str(e)}")
            extracted_data = None
        
        finally:
            self.processed_data = extracted_data #save data for further formatting
            self.update_output_view()  # View mode (JSON <-> Text)
            end_time = time.time()
            elapsed = end_time - start_time
            self.label_time.setText(f"Processed in {elapsed:.2f} seconds")
            
            self.setEnabled_all(True)
            self.label_processing.setVisible(False)

    def setEnabled_all(self, enabled: bool):
        '''
        Enable widgets
        '''
        self.btn_select_file.setEnabled(enabled)
        self.btn_process_file.setEnabled(enabled)
        self.list_select_type.setEnabled(enabled)
        self.view_mode.setEnabled(enabled)
    
    def update_output_view(self):
        '''
        Display JSON view or Text view
        '''
        if not self.processed_data:
            return

        mode = self.view_mode.currentText()

        if mode == "JSON":
            self.output_box.setPlainText(json.dumps(self.processed_data, indent=4))
        elif mode == "Text":
            try:
                formatted = self.format_pretty_text(self.processed_data)
                self.output_box.setPlainText(formatted)
            except Exception as e:
                self.show_error(f"Cannot convert to text: {str(e)}")
                self.output_box.setPlainText(json.dumps(self.processed_data, indent=4))
                

    def format_pretty_text(self, data: dict, indent: int = 0) -> str:
        '''
        Change text format
        '''
        lines = []
        spacing = "  " * indent
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{spacing}{key}:")
                lines.append(self.format_pretty_text(value, indent + 1))
            else:
                lines.append(f"{spacing}{key}: {value}")
        return "\n".join(lines)
    