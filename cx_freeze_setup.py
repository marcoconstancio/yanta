import sys
from cx_Freeze import setup, Executable

########################################
#Here is a list of the build_exe options
########################################
#1) append the script module to the executable
append_script_to_exe=False
#2) the name of the base executable to use which, if given as a relative path, will be joined with the bases subdirectory of the cx_Freeze installation; the default value is "Console"
base="Console"
#3) list of names of files to exclude when determining dependencies of binary files that would normally be included; note that version numbers that normally follow the shared object extension are stripped prior to performing the comparison
bin_excludes=[]
#4) list of names of files to include when determining dependencies of binary files that would normally be excluded; note that version numbers that normally follow the shared object extension are stripped prior to performing the comparison
bin_includes=[] 
#5) list of paths from which to exclude files when determining dependencies of binary files
bin_path_excludes=[]
#6) list of paths from which to include files when determining dependencies of binary files
bin_path_includes=[]
#7) directory for built executables and dependent files, defaults to build/
build_exe="E:\\Build\\"
#8) create a compressed zip file
compressed=False
#9) comma separated list of constant values to include in the constants module called BUILD_CONSTANTS in form <name>=<value>
constants=[]
#10) copy all dependent files
copy_dependent_files=True
#11) create a shared zip file called library.zip which will contain all modules shared by all executables which are built 
create_shared_zip=False
#12) comma separated list of names of modules to exclude
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
#13) include the icon in the frozen executables on the Windows platform and alongside the frozen executable on other platforms
icon=False
#13) comma separated list of names of modules to include
## INSTALL DEPENDECIES
# pip install cssselect webob requests
### LXML BINARIES IN http://www.lfd.uci.edu/~gohlke/pythonlibs/
### lxml-3.6.4-cp34-cp34m-win32.whl file for python 3.4 32bits
# pip install lxml-3.6.4-cp34-cp34m-win32.whl
includes = [
	"json",
	"cssselect",
	"webob",
	"email",
	"requests",
	"lxml",
	"lxml._elementpath",
	"lxml.etree",
	"lxml.html",
	"lxml.ElementInclude",
	"xml.etree.ElementTree",
    "xml.etree.ElementPath",
	"PyQt5.QtCore",
	"PyQt5.QtGui",
	"PyQt5.QtPrintSupport"]
#15) list containing files to be copied to the target directory; 
#  it is expected that this list will contain strings or 2-tuples for the source and destination; 
#  the source can be a file or a directory (in which case the tree is copied except for .svn and CVS directories); 
#  the target must not be an absolute path
#
# NOTE: INCLUDE FILES MUST BE OF THIS FORM OTHERWISE freezer.py line 128 WILL TRY AND DELETE dist/. AND FAIL!!!
# Here is a list of ALL the DLLs that are included in Python27\Scripts 
include_files=[
			"actions\\",
			"gui\\",
			"libs\\",
			"libs\\python\\FileTreeview.py",
			"libs\\python\\NoteFunctions.py",
			"libs\\python\\NoteViewer.py",
			"libs\\python\\formlayout",
			"libs\\python\\pyquery",
			"notes\\",
			"plugins\\"
            ]
#16) include the script module in the shared zip file
include_in_shared_zip=False
#17) include the Microsoft Visual C runtime DLLs and (if necessary) the manifest file required to run the executable without needing the redistributable package installed
include_msvcr =True
#18) the name of the script to use during initialization which, if given as a relative path, will be joined with the initscripts subdirectory of the cx_Freeze installation; the default value is "Console"
init_script=""
#19) comma separated list of packages to be treated as namespace packages (path is extended using pkgutil)
namespace_packages=[]
#20) optimization level, one of 0 (disabled), 1 or 2
optimize=0
#21) comma separated list of packages to include, which includes all submodules in the package
packages = []
#22) comma separated list of paths to search; the default value is sys.path
path = []
#23) Modify filenames attached to code objects, which appear in tracebacks. Pass a comma separated list of paths in the form <search>=<replace>. The value * in the search portion will match the directory containing the entire package, leaving just the relative path to the module.
replace_paths=[]
#24) suppress all output except warnings  
silent=False
#25) list containing files to be included in the zip file directory; it is expected that this list will contain strings or 2-tuples for the source and destination
zip_includes=[]

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
   base = "Win32GUI"

setup(  name = "yanta",
        version = "0.1",
		author = 'Marco Constâncio',
        description = "yanta",
		options = {"build_exe": {
                           # "append_script_to_exe": append_script_to_exe,
                           # "base":                 base,
                           # "bin_excludes":         bin_excludes,
                           # "bin_includes":         bin_includes,
                           # "bin_path_excludes":    bin_path_excludes,
                           # "bin_path_includes":    bin_path_includes,
						 	# "build_exe":            build_exe,
							# "compressed":           compressed,
                           # "constants":            constants,
							# "copy_dependent_files": copy_dependent_files,
                           # "create_shared_zip":    create_shared_zip,
							"excludes":             excludes,
                           # "icon":                 icon,
							"includes":             includes,
							"include_files":        include_files,
                           # "include_in_shared_zip":include_in_shared_zip,
                           # "include_msvcr":        include_msvcr,
                           # "init_script":          init_script,
                           # "namespace_packages":   namespace_packages,
                           # "optimize":             optimize,
							"packages":             packages,
							"path":                 path,
                           # "replace_paths":        replace_paths,
                           # "silent":               silent,
                           # "zip_includes":         zip_includes,
							}
				},
        executables = [Executable("yanta.py", base=base)]
		)
