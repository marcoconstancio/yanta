# -*- coding: utf-8 -*-
import sys


class exit_app:
    def __init__(self):
        self.this = self
        pass

    @staticmethod
    def process(data, args):
        sys.exit()
        #sys.exit(app.exec_())