#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path


from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from libs.python.NoteFunctions import NoteFunctions

class NoteViewer(QWidget):
    def __init__(self, param):
        QWidget.__init__(self)
        # Function for several oprations
        if 'NoteFunctions' in param:
            self.functions = param['NoteFunctions']
        else:
            self.functions = NoteFunctions()

        # Get all viewer, html viewer, text viewer, text
        self.available_note_viewers = {} #= self.functions.available_note_viewers()
        self.available_note_viewers_config = {}
        self.current_note_viewer_name = ""

        # Layout of this widget
        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.get_current_note_viewer())
        self.setLayout(self.layout)
        # Toolbar buttons that are going to be disabled/enabled depeding on the active note viewer

        # Active viewer config
        self.set_current_note_viewer(self.functions.config('Default viewer'))
        #self.current_note_viewer_name = self.functions.config('Default viewer')
        #self.current_note_viewer = self.functions.get_viewer(self.current_note_viewer_name)
        #self.current_note_viewer_config = self.functions.get_viewer_config(self.current_note_viewer_name)

        self.toolbar_buttons = None

    def set_function(self, functions):
        if functions:
            self.functions = functions

    def set_toolbar_buttons(self, toolbar_buttons=None):
        if toolbar_buttons:
            self.toolbar_buttons = toolbar_buttons

    def get_current_note_viewer(self):
        return self.available_note_viewers[self.current_note_viewer_name]

    def get_current_note_viewer_config(self):
        return self.available_note_viewers_config[self.current_note_viewer_name]

    # def current_note_viewer(self):
    #     return self.available_note_viewers[self.current_note_viewer_name]
    #
    # def current_note_viewer_config(self):
    #     return self.available_note_viewers_config[self.current_note_viewer_name]

    def set_current_note_viewer(self, viewer_name=''):
        self.current_note_viewer_name = viewer_name

        if viewer_name not in list(self.available_note_viewers.keys()):
            self.available_note_viewers[self.current_note_viewer_name] = self.functions.get_viewer(viewer_name)
            self.available_note_viewers_config[self.current_note_viewer_name] = self.functions.get_viewer_config(viewer_name)
            self.layout.addWidget(self.available_note_viewers[self.current_note_viewer_name])

        for anv_viewer_name in self.available_note_viewers:
            if anv_viewer_name == viewer_name:
                self.available_note_viewers[anv_viewer_name].show()
            else:
                self.available_note_viewers[anv_viewer_name].set_content(' ')
                self.available_note_viewers[anv_viewer_name].hide()

            #viewer.hide()

        #self.current_note_viewer = self.functions.get_viewer(viewer_name)

    def get_content(self):
        return self.get_current_note_viewer().get_content()

    def set_readonly(self, param=True):
        if param == True:
            self.get_current_note_viewer().set_readonly(True)
        elif param == False:
            self.get_current_note_viewer().set_readonly(False)

    def set_writeable(self):
        self.get_current_note_viewer().set_readonly(False)

    def open_file (self, file_name, viewer_name=None):

        # CHANGE THE VIEWER TYPE IF REQUESTED
        if viewer_name:
            if viewer_name != self.current_note_viewer_name:
                self.set_current_note_viewer(viewer_name)

        # Change toolbar button enable or disable
        viewer_config = self.get_current_note_viewer_config()
        viewer_supported_actions = []

        if 'supported_actions' in viewer_config:
            viewer_supported_actions = viewer_config['supported_actions']

        for button_name in self.toolbar_buttons:
            if button_name in viewer_supported_actions:
                self.toolbar_buttons[button_name].setEnabled(True)
            else:
                self.toolbar_buttons[button_name].setEnabled(False)

        ## APPLY INITIAL SETTINGS
        # Context menu extra options
        if 'context_menu_actions' in viewer_config:
            viewer_context_menu_actions = []

            for button_name in viewer_config['context_menu_actions']:
                viewer_context_menu_actions.append(self.toolbar_buttons[button_name])

            self.call_function('set_context_menu_append_actions', viewer_context_menu_actions)


        if file_name:
            self.get_current_note_viewer().open_file(file_name)



    def set_content(self, content=None, viewer_name=None):
        # CHANGE THE VIEWER TYPE IF REQUESTED
        if viewer_name:
            if viewer_name != self.current_note_viewer_name:
                #self.current_note_viewer_name = viewer_name

                #self.get_current_note_viewer()
                self.set_current_note_viewer(viewer_name)
                # if self.current_note_viewer_name in self.available_note_viewers:
                #     self.available_note_viewers[self.current_note_viewer_name] = self.functions.get_viewer(viewer_name)
                #     self.available_note_viewers_config[self.current_note_viewer_name] = self.functions.functions(viewer_name)

                # http://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
                # for i in reversed(range(self.layout.count())):
                #     widgetToRemove = self.layout.itemAt(i).widget()
                #     # remove it from the layout list
                #     self.layout.removeWidget(widgetToRemove)
                #     # remove it from the gui
                #     widgetToRemove.setParent(None)
                #
                # self.layout.addWidget(self.get_current_note_viewer())

        # Change toolbar button enable or disable
        viewer_config = self.get_current_note_viewer_config()
        viewer_supported_actions = []

        if 'supported_actions' in viewer_config:
            viewer_supported_actions = viewer_config['supported_actions']

        for button_name in self.toolbar_buttons:
            if button_name in viewer_supported_actions:
                self.toolbar_buttons[button_name].setEnabled(True)
            else:
                self.toolbar_buttons[button_name].setEnabled(False)

        ## APPLY INITIAL SETTINGS
        # Context menu extra options
        if 'context_menu_actions' in viewer_config:
            viewer_context_menu_actions = []

            for button_name in viewer_config['context_menu_actions']:
                viewer_context_menu_actions.append(self.toolbar_buttons[button_name])

            self.call_function('set_context_menu_append_actions', viewer_context_menu_actions)

        if content:
            self.get_current_note_viewer().set_content(content)

    def get_config(self):
        return self.get_current_note_viewer().get_config()

    def get_save_extensions(self):
        save_extensions = []
        viewer_config = self.get_current_note_viewer_config()

        if 'save_extensions' in viewer_config:
            save_extensions = viewer_config['save_extensions']

        return save_extensions

    def get_open_extensions(self):
        open_extensions = []
        viewer_config = self.get_current_note_viewer_config()

        if 'open_extensions' in viewer_config:
            open_extensions = viewer_config['open_extensions']

        return open_extensions

    def print_(self):
        if hasattr(self.current_note_viewer, 'print_'):
            return self.get_current_note_viewer().print_

        return None

    def print_(self, param=None):
        return self.get_current_note_viewer().print_(param)


    def call_function(self, function_name=None, *args):
        if function_name:
            if callable(getattr(self.get_current_note_viewer(), function_name, None)):
                return getattr(self.get_current_note_viewer(), function_name)(*args)