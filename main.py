# Created by - Haylton Santos
# LinkedIn - www.linkedin.com/in/hayltonevangelista/
# GitHub - www.github.com/hayltonssantos

from util import *
from screenPass import main

app = QtWidgets.QApplication([])
telaLogin = uic.loadUi("ui/login.ui")
telaSingUp = uic.loadUi("ui/SingUp.ui")
telaAlert = uic.loadUi("ui/alerta.ui")
conn = sqlite3.connect('password.db')
cursor = conn.cursor()


class SingUp():
    #Volta a tela de login
    def back():
        telaLogin.show()
        telaSingUp.hide()

    #Cadastro de user no banco de dados
    def cadastro():
        telaLogin.hide()
        telaSingUp.show()
        telaSingUp.boxPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        telaSingUp.btBack.clicked.connect(lambda: SingUp.back())
        telaSingUp.btCad.clicked.connect(
            lambda: SingUp.insertUser(telaSingUp.boxName.text(),
                                      telaSingUp.boxEmail.text(),
                                      telaSingUp.boxPassword.text())
        )

    #Insere usuario no banco de dados
    def insertUser(name, email, password):
        cursor.execute("""
                INSERT INTO user (name, email, password) VALUES (?,?,?)
            """, (name, email, password))
        conn.commit()

        telaSingUp.boxName.setText("")
        telaSingUp.boxEmail.setText("")
        telaSingUp.boxPassword.setText("")

        telaSingUp.hide()
        telaAlert.show()
        telaAlert.btOk.clicked.connect(lambda: SingUp.screenLogin(email))

    def screenLogin(email):
        telaAlert.hide()
        telaLogin.boxEmail.setText(email)
        telaLogin.show()


class login():
    def login():
        email = telaLogin.boxEmail.text()
        password = telaLogin.boxPassword.text()
        cursor.execute("""
                SELECT * FROM user WHERE email = ? AND password = ?
            """, (email, password))
        user = cursor.fetchone()
        if user is None:
            telaAlert.show()
            telaAlert.labelAlert.setText("User or password incorrect")
            telaAlert.btOk.clicked.connect(lambda: telaAlert.hide())
        else:
            main.ini(email)
            telaLogin.hide()


class createDb():
    def create():
        cursor.execute(
            """
    CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    email TEXT NOT NULL 
    );"""
        )
        conn.commit()
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email	TEXT NOT NULL UNIQUE,
    name	TEXT NOT NULL,
    password	TEXT NOT NULL
    );""")
        conn.commit()


class playScreen():
    def init():
        createDb.create()
        telaLogin.show()
        telaLogin.boxPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        #email = telaLogin.boxEmail.text()
        #password = telaLogin.boxPassword.text()

        telaLogin.btSingUp.clicked.connect(lambda: SingUp.cadastro())
        telaLogin.btLogin.clicked.connect(lambda: login.login())
        app.exec_()


if __name__ == '__main__':
    playScreen.init()
