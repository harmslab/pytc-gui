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
The first link describes how to create an app from scratch using an anaconda environment. the pytc.app file is a folder containing all of the necessary information for the app. Updating the app packages is pretty easy on the command line.

+ Download the `environment file <https://github.com/hrmyd/pytc-gui/blob/master/build_installer/pytc-gui_osx/environment.yml?raw=true>`_ for the gui
+ Create the environment on your computer using the command :code:`conda env create -f environment.yml`
+ Activate the environment with :code:`source activate pytc-gui`
+ While in the environment, go to the folder with the **setup.py** file and run :code:`pip install .` to update the version of pytc-fitter and pytc-gui, and anything else that needs to be updated, in the environment.
+ Deactivate the environment with :code:`source deactivate`
+ To copy the environment to the resources folder of the .app folder, run :code:`cp -R ~/anaconda3/envs/pytc-gui/* ~/pytc-gui.app/Contents/Resources/` while making sure all paths are correct for your machine.
+ In the Resources folder, you can safely delete the **conda-meta** and the **include** folders.
+ Now, just make sure the app properly runs when you double click it 
+ The Info.plist file under the Contents folder can be easily updated using Xcode

Creating the dmg
----------------
+ The dmg was created using **DMG Canvas**
+ Download the template made `here <https://github.com/hrmyd/pytc-gui/blob/master/build_installer/pytc-gui_osx/installer_template.dmgCanvas?raw=true>`_
+ To update the dmg, just replace the current pytc.app with the newly updated version and save out/build your dmg
+ You can also create a dmg by hand using the second link and **Disk Utility**
