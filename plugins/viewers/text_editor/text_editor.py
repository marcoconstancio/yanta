#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QTextEdit, QFileDialog, QLineEdit)
from PyQt5.QtGui import QFont

import os.path
import shutil
import json
from PyQt5.QtCore import QFile
class text_editor(QTextEdit):
    def __init__(self, text=None):
        super(text_editor, self).__init__()

        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)

        self.setCurrentFont(font)

        if text:
            self.setPlainText(text)
        else:
            self.setReadOnly(True)

        # config
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.config = None
        if os.path.isfile(config_file_path):
            with open(config_file_path) as outfile:
                self.config = json.load(outfile)
                outfile.close()


    def get_config(self):
        return self.config

    # def contextMenuEvent(self, event):
    #
    #     menu = self.page().createStandardContextMenu()
    #
    #     if 'default_context_menu_replace' in self.config:
    #         if self.config['default_context_menu_replace'] == 'True':
    #             menu = QtWidgets.QMenu(self)
    #
    #     if 'context_menu_actions' in self.config:
    #         for action in self.context_menu_actions:
    #             menu.addAction(action)
    #
    #     menu.exec_(QtGui.QCursor.pos())
    def set_readonly(self, param=True):
        if param == True:
            self.setReadOnly(True)
        elif param == False:
            self.setReadOnly(False)

    def set_writeable(self):
        self.set_readonly(False)

    def set_text(self, text=None):
        if text:
            self.setPlainText(text)

    def get_text(self,relative_path=None):
        return self.toPlainText()

    def get_content(self):
        return self.get_text()

    def set_content(self, content):
        if content:
            self.set_text(content)

    def open_file(self, file_path):
        with open(file_path, encoding='UTF-8', errors="ignore") as fd:
            self.set_text(fd.read())
            fd.close()

    # def open_file(self, file_name):
    #     file_content = ""
    #
    #     if file_name is not None and os.path.isfile(file_name):
    #         with open(file_name, encoding='UTF-8', errors="ignore") as fd:
    #             file_content = fd.read() #self.convert_markup(fd.read(), file_name, 'import', 'open')
    #             if file_content is not None:
    #                 file_content = file_content
    #             fd.close()
    #
    #     return file_content.strip()
    # def note_undo(self, param=None):
    #     self.undo()

    # def note_redo(self, param=None):
    #     self.redo()


    def set_context_menu_append_actions(self, context_menu_actions=None):
        pass

    def text_ident(self, param=None):
        pass

    def text_ident_remove(self, param=None):
        pass



    def page_action_cut(self, param=None):
        pass

    def page_action_copy(self, param=None):
        pass

    def page_action_paste(self, param=None):
        pass

    def apply_style(self, style=None, class_name=None):
        pass

    def apply_stylefile(self, file_path=None, class_name=None):
        pass