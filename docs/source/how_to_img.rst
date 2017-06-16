:orphan:

===========================
How-To: Basic Fits with GUI
===========================

Workflow
========

+ Integrate raw power curves using Origin or `NITPIC  <http://biophysics.swmed.edu/MBR/software.html>`_,
  creating files containing heats per shot.  A collection of demo heat files
  are available `on github <https://github.com/harmslab/pytc-demos>`_.
+ Load heat files and `choose model describing experiment <https://pytc.readthedocs.io/en/latest/indiv_models.html>`_.
+ Choose the `fitter <https://pytc.readthedocs.io/en/latest/fitters.html>`_.
+ Link individual fit parameters to `global parameters <https://pytc.readthedocs.io/en/latest/global_models.html>`_.
+ Fit the model to the data.
+ Evaluate the `fit statistics <https://pytc.readthedocs.io/en/latest/statistics.html>`_.
+ Export the results, which will save a csv file and pdf files showing the fit and corner plot.

Example fit
===========

The following shows an example fit to :math:`Ca^{2+}` binding to :math:`EDTA`. 
The data file can be found `here <https://github.com/harmslab/pytc-demos/blob/master/ca-edta/hepes-01.DH>`_.  

.. figure:: /screenshots/fit_steps/0.png
    :figclass: align-center

    To load an experiment, go to :code:`File -> Add Experiment`. 

.. figure:: /screenshots/fit_steps/1.png
    :figclass: align-center

    Select the heat file, select the model and set the experiment parameters.

.. figure:: /screenshots/fit_steps/2.png
    :figclass: align-center

    Before fitting, the graph shows the model calculated using the parameter
    guesses.

.. figure:: /screenshots/fit_steps/3.png
    :figclass: align-center

    To alter the fit parameters, click the button next to the experiment.

.. figure:: /screenshots/fit_steps/4.png
    :figclass: align-center

    In the window that opens, you can set parameter guess, link the fit 
    parameters to global parameters, fix them, and set fit bounds.

.. figure:: /screenshots/fit_steps/5.png
    :figclass: align-center

    Click the "Do Fit" button to do the fit.

.. figure:: /screenshots/fit_steps/6.png
    :figclass: align-center

    The fit now appears, with residuals, fit statistics, and parameter values.

.. figure:: /screenshots/fit_steps/7.png
    :figclass: align-center

    The "Corner Plot" tab shows the uncertainty and covariation between the fit
    parameters.

.. figure:: /screenshots/fit_steps/8.png
    :figclass: align-center

    The fit results can be exported by going to File->Export Results.

This can be repeated for more experiments.  Any new experiments you load will be
added to the GUI. 

Videos of fits
==============

**Maximum likelihood single-site fit**

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/AebnhMiKwNk" frameborder="0" allowfullscreen></iframe>
    </div>

**Bayesian single-site fit**

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/aH2iv4duoTQ" frameborder="0" allowfullscreen></iframe>
    </div>

**Model selection using an AIC test**

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/pNju0ESpXEo" frameborder="0" allowfullscreen></iframe>
    </div>

**Simple global fit**

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/j_1MEPM6BeU" frameborder="0" allowfullscreen></iframe>
    </div>

**Van't Hoff connector fit**

.. raw:: html

    <div style="position: relative; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/nKFXZrssUm8" frameborder="0" allowfullscreen></iframe>
    </div>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
