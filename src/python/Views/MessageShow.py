from PyQt5.QtWidgets import QMessageBox

def warn(title, text):
    message = QMessageBox()
    message.setStyleSheet("""
    .QMessageBox{
        color: rgb(0, 243, 255);
        background-color: rgba(0, 0, 0, 200);
        border:1px solid rgba(0, 200, 200, 150);
    }
    """)
    message.setStyleSheet("""
    color: rgb(0, 243, 255);
    background-color: rgba(0, 0, 0, 200);
    """)

    message.setText(title)
    message.setInformativeText(text)
    message.setStandardButtons(QMessageBox.Ok)
    message.setIcon(QMessageBox.Warning)
    message.setModal(True)
    message.exec()

def question(title, text):
    message = QMessageBox()
    message.setStyleSheet("""
    color: rgb(0, 243, 255);
    background-color: rgba(0, 0, 0, 200);
    border:1px solid rgba(0, 200, 200, 150);
    """)
    message.setText(title)
    message.setInformativeText(text)
    message.setStandardButtons(QMessageBox.Ok)
    message.setIcon(QMessageBox.Question)
    message.setModal(True)
    message.exec()

def error(title, text):
    message = QMessageBox()
    message.setStyleSheet("""
    color: rgb(0, 243, 255);
    background-color: rgba(0, 0, 0, 200);
    border:1px solid rgba(0, 200, 200, 150);
    """)
    message.setText(title)
    message.setInformativeText(text)
    message.setStandardButtons(QMessageBox.Ok)
    message.setIcon(QMessageBox.Critical)
    message.setModal(True)
    message.exec()

def info(title, text):
    message = QMessageBox()
    message.setStyleSheet("""
    color: rgb(0, 243, 255);
    background-color: rgba(0, 0, 0, 200);
    border:1px solid rgba(0, 200, 200, 150);
    """)
    message.setText(title)
    message.setInformativeText(text)
    message.setStandardButtons(QMessageBox.Ok)
    message.setIcon(QMessageBox.Information)
    message.setModal(True)
    message.exec()