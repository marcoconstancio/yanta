# Yanta

Yanta a simple note taking application built in python. It can save text notes in txt files and more complex notes.

![Screenshot 1](screenshot1.jpg)

## Instalation

For installation you need to install (tested on linux and windows 8.1)

* Python 3 - https://www.python.org/
* PyQt <=5.5 - https://sourceforge.net/projects/pyqt/files/PyQt5/

## Running

Run the command: 

	python yanta.py

or the shorcuts: `run.sh` for linux and `run.bat` for windows.

## Compiling (Windows)

You can run the application normally if install the mentioned dependecies but if you want build a windows binary for a more portability you need to install [cx_freeze](http://cx-freeze.sourceforge.net/) python package. If you installed the `pip` package during the python install just run the command:

	pip install cx_Freeze

and run the `build_exe.bat` file in application folder.
