# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


class save_note:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):

        filename = data['functions'].session('current_note')
        if filename:
            data['functions'].save_file(filename, data['note_viewer'].get_content())
