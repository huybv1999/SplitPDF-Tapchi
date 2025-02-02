import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit,  QPushButton, QTextEdit, QVBoxLayout, QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon
from PyQt6 import uic
import fitz
import re
import os

def resource_path(relative_path):
   
        if hasattr(sys, '_MEIPASS'):  # _MEIPASS is set by PyInstaller
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

class Myapp(QMainWindow):
    

    def __init__(self):
        super().__init__()
        uic.loadUi(resource_path('pdfGUI.ui'), self)
        self.setWindowTitle('Tach pdf theo ten tac gia')
        self.BrowseButton.clicked.connect(self.Browse)
        self.actionClose.triggered.connect(self.menuMenu.hide)
        self.actionQuit.triggered.connect(QApplication.instance().quit)
        self.executeButton.clicked.connect(self.Execution)
        self.ArticleButton.clicked.connect(self.Count_Article)
        
        # self.resize(500, 350)

    
    
    def Browse(self):
        dialog = QFileDialog()  
        dialog.setNameFilter("PDF Files (*.pdf)")
        if dialog.exec():  # This checks if the dialog was successful (returns 1 for success)
            selectedFile = dialog.selectedFiles()  # This returns a list of selected files
            if selectedFile:  # Check if the list is not empty
                self.FileLocation.setText(selectedFile[0])
                
    def split_pdf_by_content(self, pdf_path):
        self.Log.setPlainText("")
        doc = fitz.open(pdf_path)
        count = 0
        current_page = 0
        lastcount = 0
        for page in range(0, len(doc)):
            pagetext = doc.load_page(page)
            text = pagetext.get_text()
            count += 1
            # Check if the desired content is present
            nameregex = re.compile(r"Th[oòóôõơ]ng\s+tin\s+(?:c[aáàảãạ]c\s+)?t[aáàảãạâấầẩẫậăắằẳẵặ]c\s+gi[aáàảãạ]", flags=re.MULTILINE)
            MatchedTextArray = nameregex.findall(text)
            if MatchedTextArray:
                # Create a new PDF document
                new_doc = fitz.open()

                # Insert n pages from the original document into the new document
                for i in range(lastcount, count):
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)

                # Save the new document
                output_filename = f'splitResult/{lastcount+1}-{count}.pdf'
                new_doc.save(output_filename)
                new_doc.close()
                self.Log.insertPlainText(f"Created: {output_filename}\n")

                lastcount = count



        doc.close()    
            
    def Execution(self):
        PATH = 'splitResult'
        if not os.path.exists(PATH):
            os.makedirs(PATH)
        selected_path = self.FileLocation.toPlainText()
        self.split_pdf_by_content(selected_path)

    def Count_Article(self):
        self.Log.setPlainText("")
        selected_path = self.FileLocation.toPlainText()
        doc = fitz.open(selected_path)
        chu_de_section = ""
        
        for page in range(0, 2):
            pagetext = doc.load_page(page)
            text = pagetext.get_text()
            if page == 0:
                chu_de_section += text.split("CHỦ ĐỀ", 1)[-1]
            else:
                chu_de_section += text.split("thiết kế:", 1)[-1]
        article_pattern = re.compile(r'^\d+\s', re.MULTILINE)
        articles = article_pattern.findall(chu_de_section)
        self.Log.insertPlainText(str(len(articles)) + " bài")


def Start():
    m = Myapp()
    m.show()
    return m

if __name__ == '__main__':

    app = QApplication(sys.argv)
    # app.setStyleSheet('''
    #     QWidget {
    #         font-size: 25px;
    #     }
    #     QPushButton {
    #         font-size: 20px;
    #     }
    # ''')
    # myApp = Myapp()
    # myApp.show()
    window = Start()
    
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing windows')