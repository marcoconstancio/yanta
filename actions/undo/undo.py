# -*- coding: utf-8 -*-

class undo:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('undo')