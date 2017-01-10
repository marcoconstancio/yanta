# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLineEdit

class delete_filefolder:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        current_path = data['note_treeview'].get_selected_path()

        if current_path == data['functions'].session('current_note'):
            data['functions'].session('current_note', None)
            data['functions'].session('current_note_location', None)
            data['note_viewer'].set_content(' ')
            data['note_viewer'].set_readonly()

        data['functions'].delete_filefolder(current_path)


