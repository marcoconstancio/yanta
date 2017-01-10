# -*- coding: utf-8 -*-
import base64
import os

from PyQt5.QtWidgets import QFileDialog


class insert_image:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):

        image_path, extra = QFileDialog.getOpenFileName(None,
                                                        'Select Image',
                                                        data['functions'].session('current_note_location'),
                                                         "All Images (*.jpg *.jpeg *.png *.gif *.bmp)")

        if image_path:
            data['note_viewer'].call_function('insert_embedded_image',image_path)
