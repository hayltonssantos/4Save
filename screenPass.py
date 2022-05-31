# Created by - Haylton Santos
# LinkedIn - www.linkedin.com/in/hayltonevangelista/
# GitHub - www.github.com/hayltonssantos

from util import *

app = QtWidgets.QApplication([])
tela = uic.loadUi("ui/main.ui")

conn = sqlite3.connect('password.db')
cursor = conn.cursor()


class savePass():
    #Caso os campos sejam preenchidos manualmente, ele insere e caso exista ID faz update
    def savePassword():
        name = tela.boxName.text()
        password = tela.boxPass.text()
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        if tela.boxID.text() == "":
    
            cursor.execute(
                """
                INSERT INTO passwords (name, password, date,email) VALUES (?,?,?,?)
            """, (name, password, date, email)
            )
            conn.commit()
            showPass.showAllPass(email)

        else:

            cursor.execute(
                """
                UPDATE passwords SET name = ?, password = ?, date = ? WHERE id = ?
            """, (name, password, date, tela.boxID.text())
            )
            conn.commit()
            showPass.showAllPass(email)


class generatePass():

    global options
    options = string.ascii_letters + string.digits

    # Função para gerar senha tb faz update
    def generatePassword():
        name = tela.boxName.text()
        length = int(tela.boxQnt.text())
        date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        password = ""

        if tela.radioCaracters.isChecked():
            specialCaracter = 's'
        else:
            specialCaracter = 'n'

        for i in range(length):
            if specialCaracter.lower() == 'n':
                password += random.choice(options)
            if specialCaracter.lower() == 's':
                password += random.choice(string.printable)

        if tela.boxID.text() == "":
            cursor.execute(
                """
                INSERT INTO passwords (name, password, date,email) VALUES (?,?,?,?)
            """, (name, password, date, email)
            )
        else:
            cursor.execute(
                """
                UPDATE passwords SET name = ?, password = ?, date = ? WHERE id = ?
            """, (name, password, date, tela.boxID.text())
            )
        conn.commit()
        tela.boxID.setText("")
        tela.boxName.setText("")
        tela.boxPass.setText("")
        tela.boxQnt.setValue(0)
        showPass.showAllPass(email)
       


class showPass():
    # Função para mostrar todos os passwords / e buscar tb
    def showAllPass(email, search=""):
         
        if search == "":
            cursor.execute(
                """
                SELECT * FROM passwords WHERE email = ?;
            """, (email,))
            data = cursor.fetchall()

        elif search != "":
            cursor.execute(
                """
                SELECT * FROM passwords WHERE email = ? and name LIKE ? ;
            """, (email, '%'+search+'%',))
            data = cursor.fetchall()
        
        tela.lcdNumber.display(len(data))
        tela.tablePass.setRowCount(len(data))
        tela.tablePass.setColumnCount(5)

        for i in range(0, len(data)):
            for j in range(0, 4):
                if tela.checkBoxShowDigits.isChecked():
                    tela.tablePass.setItem(
                        i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
                else:
                    tela.tablePass.setItem(
                        i, j, QtWidgets.QTableWidgetItem(str(data[i][j])))
                    tela.tablePass.setItem(
                        i, 2, QtWidgets.QTableWidgetItem('**********'))

                button = QtWidgets.QPushButton("Remove")
                tela.tablePass.setCellWidget(i, 4, button)
                # Botao Remover
                button.clicked.connect(lambda: deletePass.deleteToName(data[QtWidgets.QTableWidget.currentRow(tela.tablePass)][0],
                                                                       data[QtWidgets.QTableWidget.currentRow(tela.tablePass)][1]))
                # Duplo Clique p/ Editar

                tela.tablePass.doubleClicked.connect(lambda:
                                                     getPass.getPassword(data[QtWidgets.QTableWidget.currentRow(tela.tablePass)][0],
                                                                         data[QtWidgets.QTableWidget.currentRow(
                                                                             tela.tablePass)][1],
                                                                         data[QtWidgets.QTableWidget.currentRow(tela.tablePass)][2]))


class getPass():
    # Função para pegar a senha e editar
    def getPassword(id, name, password):
        tela.boxID.setText(str(id))
        tela.boxName.setText(name)
        tela.boxPass.setText(password)


class deletePass():
    # Função para deletar a senha
    def deleteToName(id, name):
        cursor.execute(
            """
            DELETE FROM passwords WHERE id = ?;
        """, (id,)
        )
        
        conn.commit()
        showPass.showAllPass(email)


class main():
    # Incio do programa
    def ini(emailLogin):
        global email
        email = emailLogin
        tela.show()
        app.exec_()
        showPass.showAllPass(email)
        tela.btGenerate.clicked.connect(generatePass.generatePassword)
        tela.btSave.clicked.connect(savePass.savePassword)
        tela.checkBoxShowDigits.stateChanged.connect(lambda:showPass.showAllPass(email))
        tela.btSearch.clicked.connect(lambda:
                                      showPass.showAllPass(email, tela.boxSearch.text()))
        #      1. Generate a password
        #      2. Show all passwords
        #      3. Update a password
        #      4. Delete a password
        #      5. Exit


if __name__ == '__main__':

    pass
