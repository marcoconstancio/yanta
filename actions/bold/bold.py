# -*- coding: utf-8 -*-

class bold:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('toggle_bold')