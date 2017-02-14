#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import string
import sys
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QTextEdit

if getattr(sys, 'frozen', False):
    # frozen
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.executable), "libs")))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.executable), "libs", "python")))
else:
    # unfrozen
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "libs")))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "libs", "python")))

from formlayout import fedit
from FileTreeview import FileTreeview
from NoteFunctions import NoteFunctions
from NoteViewer import NoteViewer

#https://code.google.com/p/wkhtmltopdf/
#http://www.slideshare.net/QT-day/qt-webkit
#http://talk.maemo.org/showthread.php?t=62667

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, functions):

        self.functions = functions

        self.config = self.functions.config
        actions_config = self.functions.load_actions()
        toolbar_config = self.functions.get_toolbar_config()
        sidebuttons_config = self.functions.get_sidebuttons_config()

        self.note_viewer = NoteViewer({'NoteFunctions':self.functions})

        self.functions.session('editor_load_functions', {})
        self.functions.session('editor_load_files_code', {})

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(756, 515)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(self.functions.session('Base path'), 'gui', 'icons', 'note.png')))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        ## LAYOUT
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)

        ## FILE TREE VIEW
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.SideLayout  = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.SideLayout .setContentsMargins(0, 0, 0, 0)
        self.SideLayout .setObjectName("FileTreeLayout")

        #File treeview
        self.note_treeview = FileTreeview(self.verticalLayoutWidget, self.config('Notes path'), self.functions.get_open_extensions())
        self.file_model = self.note_treeview.get_file_model()
        #self.note_treeview.cliked.connect(self.treeview_doubleclick)

        self.SideLayout.addWidget(self.note_treeview)
        self.fileListButtonsLayout = QtWidgets.QHBoxLayout()
        self.fileListButtonsLayout.setObjectName("fileListButtonsLayout")

        self.noteTabLayout = QtWidgets.QTabWidget(self.splitter)

        self.app_data = {
            'note_viewer': self.note_viewer,
            'file_model': self.file_model,
            'note_treeview': self.note_treeview,
            'functions': self.functions
        }

        for sidebuttons_group_name in sorted(sidebuttons_config.keys()):
            for buttonbar_item in sidebuttons_config[sidebuttons_group_name]:
                if isinstance(buttonbar_item, list):

                    first_item = buttonbar_item[0]

                    pushbutton_item = actions_config[first_item]
                    pushbutton_submenu = QtWidgets.QMenu(MainWindow)

                    if buttonbar_item:
                        for item in buttonbar_item:
                            pushbutton_submenu.addAction(self.create_button(actions_config[item], MainWindow, None))

                        pushbutton_item['submenu'] = pushbutton_submenu
                else:
                    pushbutton_item = actions_config[buttonbar_item]

                icon_path = os.path.join(pushbutton_item['path'],pushbutton_item['icon'])
                item = QtWidgets.QPushButton(QtGui.QIcon(QtGui.QPixmap(icon_path)),  None, self.verticalLayoutWidget)

                if pushbutton_item['name']:
                    item.setObjectName(pushbutton_item['name'])

                if pushbutton_item['description']:
                    tooltip_text = pushbutton_item['description']

                    if pushbutton_item['shortcut']:
                        tooltip_text = tooltip_text + " (" + pushbutton_item['shortcut'] + ")"

                if 'submenu' in pushbutton_item:
                    item.setMenu(pushbutton_item['submenu'])

                if pushbutton_item['instance']:
                    if hasattr(pushbutton_item['instance'], 'load_process'):
                        pushbutton_item['instance'].load_process(self.app_data, {})

                    if hasattr(pushbutton_item['instance'], 'process'):
                        item.clicked.connect(partial(pushbutton_item['instance'].process, self.app_data, {}))

                self.fileListButtonsLayout.addWidget(item)

        self.SideLayout.addLayout(self.fileListButtonsLayout)

        self.note_html_content = QTextEdit()
        #self.note_markup_content = QTextEdit()
        font = QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
        #self.note_markup_content.setCurrentFont(font)
        self.note_html_content.setCurrentFont(font)
        #self.note_html_content.setReadOnly(True)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteTabLayout.sizePolicy().hasHeightForWidth())
        self.noteTabLayout.setSizePolicy(sizePolicy)
        self.noteTabLayout.setObjectName("noteTabLayout")

        self.noteTabLayout.addTab(self.note_viewer, "Content")
        #self.noteTabLayout.addTab(self.note_html_content, "Html")

        self.functions.session('current_tabview', 0)
        self.noteTabLayout.currentChanged.connect(self.update_current_tabeditor)

        #Note Contact Size policy
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.note_viewer.sizePolicy().hasHeightForWidth())
        self.note_viewer.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        toolbars_defs = {}

        self.toolbar_buttons = {}

        for toolbar_name in sorted(toolbar_config.keys()):
            toolBar = self.build_toolbar(toolbar_name, toolbar_config, actions_config)
            MainWindow.addToolBarBreak()
            MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, toolBar)

        # required for the note viewer to know which buttons to enable/disable
        # depeding on the opened file
        self.note_viewer.set_toolbar_buttons(self.toolbar_buttons)

        # Set the initial toolbar buttons states
        initial_supported_actions = ['new_note','new_folder','change_notes_path','delete_filefolder','exit_app',
                                     'file_folder_settings','information','new_folder','new_note','open_note',
                                     'rename_filefolder','settings','treeview_options']

        for button_name in self.toolbar_buttons:
            if button_name in initial_supported_actions:
                self.toolbar_buttons[button_name].setEnabled(True)
            else:
                self.toolbar_buttons[button_name].setEnabled(False)

        self.note_treeview.set_double_click_action(actions_config['open_note']['instance'], self.app_data)

        self.apply_settings()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def build_toolbar(self, toolbar_name, toolbar_config, actions_config):
        toolBar = QtWidgets.QToolBar(toolbar_name[4:])

        for toolbar_item in toolbar_config[toolbar_name]:
            if isinstance(toolbar_item, list):
                first_item = toolbar_item[0]
                remaining_items = toolbar_item[1:]

                if first_item == "separator":
                    toolBar.addSeparator()
                else:
                    # First element will the submenu button
                    toolbar_button = self.create_button(actions_config[first_item], MainWindow, None)
                    self.toolbar_buttons[actions_config[first_item]['class_file']] = toolbar_button

                    # Adds submenu
                    popupMenu = QtWidgets.QMenu(MainWindow)
                    toolbar_subbuttons = {}

                    for item in remaining_items:
                        toolbar_subbuttons[item] = self.create_button(actions_config[item], MainWindow, None)
                        popupMenu.addAction(toolbar_subbuttons[item])
                        self.toolbar_buttons[actions_config[item]['class_file']] = toolbar_subbuttons[item]

                    toolbar_button.setMenu(popupMenu)

                    # Adds button and submenu to toolbar
                    toolBar.addAction(toolbar_button)
            else:
                if toolbar_item == "separator":
                    toolBar.addSeparator()
                else:
                    toolbar_button = self.create_button(actions_config[toolbar_item], MainWindow, None)
                    self.toolbar_buttons[actions_config[toolbar_item]['class_file']] = toolbar_button
                    toolBar.addAction(toolbar_button)

        return toolBar

    def update_current_tabeditor(self, idx):
        if idx == 0:
            self.note_viewer.call_function('set_html', self.note_html_content.toPlainText())
        elif idx == 1:
            self.note_html_content.setPlainText(self.note_viewer.get_content())

        #self.note_html_content.setPlainText(self.note_viewer.get_content())

        self.functions.session('current_tabview', idx)

    def apply_settings(self):
        self.note_treeview.setColumnHidden(1, not self.config('Show Filetree Sizes', None, 'view'))
        self.note_treeview.setColumnHidden(2, not self.config('Show Filetree Types', None, 'view'))
        self.note_treeview.setColumnHidden(3, not self.config('Show Filetree Dates', None, 'view'))

        self.note_treeview.setRootIndex(self.file_model.index(self.config('Notes path')))

        #if self.config('Notes path') and self.config('Color Style', None, 'view'):
        #    self.note_viewer.apply_stylefile(os.path.join(self.config('Plugins path'), 'styles', self.config('Color Style', None, 'view')))

        file_name_filters = ["*."+ext for ext in self.config('Show Extensions')]
        file_name_filters.append("*.randomext")
        self.file_model.setNameFilters(file_name_filters)

    def set_status_message(self, message, time=5000):
        if message:
            self.statusbar.showMessage(message, time)

    def set_status_progress(self, message, time=5000):
        if message:
            self.statusbar.show()
            self.statusbar.showMessage(message, time)

    def format_filename(self, s):
        """Take a string and return a valid filename constructed from the string.
            Uses a whitelist approach: any characters not present in valid_chars are
            removed. Also spaces are replaced with underscores.

            Note: this method may produce invalid filenames such as ``, `.` or `..`
            When I use this method I prepend a date string like '2009_01_15_19_46_32_'
            and append a file extension like '.txt', so I avoid the potential of using
            an invalid filename.
        """
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
        return filename

    def create_button(self, button_item, MainWindow, custom_options={}):
        if 'path' in button_item and 'icon' in button_item:
            image_path = os.path.join(button_item['path'], button_item['icon'])
            item = QtWidgets.QAction(QtGui.QIcon(QtGui.QPixmap(image_path)), button_item['name'], MainWindow)
        else:
            item = QtWidgets.QAction(QtGui.QIcon(QtGui.QPixmap("")), button_item['name'], MainWindow)

        if 'description' in button_item and len(button_item['description']) > 0:
            item.setToolTip( button_item['name'] + " (" + button_item['description'] + ")")

        if 'shortcut' in button_item and len(button_item['shortcut']) > 0:
            item.setShortcut(button_item['shortcut'])
            item.setToolTip(button_item['name'] + " (" + button_item['description'] + ")")

        if 'submenu' in button_item:
            submenu = QtWidgets.QMenu(MainWindow)
            button_item['parent_name'] = button_item['name']

            if 'submenu_checked' in button_item and button_item['submenu_checked'] == "True":
                radio_menu = True
                submenu_radio = QtWidgets.QMenu("test", MainWindow)
            else:
                radio_menu = False

            submenu_button_item = {
                'path': button_item['path']
            }

            submenu_item_names = button_item['submenu']
            del(button_item['submenu'])

            for submenu_item_name in submenu_item_names:
                button_item['name'] = submenu_item_name
                submenu_item_icon_path = os.path.join(button_item['path'], self.format_filename(button_item['name']) + ".png")

                if radio_menu:
                    radio_item = self.create_button(button_item, MainWindow, { "submenu_selected_option": submenu_item_name })
                    radio_item.setCheckable(True)
                    radio_item.setChecked(button_item['instance'].get_data(self.app_data, { 'action': 'get_value', 'value_name': submenu_item_name }))
                    radio_item.setIcon(QtGui.QIcon(submenu_item_icon_path))

                    submenu_radio.addAction(radio_item)
                else:
                    submenu_item = self.create_button(button_item, MainWindow, { "submenu_selected_option": submenu_item_name })
                    submenu_item.setIcon(QtGui.QIcon(submenu_item_icon_path))
                    submenu.addAction(submenu_item)

            if radio_menu:
                item.setMenu(submenu_radio)
            else:
                item.setMenu(submenu)
            #item.triggered.connect(lambda: button_item['instance'].process(self.app_data, { "submenu":button_item["submenu"] }))

        if 'instance' in button_item:
            # Function that are to run when a note is opened for preparation of that note

            # LOAD PROCESS FUNCTIONS - usually python code
            if hasattr(button_item['instance'], 'load_process'):
                editor_load_functions = self.functions.session('editor_load_functions')

                if 'parent_name' in button_item.keys():
                    if button_item['parent_name'] not in editor_load_functions:
                        editor_load_functions[button_item['parent_name']] = {
                            'load_process_function':button_item['instance'].load_process,
                            'app_data':self.app_data,
                            'custom_options':custom_options
                        }
                else:
                    if button_item['name'] not in editor_load_functions:
                        editor_load_functions[button_item['name']] = {
                            'load_process_function':button_item['instance'].load_process,
                            'app_data':self.app_data,
                            'custom_options':custom_options
                        }

                self.functions.session('editor_load_functions', editor_load_functions)

            # Function that are to run when a the button is clicked
            if hasattr(button_item['instance'], 'process'):
                item.triggered.connect(lambda: button_item['instance'].process(self.app_data, custom_options))

        return item

    def create_submenu(self,submenu_options, MainWindow):
        popupMenu = QtWidgets.QMenu(MainWindow)
        for array_item in submenu_options:
            popupMenu.addAction(self.create_button(array_item, MainWindow))
        return popupMenu

    def export_note(self, param=None):
        self.save_note('export')

    def rename_filefolder(self, file_folder):
        treeview_selection_index = self.note_treeview.selectedIndexes()
        if treeview_selection_index:
            current_name = self.treeview_getselection(treeview_selection_index[0])
            new_name, ok = QtWidgets.QInputDialog.getText(None, 'New name', 'Enter a new for the file/folder.',
                                                          QLineEdit.Normal, os.path.basename(current_name))
            if ok:
                self.functions.rename_filefolder(current_name, new_name)
        else:
            pass

    def treeview_getselection(self, index=None):
        indexItem = self.file_model.index(index.row(), 0, index.parent())
        filepath = self.file_model.filePath(indexItem)
        return filepath

    #https://wiki.python.org/moin/PythonSpeed/PerformanceTips
    def treeview_show(self, param=None):
        if param and isinstance(param, dict) and  'action' in param:

            if param['action'] in self.functions.get_extensions('native'):
                show_extensions = self.config('Show Extensions')
                if param['action'] in show_extensions:
                    show_extensions.remove(param['action'])
                else:
                    show_extensions.append(param['action'])

                #self.config['view']['Show Extensions'] = show_extensions
                self.config('Show Extensions', show_extensions, 'view')
            else:
                value = not self.config(param['action'], None, 'view')
                self.config(param['action'], value, 'view')

            self.functions.save_configfile()
            self.apply_settings()

    def change_notes_path(self, param=None):
        notes_path = QFileDialog.getExistingDirectory(None, "Select Direcory", self.config('Notes path'))

        if notes_path:
            self.config('Notes path', notes_path)
            self.note_treeview.setRootIndex(self.file_model.index(self.config('Notes path')))

    # def exit_app(self, param=None):
    #     sys.exit(app.exec_())

    def changeMainWindowsTitle(self, MainWindow, title=""):
        MainWindow.setWindowTitle(title)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Yanta"))

notefunctions = NoteFunctions()
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow, notefunctions)
MainWindow.show()
sys.exit(app.exec_())