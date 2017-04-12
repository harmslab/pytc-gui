======================
pytc-gui documentation
======================

Dependencies
============

* python 3.x
* pyqt5
* pytc
* seaborn

The GUI was built using **PyQt5**.

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

the gui can also be pip installed
::

  pip3 install pytc-gui


installing PyQt5/sip yourself
-----------------------------
**if you frequently use python and have at least 3.5 installed, PyQt5/sip can be installed through pip**

to check which version of python3 you are currently using, run the following on terminal:
::

  python3 -V

run the following in terminal:
::

  pip3 install PyQt5

sip will automatically be downloaded with PyQt5.

if you use anaconda to manage your python3 packages, PyQt5 should already be installed. if not, it can
be installed with the following command:
::

  conda install pyqt


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
 + saving out the data saves out a .csv with fit data as well as the graph from the fit
 + adjust each parameter for an experiment using the sliders

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   how_to_img.rst
   gui_module.rst

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
