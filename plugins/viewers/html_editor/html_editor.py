#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import string
import webbrowser
import shutil
import json
import base64

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QFile
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWidgets import QInputDialog, QFileDialog
from PyQt5.QtWebKitWidgets import QWebView, QWebPage

# from bs4 import BeautifulSoup
from libs.python.pyquery import PyQuery as pq
from lxml import etree
import urllib
import time
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtWidgets import QApplication

#from PIL import Image
import requests
from io import BytesIO

class html_editor(QWebView):
    def __init__(self, parent=None, html=None, css_file=None):

    #def __init__(self, html=None, style_filename=None):
        super(html_editor, self).__init__(parent)

        # http://stackoverflow.com/questions/21357157/is-there-any-solution-for-the-qtwebkit-memory-leak
        # https://github.com/lycying/seeking

        #self.page().setContentEditable(True)
        #self.execute_js('document.designMode = "on"')
        self.file_dialog_dir = '.'
        # TO CHECK

        # http://nullege.com/codes/show/src%40c%40a%40calibre-HEAD%40src%40calibre%40gui2%40viewer%40documentview.py/89/PyQt4.QtWebKit.QWebPage.setLinkDelegationPolicy/python
        settings = self.settings()
    
        # settings.setMaximumPagesInCache(0)
        # settings.setObjectCacheCapacities(0, 0, 0)
        # settings.setOfflineStorageDefaultQuota(0)
        # settings.setOfflineWebApplicationCacheQuota(0)

        # Security
        settings.setAttribute(QWebSettings.JavaEnabled, False)
        #settings.setAttribute(QWebSettings.PluginsEnabled, False)
        #settings.setAttribute(QWebSettings.JavascriptCanOpenWindows, False)
        #settings.setAttribute(QWebSettings.JavascriptCanAccessClipboard, False)

        # Miscellaneous
        settings.setAttribute(QWebSettings.LinksIncludedInFocusChain, True)
        settings.setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        # settings.setAttribute(QWebSettings.AutoLoadImages, False)

        # Disable Hyperlinks following, open url on system browser
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.page().linkClicked.connect(lambda url: webbrowser.open(str(url.toString())))

        if html:
            self.setHtml(html)
        else:
            self.set_readonly(True)

        # config
        config_file_path = os.path.join(os.path.dirname(__file__), 'config.json')
        self.config = None
        if os.path.isfile(config_file_path):
            with open(config_file_path) as outfile:
                self.config = json.load(outfile)
                outfile.close()

        self.context_menu_actions = []

        # TO CHECK
        # https://github.com/gen2brain/pyhtmleditor/blob/master/src/pyhtmleditor/htmleditor.py
        # https://github.com/kovidgoyal/calibre/blob/master/src/calibre/gui2/comments_editor.py

    #if css_file:
        #    self.apply_stylefile(css_file)

        ############# TO IMPLEMENT ##########
        #self.note_editor.execute_js(self.functions.get_javascript_plugins())

        #self.load_functions = []
        #self.settings().setAttribute(QWebSettings.AutoLoadImages, False)

        #QWebSettings.globalSettings()->setAttribute(QWebSettings::DeveloperExtrasEnabled, true);
        #QWebSettings.globalSettings().setAttribute(QWebSettings.OfflineWebApplicationCacheEnabled, True)


    def get_config(self):
        return self.config

    def set_context_menu_append_actions(self, context_menu_actions):
        self.context_menu_actions = context_menu_actions

    def contextMenuEvent(self, event):
        menu = self.page().createStandardContextMenu()

        if 'default_context_menu_replace' in self.config:
            if self.config['default_context_menu_replace'] == 'True':
                menu = QtWidgets.QMenu(self)

        if 'context_menu_actions' in self.config:
            for action in self.context_menu_actions:
                menu.addAction(action)

        menu.exec_(QtGui.QCursor.pos())

    def set_readonly(self, param=True):
        if param == True:
            self.execute_js('document.body.contentEditable = "false"')
        elif param == False:
            self.execute_js('document.body.contentEditable = "true"')

    def set_writeable(self):
        self.set_readonly(False)

    def set_html(self, html=None):
        if html:
            self.setHtml(html)


    def get_html(self,relative_path=None):
        html = self.page().mainFrame().toHtml()

        pd_content = pq(html)

        if pd_content('img').length > 0:
            num_img = 0
            max_num_img = 0

            # Dertemines the number of image to download and process
            for img in pd_content('img'):
                if "base64" not in img.attrib['src']:
                    max_num_img += 1

            # There are image to download and process
            if max_num_img > 0:
                progress_dialog = QProgressDialog(self)
                progress_dialog.setWindowTitle('Please Wait')
                progress_dialog.setLabelText('Downloading and processing images. Please wait.')
                progress_dialog.setRange(num_img, max_num_img)
                progress_dialog.setValue(num_img)
                progress_dialog.setCancelButton(None)
                progress_dialog.show()
                QApplication.processEvents()

                for img in pd_content('img'):
                    if "base64" not in img.attrib['src']:
                        if 'http' in img.attrib['src'].lower() or 'ftp' in img.attrib['src'].lower():
                            # Downloads images
                            response = requests.get(img.attrib['src'])

                            # Generates base64 of the image
                            base64_img = base64.b64encode(response.content).decode('ascii')
                            # Build uri
                            uri = "data:" + response.headers['Content-Type'] + ";" + "base64," + base64_img
                            # Reasings src attrbiute with the uri data
                            img.attrib['src'] = uri

                        # Updates progress bar
                        num_img = num_img + 1
                        progress_dialog.setValue(num_img)
                        QApplication.processEvents()

                html = pd_content.html()

        return html

    def get_content(self):
        return self.get_html()

    def set_content(self, content):
        if content:
            self.set_html(content)

    def open_file(self, file_path):
        with open(file_path, encoding='UTF-8', errors="ignore") as fd:
            base_url = QUrl.fromLocalFile(os.path.join(os.path.dirname(file_path), ''))
            self.setHtml(fd.read(), base_url)
            fd.close()

        # Generates uft8 bugs
        # fd = QFile(file_path)
        # if fd.open(QFile.ReadOnly):
        #     # Required for webkit to access local images
        #     base_url = QUrl.fromLocalFile(os.path.join(os.path.dirname(file_path),''))
        #     self.setContent(fd.readAll(), "text/html", base_url)
        #     fd.close()

    def toggle_bold(self, parm=None):
        self.page().triggerAction(QWebPage.ToggleBold)

    def toggle_italic(self, parm=None):
        self.page().triggerAction(QWebPage.ToggleItalic)

    def heading(self, param=None):
        if param and param in ['heading_1', 'heading_2', 'heading_3', 'heading_4', 'heading_5', 'heading_6']:
            cmd_str = str("document.execCommand('formatblock', false, '%s');" % str('h'+param[8]))
            self.execute_js(cmd_str)

    def orderedlist(self, param=None):
        self.page().triggerAction(QWebPage.InsertOrderedList)

    def unorderedlist(self, param=None):
        self.page().triggerAction(QWebPage.InsertUnorderedList)

    def insert_horizontal_rule(self, param=None):
        self.execute_js("document.execCommand('inserthorizontalrule', false, false);")

    def block_quote(self, param=None):
        self.execute_js("document.execCommand('formatblock', false, 'blockquote');")

    def insert_html(self, param=None):
        if param:
            cmd_str = 'var range = document.getSelection().getRangeAt(0); \
                       document.execCommand("inserthtml",false,"' + param + '");'
            self.execute_js(cmd_str)

    def preformated_text(self, param=None):
        self.execute_js("document.execCommand('formatblock', false, 'pre');")
        # if self.page().hasSelection():
        #     #pass
        #
        #     cmd_str = 'var range = document.getSelection().getRangeAt(0); \
        #                document.execCommand("inserthtml",false,"<pre><code>" + range + "</code></pre>");'
        #     self.execute_js(cmd_str)

    def block_code(self, param=None):
        if self.page().hasSelection():
            cmd_str = 'var range = document.getSelection().getRangeAt(0); \
                       document.execCommand("inserthtml",false,"<code>" + range + "</code>");'
            self.execute_js(cmd_str)

    def insert_checkbox(self, param=None):
        if self.page().hasSelection():
            cmd_str = 'var range = document.getSelection().getRangeAt(0); \
                       document.execCommand("inserthtml",false,"<input type=\'checkbox\' name=\'test\' checked>" + selObj.toString() + range);'
            self.execute_js(cmd_str)

    def indent(self, param=None):
        self.execute_js("document.execCommand('indent', false, true);")

    def outdent(self, param=None):
        self.execute_js("document.execCommand('outdent', false, true);")

    def undo(self, param=None):
        self.page().triggerAction(QWebPage.Undo)

    def redo(self, param=None):
        self.page().triggerAction(QWebPage.Redo)

    def cut(self, param=None):
        self.page().triggerAction(QWebPage.Cut)

    def copy(self, param=None):
        self.page().triggerAction(QWebPage.Copy)

    def paste(self, param=None):
        self.page().triggerAction(QWebPage.Paste)

    def remove_format(self, param=None):
        self.page().triggerAction(QWebPage.RemoveFormat)

    def insert_link(self, param=None):
        link, ok = QInputDialog.getText(None, 'Insert Link','Enter a url for the link (ex: http://www.google.com).') #QLineEdit.Normal
        if ok:
            self.execute_js("document.execCommand('createLink', false, '%s');" % link)

    def insert_embedded_image(self, param=None):
        if param:
            filename, fileextension = os.path.splitext(param)
            fileextension = fileextension[1:]
            image_encoded_data = base64.b64encode(open(param, "rb").read())
            self.insert_html("<img src='data:image/" + fileextension + ";base64," + image_encoded_data.decode('ascii') + "' />")

    def insert_image(self, image_path=None, new_image_path=None):
        #image_path, extra = QFileDialog.getOpenFileName(None, 'Select Image', self.file_dialog_dir, "All files (*.*);;JPEG (*.jpg *.jpeg);;TIFF (*.tif)")

        image_path_base, file_extension = os.path.splitext(image_path)
        file_name = os.path.basename(image_path)
        copied = False

        if image_path and new_image_path:
            if not os.path.isfile(os.path.join(new_image_path, file_name)):
                try:
                    shutil.copy2(image_path, new_image_path)
                    copied = True
                except (OSError, IOError):
                    print("Unable to copy the file to :" + str(new_image_path))
            else:
                try:
                    new_location = image_path_base + '_' + time.strftime("%Y%m%d") + "_" + time.strftime("%H%M%S") + file_extension
                    shutil.copy2(image_path, new_location)
                    copied = True
                except (OSError, IOError):
                    print("Unable to copy the file to :" + str(new_location))

            if copied:
                # file_path = QUrl.fromLocalFile(new_location).toString()
                # self.execute_js("document.execCommand('insertImage', false, '%s');" % file_path)
                self.insert_html("<img src ='" + file_name + "' />")

    def execute_js(self, param=None):
        if param:
            #print ("**************************************************")
            #print (param)
            self.page().mainFrame().evaluateJavaScript(param)

    def execute_jsfile(self, param=None):
        if param:
            js_content = None
            file_path = os.path.join(os.path.dirname(__file__), param)

            if os.path.isfile(file_path):
                with open(file_path, encoding='UTF-8') as fd:
                    js_content = fd.read()
                    fd.close()

            if js_content:
                self.execute_js(js_content)


    def apply_style(self, style=None, class_name=None):
        if style:
            style = style.replace("\"", "'").replace("\n", " ")

            js_code = ""

            if class_name:
                js_code += "var elements = document.getElementsByClassName('" + class_name + "'); "
                js_code += "while (elements.length > 0){ elements[0].parentNode.removeChild(elements[0]); } "

            js_code += "var css = document.createElement('style'); "
            js_code += "css.type = 'text/css'; "

            if class_name:
                js_code += "css.className = '" + class_name + "'; "



            js_code += "var styles = '" + style + "'; "
            js_code += "if(css.styleSheet){ css.styleSheet.cssText = styles; }else{ css.appendChild(document.createTextNode(styles)); } "
            js_code += "document.getElementsByTagName('head')[0].appendChild(css); \n"

            self.execute_js(js_code)


            # ORIGINAL CODE
            # original_html = self.page().mainFrame().toHtml()
            #
            # try:
            #     soup = BeautifulSoup(original_html, "lxml")# "html.parser")
            #     head = soup.head
            #
            #     if class_name:
            #         note_styles = soup.find_all("style", {'class': class_name})
            #         if note_styles:
            #             for note_style in note_styles:
            #                 note_style.decompose()
            #
            #     if style:
            #         new_style = soup.new_tag('style')
            #         new_style['type'] = 'text/css'
            #
            #         if class_name:
            #             new_style['class'] = class_name
            #
            #         new_style.append(style)
            #         head.append(new_style)
            #
            #     #new_html = soup.prettify()#()(formatter="minimal")
            #     new_html=str(soup)
            #     self.set_content(new_html)
            # except Exception as e:
            #     self.set_content(original_html)


    def apply_stylefile(self, file_path=None, class_name=None):
        if file_path and os.path.isfile(file_path):
            css_file_content_content = ""

            with open(file_path, encoding='UTF-8', errors="ignore") as fd:
                file_content = fd.read()  # self.convert_markup(fd.read(), file_name, 'import', 'open')
                if file_content is not None:
                    css_file_content_content = file_content
                fd.close()

            self.apply_style(css_file_content_content, class_name)