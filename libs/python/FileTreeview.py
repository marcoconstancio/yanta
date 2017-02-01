#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QDir
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView
from PyQt5.QtWidgets import QFileSystemModel

class FileTreeview(QTreeView):
    def __init__(self, parent=None, path=None, extensions=None):
        super(FileTreeview, self).__init__(parent)

        # Create the the file model
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(path)
        self.file_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)
        self.file_model.setNameFilterDisables(0)
        self.file_model.setReadOnly(False)


        file_name_filters = ["*." + ext for ext in extensions]

        # when file_name_filters is empty, filetree shows all files
        # so we include a random extension to prevent that
        file_name_filters.append("*.randomext")

        self.file_model.setNameFilters(file_name_filters)

        self.setParent(parent)
        self.setObjectName("file_treeview")

        self.setAcceptDrops(True)
        self.setDragEnabled(True)

        self.setSortingEnabled(True)
        self.sortByColumn(0, Qt.AscendingOrder)
        self.setAllColumnsShowFocus(True)
        self.setModel(self.file_model)

        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.setRootIndex(self.file_model.index(path))
        self.setColumnWidth(0, 300)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.singleClickAction = None
        self.doubleClickAction = None
        self.app_data = None

    def get_file_model(self):
        return self.file_model



    def get_selected_path(self):
        current_dir = None
        selected_indexes = self.selectedIndexes()

        if selected_indexes:
            first_selected_index = self.file_model.index(selected_indexes[0].row(), 0, selected_indexes[0].parent())
            current_dir = self.file_model.filePath(first_selected_index)

        return current_dir

    def set_selected_file(self, file_name=None):
        if file_name:
            self.setCurrentIndex(self.file_model.index(file_name))


    def set_current_dir(self, dir_index=None):
        if dir_index:
            self.setRootIndex(self.file_model.index(dir_index))

    def set_single_click_action(self, action_instance=None, app_data=None):
        self.singleClickAction = action_instance
        self.app_data = app_data

        if self.singleClickAction:
            self.clicked.connect(self.set_single_click)


    def set_single_click(self, index=None):
        first_selected_index = self.file_model.index(index.row(), 0, index.parent())
        current_file = self.file_model.filePath(first_selected_index)
        self.singleClickAction.process(self.app_data, {'file_name': current_file} )

    def set_double_click_action(self, action_instance=None, app_data=None):
        self.doubleClickAction = action_instance
        self.app_data = app_data

        if self.doubleClickAction:
            self.doubleClicked.connect(self.set_double_click)

    def set_double_click(self, index=None):
        first_selected_index = self.file_model.index(index.row(), 0, index.parent())
        current_file = self.file_model.filePath(first_selected_index)

        self.doubleClickAction.process(self.app_data, { 'file_name':current_file } )
