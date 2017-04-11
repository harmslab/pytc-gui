===========================
How-To: Basic Fits with GUI
===========================

Setting Up
==========

Single-Site Model
-----------------
for performing a simple single-site model fit.

.. figure:: /screenshots/fitting/01.png
	:width: 40%
	:figclass: align-center

	First, go to File > Add Experiment. Select the model, load in the file, and shot start. Repeat for each experiment/blank.

.. figure:: /screenshots/fitting/02.png
	:figclass: align-center

	before fitting, graph shows the parameter guesses of each experiment that has been loaded in.

.. figure:: /screenshots/fitting/03.png
	:figclass: align-center

	To perform a fit, go to Fitting -> Fit Experiments.

This can be repeated for any model you'd like to fit. Any new models you make will automatically be updated in the GUI. 

Connecting to Global Variables
==============================

Simple Global
-------------
.. figure:: /screenshots/global_var/01.png
	:width: 60%
	:figclass: align-center

	The sliders for each experiment show up in a pop-up when you click on **Show Sliders** next to the experiment name. Each pop-up has this general layout. To add a new global variable, select **Add Global Var** from the dropdown.

.. figure:: /screenshots/global_var/02.png
	:width: 40%
	:figclass: align-center

	This pop-up will show up and allow you to name the global variable.

.. figure:: /screenshots/global_var/03.png
	:width: 60%
	:figclass: align-center

	Once a global variable is made, it can be connected to any parameter by selecting it from the dropdown menu for that parameter.

.. figure:: /screenshots/global_var/04.png
	:figclass: align-center

	A new entry is made for the global variable. After this select Fitting > Fit Experiments. The parameter box and graph will update for the new linked fit.

Connectors
----------
.. figure:: /screenshots/global_var/05.png
	:width: 40%
	:figclass: align-center

	Connectors are linked in a similar way, except instead select **Add Connector** from the dropdown menu. A new pop-up will come up allowing you to select the type of connector you'd like to make, the name, and any general variables linked to the connector.

.. figure:: /screenshots/global_var/06.png
	:width: 60%
	:figclass: align-center

	Again, link parameters to a connector parameter by selecting the connector from the dropdown menu.

.. figure:: /screenshots/global_var/07.png
	:figclass: align-center

	Some connectors might require some variables to be defined for a specific experiment, these need to be defined before performing the new fit.

.. figure:: /screenshots/global_var/08.png
	:figclass: align-center

	Once everything is set, perform the new fit.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
