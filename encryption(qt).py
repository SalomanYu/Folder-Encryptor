import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QCoreApplication
from ecnry_decry import encrypt_dirs, decrypt_dirs


class App(QWidget):
    def __init__(self):        
        super().__init__()

        self.initGui()
    

    def initGui(self):
        boxV = QVBoxLayout()
        boxH1 = QHBoxLayout()
        boxH2 = QHBoxLayout()

        main_label = QLabel(self, text='Mom will never khow.')
        main_label.setAlignment(Qt.AlignCenter)
        
        self.path_entry = QLineEdit(self)
        path_btn = QPushButton(text='Select a folder')

        encrypt_btn = QPushButton(self, text='Encrypt')
        decrypt_btn = QPushButton(self, text='Decrypt')

        exit_btn = QPushButton(self, text='To Finish')

        path_btn.clicked.connect(self.choiceDirectory)
        path_btn.setShortcut('Ctrl+O')
        encrypt_btn.clicked.connect(self.startEncryption)
        decrypt_btn.clicked.connect(self.startDecryption)
        exit_btn.clicked.connect(self.closeApp)

        boxV.addWidget(main_label)
        boxH1.addWidget(self.path_entry)
        boxH1.addWidget(path_btn)
        boxV.addLayout(boxH1)
        boxV.addStretch(1)
        boxH2.addWidget(encrypt_btn)
        boxH2.addWidget(decrypt_btn)
        boxV.addLayout(boxH2)
        boxV.addWidget(exit_btn)

        self.setLayout(boxV)
        self.setGeometry(900,500,400,120)
        self.setWindowTitle('Encryption & Decryption')
        self.setWindowIcon(QIcon('media/key.jpeg'))
        self.show()

    def choiceDirectory(self):
        path = QFileDialog.getExistingDirectory(self, 'Folder Choice')
        self.path_entry.setText(path)
        
    

    def startEncryption(self):
        path = self.path_entry.text()
        if len(path) > 3:
            password, response = QInputDialog.getText(self, 'Encryption', 'Create a password')
            if response:
                if len(password) > 0:
                    self.successMessage('Program is running. Wait...')
                    encrypt_dirs(path, password)
                    self.successMessage('The files were successfuly <b>encrypted</b>')
                else:
                    self.errorMessage('Password so short. Repeat.')
        else:
            self.errorMessage('Come back and select a folder')
    

    def startDecryption(self):
        path = self.path_entry.text()

        if len(path) > 3:    
            password, response = QInputDialog.getText(self, 'Decryption', 'Write the password')
            if response:
                if len(password) > 0:
                    self.successMessage('Program is running. Wait...')

                    if str(decrypt_dirs(path, password)) == 'Wrong password (or file is corrupted).':
                        self.errorMessage(message='Error! Wrong Password')
                    elif str(decrypt_dirs(path, password)) == 'Input and output files are the same.':
                        self.errorMessage(message='There are no encrypted files in the folder.')                    
                    else:
                        print(f'{decrypt_dirs(path, password)}')
                        self.successMessage(message='The files were successfuly <b>decrypted</b>')
                
        else:
            self.errorMessage('Come back and select a folder')

    def closeApp(self):
        QCoreApplication.instance().quit()
        

    def successMessage(self, message):
        QMessageBox.about(self, 'Success', message)


    def errorMessage(self, message):
        QMessageBox.about(self, 'Mom will never know.', message)

if __name__ == '__main__':
    run = QApplication(sys.argv)
    style = """
        QLabel{
            color: #2d424a  ;
            font-size:15px;
            
        }
        QLineEdit{
            color: #2d424a;
            border: 2px solid #b4786b ;
            border-radius: 6px;
            padding: 3px;
            font-size: 14px;
        }
        QWidget{
            background: #5f6468  ;
        }
        QPushButton{
            color: #2d424a;
            background: #b4786b;
            border: 2px solid #b4786b ;
            border-radius:6px;
            font-size: 15px;
            padding: 5px;
            outline: none;
        }
        QPushButton:hover{
            color: #b4786b;
            background: #2d424a;
        }
    """
    run.setStyleSheet(style)
    main = App()
    sys.exit(run.exec_())
