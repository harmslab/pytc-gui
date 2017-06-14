======================
pytc-gui documentation
======================

`pytc-gui` is a graphical interface for `pytc <https://github.com/harmslab/pytc>`_,
a flexible package for fitting Isothermal Titration Calorimetry data.  

+ `Installation <installation.html>`_
+ `How to do fits <how_to_img.html>`_
+ `Full pytc docs <https://pytc.readthedocs.io/>`_

Start-up
========

+ Double-click the icon for the installed program OR
+ run :code:`pytc-gui` on command line 

Workflow
========

Demo heat files are `here <https://github.com/harmslab/pytc-demos>`_.

+ Integrate raw power curves using Origin or NITPIC, creating files containing heats per shot.
+ Load heat files and `choose model describing experiment <https://pytc.readthedocs.io/en/latest/indiv_models.html>`_.
+ Choose the `fitter <https://pytc.readthedocs.io/en/latest/fitters.html>`_.
+ Link individual fit parameters to `global parameters <https://pytc.readthedocs.io/en/latest/global_models.html>`_.
+ Fit the model to the data
+ Evaluate the `fit statistics <https://pytc.readthedocs.io/en/latest/statistics.html>`_.
+ Export the results, which will save a csv file and pdf files showing the fit and corner plot

Reference
=========

+ `Programming reference <programming.html>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
