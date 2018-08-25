==============================
Updating the MacOSX .app file
==============================

Resources Used
--------------
+ `Creating a Mac OSX app from an anaconda environment <https://dschreij.github.io/how-to/package-anaconda-environments-as-apps>`_
+ `How to create installation dmg files <http://ramezanpour.net/post/2014/05/12/how-to-create-installation-dmg-files-in-os-x/>`_
+ `Alternative quick and easy dmg file creator <http://www.araelium.com/dmgcanvas>`_

Updating the Resources folder
-----------------------------
The first link describes how to create an app from scratch using Conda_. If you don't have Conda, first install Miniconda here_.

.. _Conda: https://conda.io/docs/index.html
.. _here: https://conda.io/miniconda.html

1. For the mac app only, in the **main_window.py** file under the **Main** class, find the line with :code:`menu.setNativeMenuBar(False)` and set it to :code:`True` before installing it to the environment. You can change it back after installing it to the conda environment.
2. Navigate to the Conda ``environment.yml`` file in ``build_installer/pytc-gui_osx/environment.yml``. Here, you can update dependencies for the GUI. Change the version numbers listed next to each package.
3. Once you've updated this file, create a new conda environment from this file using the command :code:`conda env create -f environment.yml`
4. Activate the conda environment with :code:`source activate pytc-gui`
5. While in the environment, go to the folder with the **setup.py** file and run :code:`pip install .` to install the updated pytc-gui.
6. Deactivate the environment with :code:`source deactivate`.
7. Copy the whole environment to the ``Contents/Resources`` folder of the `pytc.app` folder using the following steps:

   1. Run `conda info`.

      .. code-block::

        active environment : pytc-gui
        active env location : /Users/username/miniconda3/envs/pytc-gui
        shell level : 1
        user config file : /Users/username/.condarc
        populated config files : /Users/username/.condarc
        conda version : 4.5.9
        conda-build version : not installed
        python version : 3.6.3.final.0
        base environment : /Users/username/miniconda3  (writable)
        channel URLs : https://repo.anaconda.com/pkgs/main/osx-64
                       https://repo.anaconda.com/pkgs/main/noarch
                       https://repo.anaconda.com/pkgs/free/osx-64
                       https://repo.anaconda.com/pkgs/free/noarch
                       https://repo.anaconda.com/pkgs/r/osx-64
                       https://repo.anaconda.com/pkgs/r/noarch
                       https://repo.anaconda.com/pkgs/pro/osx-64
                       https://repo.anaconda.com/pkgs/pro/noarch
        package cache : /Users/username/miniconda3/pkgs
                        /Users/username/.conda/pkgs
        envs directories : /Users/username/miniconda3/envs
                           /Users/username/.conda/envs
        platform : osx-64
        netrc file : None
        offline mode : False

   2. Copy the path next to ``active env location`` (it should end with ``pytc-gui``).
   3. Copy the contents of this directory into the ``pytc.app/Contents/Resources/`` directory.

      Example:

      .. code-block::

        cp -R /Users/username/miniconda3/envs/pytc-gui/* build_installer/pytc-gui_osx/pytc.app/Contents/Resources/

8. In the Resources folder, you can safely delete the **conda-meta** and the **include** folders.
9. Check that the app properly runs by double opening ``pytc.app``. Either double click the app, or run ``open pytc.app`` from the command line.


Creating the dmg
----------------

Following any of the methods here: https://www.wikihow.com/Make-a-DMG-File-on-a-Mac
