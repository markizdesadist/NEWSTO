from PyQt5 import QtCore

class Retranslater:
    def retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        # self.setWindowTitle(_translate("MainWindow", "BaseSTO"))
        #
        # self.setWindowTitle(_translate("Dialog", "Dialog"))

        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_order),
            _translate("MainWindow", "Новый Акт")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_order),
            _translate("MainWindow", "Создание нового акта, печать Заказ-нарядов и Внутренних накладных")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_client),
            _translate("MainWindow", "Новый клиент")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_client),
            _translate("MainWindow", "Внесение данных о новом клиенте")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_new_car),
            _translate("MainWindow", "Новая машина")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_new_car),
            _translate("MainWindow", "Внесение данных о новой машине клиента")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_old_order),
            _translate("MainWindow", "Закрытые заказ-наряды")
        )
        self.tabWidget.setTabToolTip(
            self.tabWidget.indexOf(self.tab_old_order),
            _translate("MainWindow", "Выписка по закрытым Заказ-нарядам")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_help),
            _translate("MainWindow", "Help")
        )