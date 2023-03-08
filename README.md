The application requires Python 3 and the following packages:
  tkinter: 		the GUI front end
  pandas: 		handles data as tables and data import & export 
  pandastable: 	presents a panda dataframe as a table object
  numpy:		performs mathematical calculations and random operations
  matplotlib: 	charting of data
  datetime:		handles date operations for the 5-year lookback
  dateutil:		handles date operations for the 5-year lookback
  yfinance:		package to pull financial data from Yahoo Finance
  os: 			connects to the operating system to delete a file

Missing libraries can be installed at a terminal prompt as:
"pip install {missing package name}"

Your version of Python can be viewed via a terminal prompt as:
"python --version"

Search your steps for installing Python 3 if missing.

The two files comprising the application are MonteCarloCore.py and mc_lib.py.
The application is launched via the following terminal prompt:
"python MonteCarloCore.py"

Two Jupyter Notebooks (*.ipynb) are also included that were used for prototyping.
