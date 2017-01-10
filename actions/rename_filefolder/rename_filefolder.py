# -*- coding: utf-8 -*-
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

class rename_filefolder:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        current_path = data['note_treeview'].get_selected_path()

        if current_path:
            new_name, ok = QtWidgets.QInputDialog.getText(None, 'New name', 'Enter a new for the file/folder.',
                                                          QLineEdit.Normal, os.path.basename(current_path))
            if ok:
                data['functions'].rename_filefolder(current_path, new_name)
