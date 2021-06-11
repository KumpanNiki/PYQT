import os
import sys
import sqlite3
from PyQt5.QtWidgets import QMainWindow, QListWidget, QLineEdit, QWidget, QMessageBox, QPushButton, QPlainTextEdit, \
    QLabel
from PyQt5 import QtCore, QtGui, QtWidgets

COMBINATION = {"qwe", "wer", "ert", "rty", "tyu", "yui", "uio", "iop",  # это комбинации рядом стоящих 3-х клавиш
               "asd", "sdf", "dfg", "fgh", "ghj", "hjk", "jkl", "zxc",
               "xcv", "cvb", "vbn", "bnm", "йцу", "цук", "уке", "кен",
               "енг", "нгш", "гшщ", "шщз", "щзх", "зхъ", "фыв", "ыва",
               "вап", "апр", "про", "рол", "олд", "лдж", "джэ", "жэё",
               "ячс", "чсм", "сми", "мит", "ить", "тьб", "ьбю", "123",
               "234", "345", "456", "567", "678", "789", "890"}

FILE = 'project'  # название базы данных
FORBIDDEN_CHARACTERS = '`~!@"№#$;%^:&?*()-_+={}[]<>,/|"\" '  # запрещенные символы


# классы возбуждаемых ошибок
class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


