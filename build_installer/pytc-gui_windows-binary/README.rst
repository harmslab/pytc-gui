================================================
Creating a windows binary installer for pytc-gui
================================================

Prep the python environment
---------------------------

+ Download the latest winpython "zero" distribution.  
+ Install it into the pytc-gui_windows-binary\pytc-gui directory.
+ Rename the :code:`WinPython-64bit-3.6.1.0Zero` directory to :code:`winpython64`.  
+ Download windows "wheel" files for numpy and scipy. 
  + make sure you download the :code:`Numpy+MKL` version of numpy.
  + make sure the python version matches your python version.
  + pay attention to 32 bit versus 64 bit.
  + Good source for wheel files: http://www.lfd.uci.edu/~gohlke/pythonlibs/
+ Open "WinPython Command Prompt.exe" within the distribution.
+ type :code:`pip install wheel`
+ type :code:`pip install PATH_TO_NUMPY_WHEEL_FILE`
+ type :code:`pip install PATH_TO_SCIPY_WHEEL_FILE`
+ type :code:`pip install pytc-gui`

Create installer
----------------

+ Install Inno Setup
+ Open "dev\compile-installer.iss"
+ Things to check out:
  + DirectoryRoot
  + MyAppVersion
  + MyAppBits
+ Compile the installer
