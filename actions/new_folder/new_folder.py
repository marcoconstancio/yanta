# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

class new_folder:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        foldername, ok = QtWidgets.QInputDialog.getText(None, 'New Folder', 'Enter a name for the new folder.',
                                                        QLineEdit.Normal, "New Folder")

        if ok:
            current_path = data['note_treeview'].get_selected_path()

            if current_path is None:
                current_path = data['functions'].config('Notes path')

            data['functions'].new_folder(current_path, foldername)
