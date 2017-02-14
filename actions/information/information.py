# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox


class information:
    def __init__(self):
        self.this = self
        pass

    @staticmethod
    def process(data, args):

        text = "YANTA\n"
        text += "Yet Another Note Taking Application\n\n"

        text += "Libs Used: Pyqt5, Pyquery, formlayout, jQuery\n"
        text += "Icons by: FatCow hosting - www.fatcow.com/free-icons\n"

        reply = QMessageBox.question(None, 'Information',
                                           text,  QMessageBox.Ok)