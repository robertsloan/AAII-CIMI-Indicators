# AAII-CIMI-Indicators

Based on Al Zmyslowski's Stock Market Review - Technical & Economic Indicators<br>
from the American Association of Individual Investors www.aaii.com<br>
Silicon Valley chapter of the Computerized-Mechanical Investing Group<br>
http://www.siliconvalleyaaii.org/discussiongroups.html<br>

## Current Implementation Architecture
A single file indicators.py whose function it is to:<br>
  Get Data for all indicators to use<br>
  From a 'record-date', which could be todays date or a date in the past, <br>
    calculate the End-Of-Month market day for the previous month (last_EOM_date) the month before that (previous_EOM_date)<br>
  Look for all indicator files in the current directory.  Files in the format I_*.py<br>
  Pass the ticker data, record_date, last_EOM_date, previous_EOM_date and call each indicator file<br>
Each indicator file takes in ticker data, record_date, last_EOM_date, previous_EOM_date <br>
  and returns a dictionary which contains name of the Technical Indicator, Frequency, the result of that indicator for<br>
  the last month and the month before that and any comments.<br>
  The retults are in the form LONG/SHORT and optionally a numeric result of the indicator usually in the form of a %<br>
  e.g. 10 month SMA SPY,	Monthly,	LONG (3.64%),	LONG (7.12%),	 SPY/10 month SMA; 1.0 is lower limit<br>
  
## Original Python Jupyter Notebooks
This repository also includes a folder "Jupyter Notebooks" of the original implementation of Python Jupyter Notebooks Calculating several Stock Market Techical Indicators


