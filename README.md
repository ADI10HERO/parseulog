# parseulog

Python wrapper/custom parser for the px4/pyulog tool.

### Prerequisites

> pip install -r requirements.txt

### Steps to use the custom parser

> python parse.py /path/to/ulog/file --plot

_Note: --plot is an optional command line argument passed when we want to see a graph plotted, if we ignore the --plot flag, data will be printed to the std out_

Example:

> python parse.py data\04_50_04.ulg --plot