class MyWidget(QMainWindow):  # форма входа
    def setupUi(self, ENTER):
        ENTER.setObjectName("ENTER")
        ENTER.resize(793, 194)
        ENTER.setStyleSheet("")
        self.label_login = QtWidgets.QLabel(ENTER)  # метка логина
        self.label_login.setGeometry(QtCore.QRect(40, 20, 131, 41))
        self.label_login.setTextFormat(QtCore.Qt.AutoText)
        self.label_login.setObjectName("label_login")
        self.label_password = QtWidgets.QLabel(ENTER)  # метка пароля
        self.label_password.setGeometry(QtCore.QRect(10, 80, 191, 41))
        self.label_password.setObjectName("label_password")
        self.login = QtWidgets.QLineEdit(ENTER)  # логин
        self.login.setGeometry(QtCore.QRect(200, 20, 211, 41))
        self.login.setObjectName("login")
        self.password = QtWidgets.QLineEdit(ENTER)  # пароль
        self.password.setGeometry(QtCore.QRect(200, 70, 211, 41))
        self.password.setObjectName("password")
        self.label_question = QtWidgets.QLabel(ENTER)
        self.label_question.setGeometry(QtCore.QRect(70, 160, 211, 31))  # метка вопроса
        self.label_question.setObjectName("label_question")
        self.registration = QtWidgets.QPushButton(ENTER)  # кнопка регистрации
        self.registration.setGeometry(QtCore.QRect(290, 160, 131, 31))
        self.registration.setObjectName("registration")
        self.enter = QtWidgets.QPushButton(ENTER)  # кнопка входа
        self.enter.setGeometry(QtCore.QRect(290, 120, 121, 31))
        self.enter.setObjectName("enter")
        self.error_1 = QtWidgets.QLabel(ENTER)  # метка ошибки с логином
        self.error_1.setGeometry(QtCore.QRect(440, 20, 331, 81))
        self.error_1.setText("")
        self.error_1.setObjectName("error_1")
        self.error_2 = QtWidgets.QLabel(ENTER)  # метка ошибки с паролем
        self.error_2.setGeometry(QtCore.QRect(440, 70, 331, 41))
        self.error_2.setText("")
        self.error_2.setObjectName("error_2")

        self.retranslateUi(ENTER)
        QtCore.QMetaObject.connectSlotsByName(ENTER)

    def retranslateUi(self, ENTER):
        _translate = QtCore.QCoreApplication.translate
        ENTER.setWindowTitle(_translate("ENTER", "ВХОД"))
        self.label_login.setWhatsThis(_translate("ENTER",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\""
                                                 " \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\""
                                                 " /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'"
                                                 "; font-size:8pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\"-qt-paragraph-type:empty;"" margin-top:12px; "
                                                 "margin-bottom:12px;"" margin-left:0px; margin-right:0px;"
                                                 " -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_login.setText(_translate("ENTER",
                                            "<html><head/><body><p><span style=\""
                                            " font-size:16pt;\">ЛОГИН</span></p></body></html>"))
        self.label_password.setText(_translate("ENTER",
                                               "<html><head/><body><p><span style=\" font-size:16pt;"
                                               "\">ПАРОЛЬ</span></p></body></html>"))
        self.label_question.setText(_translate("ENTER",
                                               "<html><head/><body><p><span style=\" font-size:12pt; color:#0055ff;"
                                               "\">Впервые у нас ?</span></p></body></html>"))
        self.registration.setText(_translate("ENTER", "РЕГИСТРАЦИЯ"))
        self.enter.setText(_translate("ENTER", "ВОЙТИ"))
        self.enter.clicked.connect(self.run)
        self.registration.clicked.connect(self.registr)

    def run(self):  # функция для входа в аккаунт
        passw = ''
        if self.login.text().replace(' ', '') == '' \
                or self.password.text().replace(' ', '') == '':
            if self.login.text().replace(' ', '') == '' \
                    and self.password.text().replace(' ', '') == '':
                self.error_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Введите логин.</h3>')
                self.error_2.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Введите пароль.</h3>')
            elif self.login.text().replace(' ', '') != '' \
                    and self.password.text().replace(' ', '') == '':
                self.error_2.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Введите пароль.</h3>')
                self.error_1.setText('')
            else:
                self.error_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Введите логин.</h3>')
                self.error_2.setText('')
        elif self.login.text().replace(' ', '') != '' \
                and self.password.text().replace(' ', '') != '':
            con = sqlite3.connect('{}'.format(FILE))
            cur = con.cursor()
            rez = cur.execute("""select password from proga
                    where login = '{}'""".format(self.login.text()))
            for i in rez:
                if len(str(*i)) != 0:
                    passw = str(*i)
                else:
                    passw = ''
            con.commit()
            con.close()
            if passw == '':  # проверка на наличие логина путем существования пароля
                self.error_1.setText(
                    '<h3 style="color: rgb(250, 55, 55);">Извините, такого логина</h3>\n'
                    '<h3 style="color: rgb(250, 55, 55);">не существует.</h3>')
                self.error_2.setText('')
            elif passw != '' and self.password.text() != passw:
                self.error_2.setText('<h3 style="color: rgb(250, 55, 55);"'
                                     '>Неверный пароль.</h3>')
                self.error_1.setText('')
            else:
                self.error_1.setText('')
                self.error_2.setText('')
                # открывем следущую форму, передав логин пользователя
                self.second_form = SecondForm(self, self.login.text())
                self.second_form.show()
                self.login.setText('')
                self.password.setText('')

    def registr(self):  # функция регистрации
        self.error_2.setText('')
        self.error_1.setText('')
        self.login.setText('')
        self.password.setText('')
        self.fourth_form = FourthForm(self, self.login.text())  # открывем следущую форму, передав логин пользователя
        self.fourth_form.show()


