import sys

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python < 3.x is not supported')

# Try using setuptools first, if it's installed
from setuptools import setup, find_packages

packages = ["pytc_gui",
            "pytc_gui/dialogs",
            "pytc_gui/widgets",
            "pytc_gui/widgets/experiment_box",
            "pytc_gui/widgets/experiment_box/experiment_dialog"]

# Need to add all dependencies to setup as we go!
setup(name='pytc-gui',
      packages=packages,
      version='1.2.1',
      description="PyQt5 GUI for pytc API",
      long_description=open("README.rst").read(),
      author='Hiranmayi Duvvuri',
      author_email='hiranmayid8@gmail.com',
      url='https://github.com/harmslab/pytc-gui',
      download_url='https://github.com/harmslab/pytc-gui/tarball/1.2.1',
      zip_safe=False,
      install_requires=["pytc-fitter>=1.1.4","seaborn","pyqt5"],
      package_data={"pytc_gui":["*.png","widgets/experiment_box/icons/*.png"]},
      classifiers=['Programming Language :: Python'],
      entry_points = {
            'gui_scripts': [
                  'pytc-gui = pytc_gui.main_window:main'
            ]
      })

