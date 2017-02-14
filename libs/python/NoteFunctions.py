# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import platform
import sys
import shutil
import json

class NoteFunctions():
    def __init__(self,config_file=None):
        if config_file is None:
            config_file = 'config.json'

        self.yanta_data = {}
        if getattr(sys, 'frozen', False):
            # The application is frozen
            main_dir = os.path.dirname(sys.executable)
            #full_real_path = os.path.realpath(sys.executable)

            self.yanta_data['base_dir'] = main_dir #os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
        else:
            # The application is not frozen
            # Change this bit to match where you store your data files:
            self.yanta_data['base_dir'] = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

            # script_dir = os.path.dirname(__file__)
            # main_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            # full_real_path = os.path.realpath(sys.argv[0])


        self.yanta_data['config_file'] = os.path.join(self.yanta_data['base_dir'], config_file)

        self.yanta_data['config'] = self.load_configfile()
        self.yanta_data['action'] = self.load_actions()
        self.yanta_data['styles'] = self.load_styles()
        self.yanta_data['viewers'] = self.load_viewers()

        self.session('Base path', self.yanta_data['base_dir'])


    def settings(self,param_name=None, param_value=None, section=None):
        return self.config(param_name, param_value, section, 'settings')

    def session(self,param_name=None, param_value=None, section=None):
        return self.config(param_name, param_value, section, 'session')

    def config(self, param_name=None, param_value=None, section=None, category='config'):
        if param_name:
            #print("1 "+str(category)+" - "+str(section)+" - "+str(param_name)+": " +str(param_value))
            if param_value is not None: # WRITE VALUE ON CONFIG
                # print("2 "+str(category)+" - "+str(section)+" - "+str(param_name)+": " +str(param_value))
                if section:
                    if category not in self.yanta_data:
                        self.yanta_data[category] = { 'general':{} }

                    if section not in self.yanta_data[category]:
                        self.yanta_data[category][section] = {}

                    # print("3 "+str(category)+" - "+str(section)+" - "+str(param_name)+": " +str(param_value))
                    self.yanta_data[category][section][param_name] = param_value
                else:
                    # print("4 "+str(category)+" - "+str(section)+" - "+str(param_name)+": " +str(param_value))
                    self.config(param_name, param_value, 'general', category)
            else:
                # READS VALUES FROM CONFIG
                if section:
                    # THE SECTION IS KNOWN
                    # print("SECTION "+param_name+" "+section)
                    if section in self.yanta_data[category] and param_name in self.yanta_data[category][section]:
                        # if(isinstance(self.yanta_data[category][section], list)):
                        #     return True
                        # else:
                        # print("SECTION "+section+" "+param_name+" PASSED")
                        return self.yanta_data[category][section][param_name]
                else:
                    # THE SECTION IS NOT KNOWN, WILL TRY TO FIND IT
                    if category in self.yanta_data:
                        # print("CATEGORY "+category +" "+param_name)
                        # SEARCH FIRST THE GENERAL SECTION, THE MOST COMMON ONE
                        if 'general' in self.yanta_data[category] and param_name in self.yanta_data[category]['general']:
                            # print("CATEGORY "+category+" "+param_name+" GENERAL PASSED")
                            return self.yanta_data[category]['general'][param_name]
                        else:
                            # print("CATEGORY "+category+" "+param_name+" OTHER PASSED")
                            for cat_section in self.yanta_data[category]:
                                if param_name in self.yanta_data[category][cat_section]:
                                    # if(isinstance(self.yanta_data[category][cat_section], list)):
                                    #     return True
                                    # else:
                                    return self.yanta_data[category][cat_section][param_name]

        else:
            return self.yanta_data[category]

        return None


    def get_javascript_plugins(self):
        return self.yanta_data['javascript']

    def get_current_style_path(self):
        plugins_dir = self.config('Plugins path')
        style_dir = os.path.join(plugins_dir,"styles",self.config('Default Color Style', None, 'view'))

        if os.path.isfile(style_dir):
            return style_dir

        return None

    def get_extension_definitions(self):
        actions = []
        for viewer in self.yanta_data['viewers']:
            if 'extension_definitions' in self.yanta_data['viewers'][viewer]:
                if "name" in self.yanta_data['viewers'][viewer]['extension_definitions'] and "definitions" in self.yanta_data['viewers'][viewer]['extension_definitions']:
                    actions.append(self.yanta_data['viewers'][viewer]['extension_definitions'])

        return actions

    # def get_default_viewer(self):
    #     return self.yanta_data['viewers'][self.config('Default viewer')]['instance']()

    def get_viewer(self, name):
        return self.yanta_data['viewers'][name]['instance']()

    def available_note_viewers(self):
        return self.yanta_data['viewers']

    def get_viewer_config(self, name):
        default_viewer_config = {}

        if name:
            for prop_name in self.yanta_data['viewers'][name]:
                if prop_name != 'instance':
                    default_viewer_config[prop_name] = self.yanta_data['viewers'][name][prop_name]

        #default_viewer_config = self.yanta_data['viewers'][self.config('Default viewer')]
        #del(default_viewer_config['instance'])
        return default_viewer_config


    def get_default_viewer_obj(self):
        return self.yanta_data['viewers'][self.config('Default viewer')]

    def get_viewers(self):
        return self.yanta_data['viewers']


    def get_styles(self):
        styles = [('', 'No Style')]
        for style in self.yanta_data['styles']:
            styles.append((style, style[:-4][:1].upper() +style[:-4][1:]))

        return styles

    @staticmethod
    def load_class(module, path):
        if path != None:
            sys.path.append(path)

        m = __import__(module)
        m = getattr(m, module)
        return m

    def load_javascript_plugins(self):
        javascript = ''
        plugins_dir = self.config('Plugins path')
        js_plugins_dir = os.path.join(plugins_dir, "js")

        if os.path.exists(js_plugins_dir):
            for dir_file in os.listdir(js_plugins_dir):
                if os.path.isfile(os.path.join(js_plugins_dir,dir_file)) and dir_file.endswith('.js'):
                    with open(os.path.join(js_plugins_dir,dir_file)) as fd:
                        javascript += fd.read()
                        fd.close()

        return javascript

    def load_styles(self):
        styles = []
        plugins_dir = self.config('Plugins path')
        js_plugins_dir = os.path.join(plugins_dir,"styles")

        for dir_file in os.listdir(js_plugins_dir):
            if os.path.isfile(os.path.join(js_plugins_dir,dir_file)) and dir_file.endswith('.css'):
                styles.append(dir_file)

        return styles

    def load_viewers(self):
        plugins_dir = self.config('Plugins path')
        viewers_dir = os.path.join(plugins_dir,'viewers')
        plugin_data = { }

        for dir_file in os.listdir(viewers_dir):

            viewer_path = os.path.join(viewers_dir,dir_file)
            viewer_config_path = os.path.join(viewer_path, 'config.json')

            if os.path.isdir(viewer_path) and os.path.exists(viewer_config_path):
                viewer_config = self.load_jsonfile(viewer_config_path)

                if 'class_file' in viewer_config:
                    if os.path.exists(os.path.join(viewer_path,viewer_config['class_file']+'.py')):
                        plugin_data[dir_file] = {}
                        plugin_data[dir_file]['instance'] = self.load_class(viewer_config['class_file'],viewer_path)
                        plugin_data[dir_file].update(viewer_config)


        return plugin_data


    def load_actions(self):
        actions_dir = self.config('Actions path')

        actions_data = {}

        for dir_file in os.listdir(actions_dir):
            if os.path.isdir(os.path.join(actions_dir, dir_file)):

                current_filepath = os.path.join(actions_dir, dir_file)
                config_filepath = os.path.join(actions_dir, dir_file, 'config.json')

                if os.path.isfile(config_filepath):

                    actions_data[dir_file] = {}
                    action_config = ''

                    with open(config_filepath) as outfile:
                        action_config = json.load(outfile)
                        outfile.close()

                    if action_config is not None:
                        actions_data[dir_file] = action_config
                        actions_data[dir_file]['path'] = current_filepath

                        if os.path.isfile(os.path.join(current_filepath, action_config['class_file']+".py")):
                            actions_data[dir_file]['instance'] = self.load_class(action_config['class_file'],current_filepath)

        return actions_data

    def save_configfile(self,config=None, settings_window_config=None):
        if config is not None:
            if settings_window_config is not None:
                #SETTINGS WINDOW
                names = []
                values = []

                for tab in settings_window_config:
                    for setting_names in tab[0]:
                        if setting_names[0] is not None:
                            names.append(tab[1].lower()+";;;"+setting_names[0])

                for tab in config:
                     for value in tab:
                         if value is not None:
                             values.append(value)

                for index, name in enumerate(names):
                    cat_name = name.split(";;;")
                    self.config(cat_name[1], values[index], cat_name[0])

                self.save_configfile(self.config())
            else:
                #OTHER
                with open(self.yanta_data['config_file'], 'w+') as outfile:
                    json.dump(config, outfile, ensure_ascii=False, sort_keys = False, indent = 2)
                    outfile.close()
        else:
            #pass
            self.save_configfile(self.config())

    def load_jsonfile(self, file):
        json_data = None
        if os.path.isfile(file):
            with open(file) as outfile:
                json_data = json.load(outfile)
                outfile.close()

        return json_data

    def get_sidebuttons_config(self):
        file_path = os.path.join(self.yanta_data['base_dir'], "gui", "sidebuttons.json")
        if os.path.exists(file_path):
            return self.load_jsonfile(file_path)
        else:
            return {}

    def get_toolbar_config(self):
        file_path = os.path.join(self.yanta_data['base_dir'], "gui", "toolbar.json")
        if os.path.exists(file_path):
            return self.load_jsonfile(file_path)
        else:
            return {}

    def load_configfile(self):
        config = None
        if os.path.isfile(self.yanta_data['config_file']):
            with open(self.yanta_data['config_file']) as outfile:
                config = json.load(outfile)
                outfile.close()

            if config is None:
                config = self.reset_configfile()

            # ADDS NECESSARY EXTRA VARS
            config['general']['Actions path'] = os.path.join(self.yanta_data['base_dir'], 'actions')
            config['general']['Libs path'] = os.path.join(self.yanta_data['base_dir'], 'libs')
            config['general']['Plugins path'] = os.path.join(self.yanta_data['base_dir'], 'plugins')

            if not os.path.isdir(config['general']['Notes path']):
                # does not exists, might be:
                # - only subfolder name in var
                # - full path with os change
                # - full path on a usb pen/disk
                # current action: resets to current dir + 'notes' subfolder
                config['general']['Notes path'] = os.path.join(self.yanta_data['base_dir'], 'notes')
                self.save_configfile(config)

                if not os.path.isdir(config['general']['Notes path']):
                    os.makedirs(config['general']['Notes path'])

                config['general']['Notes path'] = os.path.join(self.yanta_data['base_dir'], 'notes')
        else:
            print("No config file found. Generating a new one.")
            self.reset_configfile()

            if os.path.isfile(self.yanta_data['config_file']):
                return self.load_configfile()
            else:
                print("Coud not create a config file. Check for write permissions on the current folder.")

        return config

    def reset_configfile(self):
        config = {}

        config['general'] = { #Variables used by the application
                              #Variables that will changed by the user in the settings window, etc
                              'Default extension': 'html',
                              'Default viewer': 'html_editor',
                              'Notes path': 'notes',
                              'Show Extensions': ['html','htm','txt']
        }

        config['view'] = {  'Show Filetree Sizes': False,
                            'Show Filetree Types': False,
                            'Show Filetree Dates': False,
                            'Default Color Style': 'basic.css',
                            'Apply style in new notes': True,
                            'Apply style in opened notes': False,
                            'Embed Images in notes': True
        }

        config['printer'] = { 'Color Mode': '1',
                              'Orientation': '0',
                              'Paper Size': '0',
                              'Paper Unit': '0',
                              'Paper Margins': '5;5;5;5',
                              'Dots Per Inch': '150'
        }

        self.save_configfile(config)

        return config

    ###### INFO ###################
    def get_default_format(self):
        return self.config('Default format')

    def get_save_extensions(self):
        extensions = {}
        for viewer in self.yanta_data['viewers']:
            if 'save_extensions' in self.yanta_data['viewers'][viewer]:
                for ext in self.yanta_data['viewers'][viewer]['save_extensions']:
                    extensions[ext] = viewer

        return extensions

    def get_open_extensions(self):
        extensions = {}
        for viewer in self.yanta_data['viewers']:
            if 'open_extensions' in self.yanta_data['viewers'][viewer]:
                for ext in self.yanta_data['viewers'][viewer]['open_extensions']:
                    extensions[ext] = viewer

        return extensions

    ###### FILE OPERATIONS ########

    def new_file(self, current_path=None, filename=None):
        default_ext = self.get_default_format()

        if current_path and filename:
            #Detect the dir in which the note will be created
            if(os.path.isdir(current_path)):
                create_directory = current_path
            else:
                create_directory = os.path.dirname(current_path)

            #Add Extesion to the filename - NECESSARY FOR PANDOC
            fileName, fileExtension = os.path.splitext(filename)
            if not fileExtension:
                filename=filename+"."+default_ext

            file_location = os.path.join(create_directory,filename)

            try:
                f = open(file_location, 'w+', encoding='UTF-8')
                f.write(fileName)
                f.close()
                return file_location
            except Exception:
                print("Error creating new file ",file_location)

        return False

    def open_file(self, file_name=None):
        file_content = ""

        if file_name is not None and os.path.isfile(file_name):
            with open(file_name, errors="ignore", encoding='UTF-8') as fd:
                file_content = fd.read() #self.convert_markup(fd.read(), file_name, 'import', 'open')
                # if file_content is not None:
                #     file_content = file_content
                fd.close()

        return file_content.strip()

    def save_file(self, filename=None, content=None):
        if filename is not None and content is not None:
            # with open(filename, "w+") as fd:
            with open(filename, "w+", encoding='UTF-8') as fd:
                fd.write(content)

    def new_folder(self, current_path=None, foldername=None):
        if current_path and foldername:
            #Detect the dir in which the folder will be created
            if(os.path.isdir(current_path)):
                create_directory = current_path
            else:
                create_directory = os.path.dirname(current_path)
            try:
                os.makedirs(os.path.join(create_directory,foldername))
            except Exception:
                print("Error creating new folder ",foldername)


    def delete_filefolder(self, current_path=None):
        if current_path:
            try:
                if(os.path.isdir(current_path)):
                    shutil.rmtree(current_path)
                else:
                    os.unlink(current_path)
            except Exception:
                print("Error deleting the folder/file ",current_path)


    def rename_filefolder(self, current_name=None, new_name=None):
        if current_name and new_name:
            try:
                root_dir = os.path.dirname(current_name)
                #check for extension

                if os.path.isfile(current_name):
                    fileName, fileExtension = os.path.splitext(new_name)
                    if fileExtension:
                        os.rename(current_name,os.path.join(root_dir,new_name))
                    else:
                        fileName_old, fileExtension_old = os.path.splitext(current_name)

                        os.rename(current_name,os.path.join(root_dir, new_name + fileExtension_old))
                else:
                    os.rename(current_name,os.path.join(root_dir,new_name))

            except Exception:
                print("Error renaming the folder/file ",current_name)

    def get_binary_location(self, binary_name):
        if shutil.which(binary_name):
            return shutil.which(binary_name)
        else:
            system = platform.system()
            extension = ''
            if system == 'Windows':
                extension = '.exe'

            for prog_path in ['ProgramFiles','ProgramFiles(x86)','ProgramW6432']:
                if prog_path in os.environ:
                    for prog_folder in [binary_name.lower().capitalize(), binary_name,
                                        binary_name.lower(), binary_name.upper()]:
                        for prog_subfolder in ['','bin','BIN']:
                            for prog_name in [binary_name.lower().capitalize(), binary_name,
                                              binary_name.lower(), binary_name.upper()]:
                                #print(os.path.join(os.environ[prog_path], prog_folder, prog_subfolder, prog_name+extension))
                                if os.path.isfile(os.path.join(os.environ[prog_path], prog_folder, prog_subfolder, prog_name+extension)):
                                    #print(os.path.join(os.environ[prog_path], prog_folder, prog_subfolder, prog_name+extension))
                                    return os.path.join(os.environ[prog_path], prog_folder, prog_subfolder, prog_name+extension)


    def which2(self, program):
        def is_exe(fpath):
            return os.path.exists(fpath) and os.access(fpath, os.X_OK)

        def ext_candidates(fpath):
            yield fpath
            for ext in os.environ.get("PATHEXT", "").split(os.pathsep):
                yield fpath + ext

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                exe_file = os.path.join(path, program)
                for candidate in ext_candidates(exe_file):
                    if is_exe(candidate):
                        return candidate

        return None