class SecondForm(QWidget):  # форма для работы с заметками
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.name = args[-1]  # логин
        self.setGeometry(300, 300, 605, 446)
        self.setWindowTitle('ВАШИ ЗАМЕТКИ')
        self.list_of_notes = QListWidget(self)  # здесь будут отображаться заметки
        self.list_of_notes.move(50, 160)
        self.list_of_notes.resize(211, 181)
        font = QtGui.QFont()  # задаем шрифт названиям заметкам
        font.setFamily("Viner Hand ITC")
        self.list_of_notes.setFont(font)
        self.lineEdit = QLineEdit(self)  # имя заметки
        self.lineEdit.move(330, 140)
        self.lineEdit.resize(191, 21)
        self.label_input_name = QLabel(self)  # метка названия заметки
        self.label_input_name.move(340, 100)
        self.label_input_name.resize(171, 21)
        self.create = QPushButton(self)  # кнопка для создания заметки
        self.create.move(330, 180)
        self.create.resize(191, 31)
        self.change = QPushButton(self)  # кнопка для редактирования заметки
        self.change.move(330, 230)
        self.change.resize(191, 31)
        self.delete_ = QPushButton(self)  # кнопка для удаления заметки
        self.delete_.move(330, 290)
        self.delete_.resize(191, 51)
        self.label_names = QLabel(self)  # метка, где отображается имя и фамилия пользователя
        self.label_names.move(10, 90)
        self.label_names.resize(311, 61)
        self.delete_user = QPushButton(self)  # кнопка для удаления пользователя
        self.delete_user.move(20, 370)
        self.delete_user.resize(211, 41)
        self.exit = QPushButton(self)  # кнопка для выхода из аккаунта
        self.exit.move(360, 370)
        self.exit.resize(175, 41)
        self.change_name = QPushButton(self)  # кнопка для выхода из аккаунта
        self.change_name.move(230, 370)
        self.change_name.resize(131, 41)
        self.change_name.setText("ИЗМЕНИТЬ ИМЯ\n""ПОЛЬЗОВАТЕЛЯ")
        self.label_error = QLabel(self)  # метка для появления ошибок, которые допускает пользователь
        self.label_error.move(60, 20)
        self.label_error.resize(530, 61)
        self.label_error.setText("")
        self.label_input_name.setText("Введите имя заметеки")
        self.create.setText("СОЗДАТЬ НОВУЮ ")
        self.change.setText("РЕДАКТИРОВАТЬ")
        self.delete_.setText("УДАЛИТЬ\n""ЗАМЕТКУ")
        self.delete_user.setText("УДАЛИТЬ ПОЛЬЗОВАТЕЛЯ")
        self.exit.setText("ВЫЙТИ ИЗ АККАУНТА")
        self.change.clicked.connect(self.open)
        self.create.clicked.connect(self.new)
        self.exit.clicked.connect(self.exit_from)
        self.delete_.clicked.connect(self.delete)
        self.delete_user.clicked.connect(self.delete_u)
        self.change_name.clicked.connect(self.change_name_user)
        con = sqlite3.connect('{}'.format(FILE))  # заполняем таблицу заметок
        cur = con.cursor()
        rez = cur.execute("""select notes from proga
                        where login = '{}'""".format(self.name))
        for i in rez:
            a = str(*i)
        if a != "None":
            for i in a.split():
                self.list_of_notes.addItem(i)
        con.commit()
        con.close()
        con = sqlite3.connect('{}'.format(FILE))  # вставляем имя пользователя
        cur = con.cursor()
        rez = cur.execute("""select name_surname from proga
                                where login = '{}'""".format(self.name))
        for i in rez:
            a = str(*i)
        if a != 'None':
            self.label_names.setText('ПОЛЬЗОВАТЕЛЬ: {}'.format(a))
        else:
            self.label_names.setText('ПОЛЬЗОВАТЕЛЬ:')
        con.commit()
        con.close()

    def change_name_user(self):
        self.change = ChangeName(self, self.name)  # открывем форму для изменения имени пользователя,
        # передав логин пользователя
        self.change.show()
        self.close()

    def exit_from(self):  # функция для выхода из аккаунта
        valid = QMessageBox.question(
            self, 'ПОДТВЕРЖДЕНИЕ', "Подтвердите выход из аккаунта",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            self.close()

    def delete_u(self):  # функция для удаления аккаунта
        valid = QMessageBox.question(
            self, 'ПРЕДУПРЕЖДЕНИЕ', "ВЫ ТОЧНО ХОТИТЕ УДАЛИТЬ АККАУНТ?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            con = sqlite3.connect('{}'.format(FILE))
            cur = con.cursor()
            rez = cur.execute("""delete from proga
                                where login = '{}'""".format(self.name))
            con.commit()
            con.close()
            self.close()

    def open(self):  # функция для открытия заметки
        self.f = False
        if self.lineEdit.text().replace(' ', '') != '':
            for i in range(self.list_of_notes.count()):
                if self.lineEdit.text() == self.list_of_notes.item(i).text():
                    self.f = True
                    break
            if self.f:
                # передавая в другую форму название заметки, открывается текст заметки
                self.third_form = ThirdForm(self, self.lineEdit.text())
                self.third_form.show()
                self.label_error.setText('')
            else:
                self.label_error.setText('<h4 style="color: rgb(250, 55, 55);"'
                                         '>Извините, у вас нет такой заметки.</h4>')
        else:
            self.label_error.setText('<h4 style="color: rgb(250, 55, 55);"'
                                     '>Извините, вы не можете открыть безымяную заметку.</h4>')

    def new(self):  # функция для создания новой заметки
        x = []  # во время работы функции в этой переменной храним имеющиеся на данный момент заметки
        if self.lineEdit.text() != '':
            if os.path.isfile('{}.txt'.format(self.lineEdit.text())):
                self.label_error.setText(
                    '<h4 style="color: rgb(250, 55, 55);"'
                    '>Извините, данное имя заметки занято в базе.</h4>')
            else:
                f = open('{}.txt'.format(self.lineEdit.text()), mode='w')
                self.list_of_notes.addItem(self.lineEdit.text())
                for i in range(self.list_of_notes.count()):
                    x.append(self.list_of_notes.item(i).text())
                con = sqlite3.connect('{}'.format(FILE))  # обновляем данные заметок
                cur = con.cursor()
                rez = cur.execute("""UPDATE proga
                                         SET notes = '{}'
                                         where login = '{}'""".format(' '.join(x), self.name))
                f.close()
                self.third_form = ThirdForm(self, self.lineEdit.text())  # открытие новой заметки
                self.third_form.show()
                self.label_error.setText('')
                con.commit()
                con.close()
        else:
            self.label_error.setText(
                '<h4 style="color: rgb(250, 55, 55);"'
                '>Извините, вы не можете  создать безымянную заметку.</h4>')

    def delete(self):  # функция для удаления заметки
        self.f = False
        x = []  # во время работы функции в этой переменной храним имеющиеся на данный момент заметки
        for i in range(self.list_of_notes.count()):
            if self.lineEdit.text() == self.list_of_notes.item(i).text():
                self.f = True
                break
        if self.f:  # проверка на существование файла
            os.remove('{}.txt'.format(self.lineEdit.text()))
            for i in range(self.list_of_notes.count()):
                if self.lineEdit.text() != self.list_of_notes.item(i).text():
                    x.append(self.list_of_notes.item(i).text())
            for i in range(self.list_of_notes.count()):
                if self.lineEdit.text() == self.list_of_notes.item(i).text():
                    self.list_of_notes.takeItem(i)
                    break

            con = sqlite3.connect('{}'.format(FILE))  # обновляем данные об заметках
            cur = con.cursor()
            rez = cur.execute("""UPDATE proga
                                     SET notes = '{}'
                                     where login = '{}'""".format(' '.join(x), self.name))
            self.label_error.setText('')
            con.commit()
            con.close()
        else:
            self.label_error.setText('<h4 style="color: rgb(250, 55, 55);"'
                                     '>Извините, вы не можете удалить несуществующую заметку.</h4>')


class ChangeName(QWidget):  # форма для изменения имени
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.name = args[-1]
        self.setGeometry(300, 300, 445, 199)
        self.setWindowTitle('ИЗМЕНЕНИЕ ИМЕНИ')
        self.new_name = QLineEdit(self)  # новое имя
        self.new_name.move(220, 40)
        self.new_name.resize(201, 31)
        self.new_surname = QLineEdit(self)  # новая фамилия
        self.new_surname.move(220, 100)
        self.new_surname.resize(201, 31)
        self.OKEY = QPushButton(self)  # кнопка , которая меняет имя
        self.OKEY.move(110, 150)
        self.OKEY.resize(231, 31)
        self.label_new_n = QLabel(self)  # метка имени
        self.label_new_n.move(20, 30)
        self.label_new_n.resize(171, 51)
        self.label_new_s = QLabel(self)  # метка фамилии
        self.label_new_s.move(24, 89)
        self.label_new_s.resize(191, 51)
        self.OKEY.setText("ПРОДОЛЖИТЬ")
        self.label_new_n.setText(
            "<html><head/><body><p><span style=\" font-size:12pt;\">Новое имя</span></p></body></html>")
        self.label_new_s.setText(
            "<html><head/><body><p><span style=\" font-size:12pt;\">Новая фамилия</span></p></body></html>")
        self.OKEY.clicked.connect(self.ok)

    def ok(self):  # функция для изменения имени пользователя
        valid = QMessageBox.question(
            self, 'ПРЕДУПРЕЖДЕНИЕ', "ВЫ УВЕРЕНЫ?",
            QMessageBox.Yes, QMessageBox.No)
        if valid == QMessageBox.Yes:
            con = sqlite3.connect('{}'.format(FILE))
            cur = con.cursor()
            rez = cur.execute("""UPDATE proga
                                         SET name_surname = '{}'
                                         where login = '{}'""".format(
                self.new_name.text() + ' ' + self.new_surname.text(), self.name))
            con.commit()
            con.close()
        self.secondform = SecondForm(self, self.name)  # обратно открывает нашу форму
        self.secondform.show()
        self.close()


class ThirdForm(QWidget):  # форма для работы с текстом заметки
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 566, 272)
        self.setWindowTitle('ЗАМЕТКА')
        self.save = QPushButton(self)  # кнопка для сохраниения изменения в заметке
        self.save.move(190, 210)
        self.save.resize(171, 51)
        self.text_of_note = QPlainTextEdit(self)  # здесь будет отображаться текст заметки
        self.text_of_note.move(10, 10)
        self.text_of_note.resize(541, 191)
        self.save.setText("СОХРАНИТЬ")
        self.name_file = args[-1]  # имя заметки
        f = open('{}.txt'.format(self.name_file), encoding='utf8')
        data = f.readlines()
        self.text_of_note.setPlainText('\n'.join(data))
        f.close()
        self.save.clicked.connect(self.save_file)

    def save_file(self):  # функция сохраниения изменений
        f = open('{}.txt'.format(self.name_file), mode='w')
        f.write(self.text_of_note.toPlainText())
        f.close()
        self.close()


class FourthForm(QWidget):  # форма регистрации
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 1138, 432)
        self.setWindowTitle('РЕГИСТРАЦИЯ')
        self.new_login = QLineEdit(self)  # новый логин
        self.new_login.move(310, 140)
        self.new_login.resize(251, 41)
        self.new_password_1 = QLineEdit(self)  # новый пароль
        self.new_password_1.move(310, 210)
        self.new_password_1.resize(251, 41)
        self.label_new_login = QLabel(self)  # метка нового логина
        self.label_new_login.move(10, 140)
        self.label_new_login.resize(291, 41)
        self.label_new_password_1 = QLabel(self)  # метка нового пароля
        self.label_new_password_1.move(10, 210)
        self.label_new_password_1.resize(291, 41)
        self.error_login = QLabel(self)  # метка ошибки логина
        self.error_login.move(570, 140)
        self.error_login.resize(301, 41)
        self.error_login.setText("")
        self.error_new_password_1 = QLabel(self)  # метка ошибки нового пароля
        self.error_new_password_1.move(580, 210)
        self.error_new_password_1.resize(531, 41)
        self.error_new_password_1.setText("")
        self.label_new_password_2 = QLabel(self)  # метка ошибки повторного пароля
        self.label_new_password_2.move(10, 280)
        self.label_new_password_2.resize(291, 41)
        self.new_password_2 = QLineEdit(self)  # повторный пароль
        self.new_password_2.move(310, 280)
        self.new_password_2.resize(251, 41)
        self.error_new_password_2 = QLabel(self)  # ошибка повторного пароля
        self.error_new_password_2.move(580, 280)
        self.error_new_password_2.resize(281, 41)
        self.error_new_password_2.setText("")
        self.create_new_login = QPushButton(self)  # кнопка для создания нового пользователя
        self.create_new_login.move(260, 370)
        self.create_new_login.resize(321, 41)
        self.label_surname = QLabel(self)  # метка фамилии
        self.label_surname.move(10, 20)
        self.label_surname.resize(291, 41)
        self.label_name = QLabel(self)  # метка имени
        self.label_name.move(10, 70)
        self.label_name.resize(291, 41)
        self.line_surname = QLineEdit(self)  # фамилия
        self.line_surname.move(310, 20)
        self.line_surname.resize(251, 41)
        self.label_surname.resize(291, 41)
        self.line_name = QLineEdit(self)  # имя
        self.line_name.resize(251, 41)
        self.line_name.move(310, 80)
        self.label_name.resize(291, 41)
        self.error = QLabel(self)  # метка ошибки, звязанной с именем и фамилией пользователя
        self.error.move(584, 49)
        self.error.resize(461, 41)
        self.error.setText("")
        self.label_new_login.setText(
            "<html><head/><body><p><span style=\" font-size:11pt; color:#ffff00;\""
            ">Введите новый логин</span></p></body></html>")
        self.label_new_password_1.setText("<html><head/><body><p><span style=\" font-size:10pt; color:#00ff7f;\""
                                          ">Введите новый пароль</span></p></body></html>")
        self.label_new_password_2.setText("<html><head/><body><p><span style=\""
                                          " font-size:10pt; color:#ff007f;\""
                                          ">Введите повторно новый пароль</span></p></body></html>")
        self.create_new_login.setText("Подтветдить")
        self.label_surname.setText("<html><head/><body><p><span style=\" font-size:12pt; color:#aa55ff;\""
                                   ">Введите вашу фамилию</span></p></body></html>")
        self.label_name.setText(
            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\""
            ">\n""<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
            "p, li { white-space: pre-wrap; }\n"
            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'"
            "; font-size:8pt; font-weight:400; font-style:normal;\">\n"
            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;"
            " -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ffaa00;\""
            ">Введите ваше имя</span></p></body></html>")
        self.create_new_login.clicked.connect(self.create_new)

    def create_new(self):  # функция для создания нового аккаунта
        f1 = False
        f2 = False
        for i in self.new_password_1.text():
            if i in FORBIDDEN_CHARACTERS:
                f1 = True
        for i in self.new_login.text():
            if i in FORBIDDEN_CHARACTERS:
                f2 = True
        try:
            if self.line_name.text().replace(' ', '') == '' \
                    or self.line_surname.text().replace(' ', '') == '':
                self.error.setText('<h3 style="color: rgb(250, 55, 55);"'
                                   '>Введите свои данные.</h3>')
                self.new_login.setText('')
                self.new_password_2.setText('')
                self.new_password_1.setText('')
                self.error_login.setText('')
                self.error_new_password_1.setText('')
                self.error_new_password_2.setText('')
            elif self.new_login.text().replace(' ', '') == '':
                self.error_login.setText('<h3 style="color: rgb(250, 55, 55);"'
                                         '>Введите логин.</h3>')
                self.error.setText('')
                self.error_new_password_1.setText('')
                self.new_password_1.setText('')
                self.new_password_2.setText('')
                self.error_new_password_2.setText('')
            elif f2:  # проверка на недопустимые символы в логине
                self.error.setText('')
                self.error_login.setText('<h3 style="color: rgb(250, 55, 55);"'
                                         '>В логине недопустимые символы.</h3>')
            elif self.new_password_1.text() == '':
                self.error.setText('')
                self.error_login.setText('')
                self.error_new_password_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                                  '>Введите пароль.</h3>')
                self.new_password_2.setText('')
                self.error_login.setText('')
            elif f1:  # проверка на недопустимые символы в пароле
                self.error.setText('')
                self.error_new_password_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                                  '>В пароле присутствуют запрещенные символы.</h3>')
                self.error_login.setText('')
                self.new_password_2.setText('')
                self.error_new_password_2.setText('')
                self.error_login.setText('')
            elif len(self.new_password_1.text()) <= 8:  # проверка длинны пароля
                raise LengthError
            elif self.new_password_1.text().lower() == self.new_password_1.text() \
                    or self.new_password_1.text().upper() == self.new_password_1.text():  # проверка регистра пароля
                raise LetterError
            elif not any([i in self.new_password_1.text() for i in '0123456789']):  # проверка на наличие цифр в пароле
                raise DigitError
            elif any([i in self.new_password_1.text().lower() for i in
                      COMBINATION]):  # проверка наоследовательность, состоящую из близлежащих клавиш
                raise SequenceError
            elif self.new_password_2.text() != self.new_password_1.text():
                if self.new_password_2.text() != '':
                    self.error.setText('')
                    self.error_new_password_2.setText('<h3 style="color: rgb(250, 55, 55);"'
                                                      '>Пароль не совпадает.</h3>')
                    self.error_new_password_1.setText('')
                else:
                    self.error_new_password_2.setText('<h3 style="color: rgb(250, 55, 55);"'
                                                      '>Подтвердите пароль.</h3>')
                    self.error_new_password_1.setText('')
            elif self.new_password_1.text() == self.new_password_2.text():
                x = True
                con = sqlite3.connect('{}'.format(FILE))  # получение значений для дальнейшей проверки
                cur = con.cursor()
                rez = cur.execute("""select * from proga""")
                for i in rez:
                    if self.new_login.text() == i[0]:
                        x = False
                        raise sqlite3.IntegrityError
                con.commit()
                con.close()
                if x:  # проверка на занятость логина
                    valid = QMessageBox.question(
                        self, '', "Создать пользователя?",
                        QMessageBox.Yes, QMessageBox.No)
                    if valid == QMessageBox.Yes:
                        self.names = self.line_name.text() + ' ' + self.line_surname.text()
                        con = sqlite3.connect('{}'.format(FILE))  # заносим пользователя в базу данных
                        cur = con.cursor()
                        rez = cur.execute("""INSERT INTO proga(login, password, name_surname)
                         VALUES('{}', '{}', '{}')
                        """.format(self.new_login.text(), self.new_password_1.text(), self.names))
                        con.commit()
                        con.close()
                        # открываем форму для работы с заметками, передавая новый логн
                        self.second_form = SecondForm(self, self.new_login.text())
                        self.second_form.show()
                        self.close()
                        self.new_password_1.setText('')
                        self.new_password_2.setText('')
                        self.line_surname.setText('')
                        self.line_name.setText('')
                        self.new_login.setText('')
                    self.error_login.setText('')
                    self.error.setText('')
                    self.error_new_password_1.setText('')
                    self.error_new_password_2.setText('')
        except sqlite3.IntegrityError:  # ошибка, возникающая при занятости пароля
            self.error_login.setText('<h2 style="color: rgb(250, 55, 55);"'
                                     '>Извините, логин занят.</h2>')
            self.new_password_1.setText('')
            self.new_password_2.setText('')
            self.error_new_password_1.setText('')
            self.error_new_password_2.setText('')
        except LengthError:  # ошибка, возникающая при коротком пароле
            self.error_new_password_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                              '>Пароль не достаточно длинный.</h3>')
            self.error_login.setText('')
        except LetterError:  # ошибка, возникающая при употреблении одного регистра в праоле
            self.error_new_password_1.setText('<h3 style="color: rgb(250, 55, 55);"''>Пожалуйста, '
                                              'введите пароль , ''состоящий из символов не одного регистра.</h3>')
            self.error_login.setText('')
        except DigitError:  # ошибка , возникающая, когда в пароле нет цифр
            self.error_new_password_1.setText(
                '<h3 style="color: rgb(250, 55, 55);"''>Пожалуйста, добавьте цифру(ы) для надежности.</h3>')
            self.error_login.setText('')
        except SequenceError:  # ошибка , возникающая при нахождении в пароле букв,
            # которые находятся рядом на клавиатуре
            self.error_new_password_1.setText('<h3 style="color: rgb(250, 55, 55);"'
                                              '>Этот пароль легко взломать.</h3>')
            self.error_login.setText('')


if __name__ == "__main__":  # запуск программы
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MyWidget()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
