Stock Tool
==========

A command line stock quote tool written in python. Can be used for Geektool.

Installation
============

```bash
cd stocks
pip install -r requirements.txt
python stocks.py stocks.txt
```

For Geektool, open the included Geeklet.
Modify the paths of stocks.py and stocks.txt to the correct location.
Also, change the path to your bash_profile so that the correct python version
and executable are loaded (the one that executes in the python environment
with beautifulsoup installed).

Configuration
=============

The stocks.txt argument is a file that contains a list of ticker symbols, each
on their own line.
