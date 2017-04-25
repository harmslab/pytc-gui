import sys

if sys.version_info[0] < 3:
    sys.exit('Sorry, Python < 3.x is not supported')

# Try using setuptools first, if it's installed
from setuptools import setup, find_packages

packages = ["pytc_gui",
            "pytc_gui.sliders",
            "pytc_gui.slider_popup",
            "pytc_gui.exp_frames"]

# Need to add all dependencies to setup as we go!
setup(name='pytc-gui',
      packages=packages,
      version='1.0.1',
      description="PyQt5 GUI for pytc API",
      long_description=open("README.rst").read(),
      author='Hiranmayi Duvvuri',
      author_email='hiranmayid8@gmail.com',
      url='https://github.com/harmslab/pytc-gui',
      download_url='https://github.com/harmslab/pytc-gui/tarball/1.0.0',
      zip_safe=False,
      install_requires=["pytc-fitter","seaborn","pyqt5"],
      classifiers=['Programming Language :: Python'],
      entry_points = {
            'gui_scripts': [
                  'pytc-gui = pytc_gui.main_window:main'
            ]
      })

