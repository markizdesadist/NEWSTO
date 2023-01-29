from loguru import logger
from PyQt5.QtWidgets import QMessageBox, QLabel, QApplication
import os
import sys

арр_message = QApplication(sys.argv)


info_path = os.path.abspath(os.path.join('..', 'logs', 'log_{time:DD_MM_YY}.log'))
warning_path = os.path.abspath(os.path.join('..', 'logs', 'warning', 'logs', 'log_{time:DD_MM_YY}.log'))
sys.path.append(info_path)
user = os.getlogin()


def wrapper_except(func):
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)
        except Exception as err:
            message_error("Database Error: {}".format(err))


    return wrapper


def message_error(text):
    err_text = text.split(":")
    QMessageBox.critical(
        None,
        "{} - Error!".format(err_text[0]),
        err_text[1]
    )
    sys.exit(1)

    # Create the application's dialog window
    win = QLabel("Connection Successfully Opened!")
    win.setWindowTitle("message_error")
    win.resize(200, 100)
    win.show()
    sys.exit(арр_message.exec_())

def message_done(text):
    QMessageBox.information(
        None,
        "Операция прошла успешно!",
        text
    )
    sys.exit(1)

    # Create the application's dialog window
    # win = QLabel("Connection Successfully Opened!")
    win.setWindowTitle("message_done")
    win.resize(200, 100)
    win.show()
    sys.exit(арр_message.exec_())

logger.add(
    info_path,
    level='INFO',
    format='[{time:DD-MM-YY HH:mm}] | {level}\t| {name}:<{module}>: (line: {line}) |-> : ' + user + ' : {message}',
    rotation='17:00',
    retention='7 days',
    compression='zip',
    enqueue=True,
    encoding='utf-8'
)
logger.add(
    warning_path,
    level='WARNING',
    format='[{time:DD-MM-YY HH:mm}] | {level}\t| {name}:<{module}>: (line: {line}) |-> : ' + user + ' : {message}',
    rotation='17:00',
    retention='20 days',
    compression='zip',
    enqueue=True,
    encoding='utf-8'
)
if __name__ == '__main__':
    pass
