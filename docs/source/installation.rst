============
Installation 
============

windows or mac installation
===========================
**this method requires no familiarity with Python or the command line and will install either a mac .app or windows program**

+ **Windows**: download the `installation file <https://github.com/hrmyd/pytc-gui/blob/master/pytc_install/pytc-gui_v1.0_setup.exe?raw=true>`_ and follow the prompts for the installer. 
+ **Mac**: download the `dmg <https://github.com/hrmyd/pytc-gui/blob/master/pytc_install/pytc-gui_v1.0.1_osx.dmg?raw=true>`_, unpack it, and then drag the pytc icon into the Applications folder.  

pip installation (windows, mac, or linux)
=========================================
**This option requires that python3 and pip3 already be installed (see below).**

Option 1: *pip*.  In a terminal, type:
::

  pip3 install pytc-gui

Option 2: *git*.  In a terminal, type:
::

  git clone https://github.com/harmslab/pytc-gui.git
  cd pytc-gui
  pip3 install .

Installing python3
==================

If you would like to use the pytc API in addition to the GUI, we installing the python
scientific computing stack and then installing pytc-gui via the `pip` method.  You can
obtain python3 from the following sources:

* `Anaconda <https://www.continuum.io/downloads>`_  A single large installation with binaries for windows, mac, and linux.
* `WinPython <https://winpython.github.io/>`_.  A single large installation for windows.
* Package managers (linux). Ubuntu (and other debian variants) would be: :code:`sudo apt-get install python3 python3-pip`
* `python.org <https://www.python.org/downloads/>`_.  The main python binary for windows, mac, and linux. 

A zip of the demo files can be downloaded `here <https://github.com/hrmyd/pytc-gui/blob/master/pytc_install/pytc_demos.zip?raw=true>`_ for use of testing the GUI.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
