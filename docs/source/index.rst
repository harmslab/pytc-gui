======================
pytc-gui documentation
======================

Dependencies
============

* python 3.x
* qtpy
* pytc
* seaborn

QtPy is a wrapper that allows the use of PyQt4, PyQt5, or PySide. The GUI was built using **PyQt5**.

Installation 
=============
+ python 3.x is required in order to install this program, if you don't have it installed you can get it `here <https://www.python.org/downloads/>`_. otherwise, installing from the script will give you the latest version of python3.

setup.py or pip
---------------
**this method is best if you already have PyQt5/sip installed.**

run: 
::

  git clone https://github.com/harmslab/pytc-gui
  cd pytc-gui
  python3 setup.py install

or

::

  pip install pytc-gui


bash or .exe scripts
--------------------
**this method will install Python 3.6, PyQt5, sip, and Qt5**

Windows: download the .exe file, double click on the file, and follow the installation instructions.

Mac/Linux: download the bash file and run the following on terminal and then follow the installation prompts. 
::

  bash pytcreqs-0.1.0-VERSION.sh 


Start-up
========

run :code:`pytc-gui` on command line to run the GUI script

Main Interface
==============

 + add in new experiments
 + until a fit is performed, plot will show the guesses put in from the slider values
 + saving and opening your session allows to save the current experiments being used to save time in reloading each one again later on
 + saving out the data saves out a .csv with fit data as well as the graph from the fit

Documentation - pytc
====================

 + `pytc <https://pytc.readthedocs.io/en/latest/>`_
 + `Fitting models using the script API <http://mybinder.org:/repo/harmslab/pytc-binder>`_.
 + `Description of individual experiment models included in package <https://pytc.readthedocs.io/en/latest/indiv_models.html>`_.
 + `Description of global fits included in package <https://pytc.readthedocs.io/en/latest/global_models.html>`_.
 + `Defining new models <https://pytc.readthedocs.io/en/latest/writing_new_models.html>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
