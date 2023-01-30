from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QWidget
from winstart.wincammands import Command
# from winstart.texttranslate import Retranslater
from setting import logger
from datetime import datetime
import winstart.order_frame

comm_dict = {
    'set logo name': Command().on_clicked
}


class Translate:
    def __init__(self):
        self._translate = QtCore.QCoreApplication.translate

    def retranslate(self):
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_order),
            self._translate("MainWindow", "Новый Акт")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_order),
            self._translate("MainWindow", "Создание нового акта, печать Заказ-нарядов и Внутренних накладных")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_client),
            self._translate("MainWindow", "Новый клиент")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_client),
            self._translate("MainWindow", "Внесение данных о новом клиенте")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_new_car),
            self._translate("MainWindow", "Новая машина")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_new_car),
            self._translate("MainWindow", "Внесение данных о новой машине клиента")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_old_order),
            self._translate("MainWindow", "Закрытые заказ-наряды")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_old_order),
            self._translate("MainWindow", "Выписка по закрытым Заказ-нарядам")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_help),
            self._translate("MainWindow", "Help")
        )


class Frame:
    def __init__(self):
        super().__init__()
        self.frame = QtWidgets.QFrame()
        self.frame.resize(300, 300)
        self.hbox = QtWidgets.QHBoxLayout()
        self.lbl_logo = Label().set_label('LOGO')
        self.timer = Timer().set_timer()

        self.btn_save = Button().btn_test('qweqweqwe')

    @logger.logger.catch
    def frame_logo(self):
        self.frame = QtWidgets.QFrame()
        self.frame.setMaximumHeight(50)
        self.frame.setStyleSheet("QFrame {background-color: green}")
        self.hbox.addWidget(self.timer, alignment=QtCore.Qt.Alignment())
        self.hbox.addWidget(self.lbl_logo, alignment=QtCore.Qt.Alignment())
        self.frame.setLayout(self.hbox)

        return self.frame

    @logger.logger.catch
    def frame_btn(self):

        self.frame = QtWidgets.QFrame()
        self.frame.setMaximumHeight(50)
        self.frame.setStyleSheet("background-color: red")

        self.hbox.addWidget(self.btn_save)

        return self.frame

    # @logger.logger.catch
    # def frame_menu(self):
    #     self.frame.setStyleSheet("background-color: yellow")
    #     return self.frame
    #
    @logger.logger.catch
    def frame_left(self):
        pass

    @logger.logger.catch
    def frame_right(self):
        self.frame = QtWidgets.QFrame()
        self.frame.resize(300, 300)
        self.frame.setStyleSheet("background-color: yellow")
        return self.frame


class TabWidget(Translate):

    def __init__(self):
        super(TabWidget, self).__init__()
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setMaximumWidth(600)
        self.tabWidget.setMaximumSize(600, 700)
        self.tab_order = QtWidgets.QWidget()
        self.tab_client = QtWidgets.QWidget()
        self.tab_new_car = QtWidgets.QWidget()
        self.tab_old_order = QtWidgets.QWidget()
        self.tab_help = QtWidgets.QWidget()

    def frame_left(self):
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet("background-color: rgb(185, 185, 185);")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_order = QtWidgets.QWidget()
        self.tab_order.setObjectName('tab_order')
        self.tabWidget.addTab(self.tab_order, '')

        self.tab_client = QtWidgets.QWidget()
        self.tab_client.setObjectName('tab_client')
        self.tabWidget.addTab(self.tab_client, '')

        self.tab_new_car = QtWidgets.QWidget()
        self.tab_new_car.setObjectName('tab_new_car')
        self.tabWidget.addTab(self.tab_new_car, '')

        self.tab_old_order = QtWidgets.QWidget()
        self.tab_old_order.setObjectName('tab_old_order')
        self.tabWidget.addTab(self.tab_old_order, '')

        self.tab_help = QtWidgets.QWidget()
        self.tab_help.setObjectName('tab_help')
        self.tabWidget.addTab(self.tab_help, '')

        self.tabWidget.setCurrentIndex(0)


        super().retranslate()

        return self.tabWidget


class Button:
    def __init__(self):
        self.button = QtWidgets.QPushButton()
        self.command = Command()

    def btn_test(self, elem):
        self.button.setText("Запустить процесс")

        self.button.clicked.connect(lambda: comm_dict['set logo name'](elem))
        return self.button


class Label:
    def __init__(self):
        self.label = QtWidgets.QLabel()

    def set_label(self, text):
        self.label.setText(text)
        self.label.setIndent(10)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setStyleSheet("QLabel {background-color: red;}")
        return self.label


class Timer:
    def __init__(self):
        self.timeEdit = QtWidgets.QTimeEdit()
        self.current_time = QtCore.QTime.currentTime()
        self.timer = QtCore.QTimer()

    def set_timer(self):
        self.timeEdit.setGeometry(QtCore.QRect(50, 0, 118, 37))
        self.timeEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.timeEdit.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.timeEdit.setWrapping(False)
        self.timeEdit.setFrame(True)
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setReadOnly(True)
        self.timeEdit.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.timeEdit.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.timeEdit.setKeyboardTracking(False)
        self.timeEdit.setObjectName("timeEdit")
        self.timeEdit.setTime(datetime.now().time())

        self.timer.timeout.connect(self.time_edit_update)
        self.timer.start(1000)

        return self.timeEdit

    def time_edit_update(self):
        self.timeEdit.setTime(self.current_time)


if __name__ == '__main__':
    pass