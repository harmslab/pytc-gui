#!/bin/bash

git clone https://github.com/harmslab/pytc.git
git clone https://github.com/harmslab/pytc-gui.git

python3 pytc/setup.py install
python3 pytc-gui/setup.py install