# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrinterInfo, QPrintPreviewDialog
from PyQt5.QtWidgets import QFileDialog

class printer:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        printer = QPrinter(QPrinterInfo.defaultPrinter())
        printer.setOutputFormat(QPrinter.NativeFormat)

        if 'printer' in data['functions'].config():
            printer.setPaperSize(int(data['functions'].config('Paper Size', None, 'printer')))
            printer.setOrientation(int(data['functions'].config('Orientation', None, 'printer')))
            printer.setResolution(int(data['functions'].config('Dots Per Inch', None, 'printer')))
            printer.setColorMode(int(data['functions'].config('Color Mode', None, 'printer')))

            paper_margins = data['functions'].config('Paper Margins', None, 'printer')
            margins = [x.strip() for x in paper_margins.split(',')]
            if len(margins) == 4:
                printer.setPageMargins(float(margins[0]), float(margins[1]),
                                       float(margins[2]), float(margins[3]),
                                       int(data['functions'].config('Paper Unit', None, 'printer')))

            dialog = QPrintPreviewDialog(printer)
            #dialog.setWindowState(Qt.WindowMaximized)
            dialog.paintRequested.connect(data['note_viewer'].print_)
            dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint | Qt.WindowContextHelpButtonHint)
            dialog.exec()