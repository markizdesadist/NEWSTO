# from winstart.winstarter import MainWindow
from setting import logger


class Command:
    def __init__(self):
        pass

    @logger.logger.catch
    def on_clicked(self):
        super().setText('$)')
