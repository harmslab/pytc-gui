============
Installation 
============

Dependencies
============

* python 3.x
* pyqt5
* pytc
* seaborn

Option 1: push-button installation
----------------------------------

**This is the simplest option if you are not a Python and/or programming nerd.**
This method will install Python 3.6, PyQt5, sip, and Qt5.

Windows 
=======
+ Download the `latest install<https://github.com/harmslab/pytc-gui/blob/master/install/install_scripts/latest_windows.exe>_` file
+ Double click on the file
+ Follow the installation instructions.

Mac/Linux
=========
+ Download the `latest install<https://github.com/harmslab/pytc-gui/blob/master/install/install_scripts/latest_pytc_bash.sh>_` file
+ Open a terminal navigate to the directory where you saved the installation file.
+ Type the following and hit `Enter`.
::

  bash latest_pytc_bash.sh 

Option 2: pip or setup.py
-------------------------
**This method is best if you already have python3 and PyQt5/sip installed.**

Either use pip:
::

  pip3 install pytc-gui

Or git:
::

  git clone https://github.com/harmslab/pytc-gui
  cd pytc-gui
  python3 setup.py install


Option 3: installing PyQt5/sip yourself
---------------------------------------
**If you frequently use python and have at least 3.5 installed, PyQt5/sip can be installed through pip**

to check which version of python3 you are currently using, run the following on terminal:
::

  python3 -V

If you have python > 3.5, run the following in terminal:
::

  pip3 install PyQt5

sip will automatically be downloaded with PyQt5.

if you use anaconda to manage your python3 packages, PyQt5 should already be installed. If not, it can
be installed with the following command:
::

  conda install pyqt


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
