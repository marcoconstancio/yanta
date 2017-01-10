# -*- coding: utf-8 -*-
import os


class hyperlink:
    def __init__(self):
        pass

    @staticmethod
    def process(data, args):
        data['note_viewer'].call_function('insert_link')