# -*- coding : utf-8 -*-
# @File   : main.py
# @Time   : 2022/3/13
# @Author : Leonard
# @Email  : reguluslee@tom.com

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from interface import Ui_Form


class mainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        # self.lineEdit_1.setText("smtp-mail.outlook.com")
        # self.lineEdit_2.setText("587")
        # self.lineEdit_3.setText("***@outlook.com")
        # self.lineEdit_4.setText("***")
        self.pushButton_1.clicked.connect(self.fileChoose)
        self.pushButton_2.clicked.connect(self.sendMail)
        self.pushButton_3.clicked.connect(self.toolExit)

    def fileChoose(self, parent=None):
        filePath, fileType = QFileDialog.getOpenFileName(self, "打开", os.getcwd(), "PDF文件(*.pdf);;所有文件(*.*)")
        self.lineEdit_7.setText(filePath)

    def sendMail(self, parent=None):
        # mailServer = "smtp-mail.outlook.com"
        # mailPort = 587
        # senderAccount = "***@outlook.com"
        # senderPassword = "***"

        mailServer = self.lineEdit_1.text()
        mailPort = self.lineEdit_2.text()
        senderAccount = self.lineEdit_3.text()
        senderPassword = self.lineEdit_4.text()

        receiverAccount = self.lineEdit_5.text()
        topicText = self.lineEdit_6.text()
        mainText = self.plainTextEdit.toPlainText()

        # senderName = "Leonard"
        # receiverName = "Gloria"

        contentPart = MIMEText(mainText, "plain", "utf-8")
        msg = MIMEMultipart()
        msg.attach(contentPart)
        msg["Subject"] = topicText
        msg["From"] = senderAccount
        msg["To"] = receiverAccount

        if len(self.lineEdit_7.text()) != 0:
            appendixPath = self.lineEdit_7.text()
            appendixFile = open(appendixPath, "rb").read()
            appendixPart = MIMEApplication(appendixFile)
            appendixPart.add_header("Content-Disposition", "attachment",
                                    filename=os.path.basename(appendixPath))
            msg.attach(appendixPart)

        try:
            smtpObj = smtplib.SMTP(mailServer, mailPort)
            smtpObj.starttls()
            smtpObj.login(senderAccount, senderPassword)
            smtpObj.sendmail(senderAccount, receiverAccount, msg.as_string())
            self.lineEdit_9.setText("Successful")
        except smtplib.SMTPException:
            self.lineEdit_9.setText("Failed")

    def toolExit(self, parent=None):
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = mainWindow()
    myWin.show()
    sys.exit(app.exec_())
