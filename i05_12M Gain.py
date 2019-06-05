"""
6/3/2019
Robert Sloan 

Replicating Al Zmyslowski's AAII CIMI Market Review - Technical & Economic Indicators
Using Yahoo Adjusted Close for SPY and BIL in calculations.

12M gain - Compare 12 month gain of SPY vs. BIL 
TODO 

  Find out why some areas of the graph are not boxed in green (SPY better) or red (BIL better)
  
"""

# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt
# this library load is because pandas matplotlib FutureWarning
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
indicatorType = "12M Gain"

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating", indicatorType)
  # get SPY and BIL data from passed dataframe
  spy_data = dataframe["SPY"]
  bil_data = dataframe["BIL"]
  
  # Calculate 12 month gains
  spy_12M_gain = spy_data.pct_change(252)
  bil_12M_gain = bil_data.pct_change(252)

  # Determine which has greater gain SPY or BIL
  gain_flag_12M = spy_12M_gain - bil_12M_gain
  gain_flag_12M = gain_flag_12M.dropna()
  # gain is a series with 0 if SPY performed better or -1 if BIL performed better
  gain_flag_12M = gain_flag_12M.apply(lambda x: 0 if x >= 0 else -1) 
 
  # truncate SPY and BIL data to match the length of the gain series
  lengthOfGainFlag = len(gain_flag_12M)
  trunc_spy_data = spy_data[0:lengthOfGainFlag]
  trunc_bil_data = bil_data[0:lengthOfGainFlag]

  # Plot SPY and BIL
  fig, ax = plt.subplots(figsize=(16,9))
  title = indicatorType + "\n" + record_date + "\n areas in green SPY 1 year gain is greater areas in red BIL 1 year gain is greater"
  ax.set_title(title)
  ax.plot(trunc_spy_data.index, trunc_spy_data, label='SPY')
  ax.plot(trunc_bil_data.index, trunc_bil_data, label='BIL')
  # Add labels and legend
  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price SPY and BIL ($)')
  ax.legend()
  # fillin green or red bars depending if SPY or BIL had a better 12M year gain
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_12M==0, facecolor = 'green', alpha=0.5)
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_12M<0, facecolor = 'red', alpha=0.5)
  fig.savefig("Figures/" + indicatorType +".png") 
  #plt.show()

  # Calculate for Last day of last month
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short
  
  endOfLastMonth_gain_flag_12M = gain_flag_12M.loc[last_EOM_date] 
  endOfLastMonth_spy_12M_gain = str(round((spy_12M_gain.loc[last_EOM_date][0])*100,2))
  endOfLastMonth_bil_12M_gain = str(round((bil_12M_gain.loc[last_EOM_date][0])*100,2))

  if (endOfLastMonth_gain_flag_12M[0] == 0):
      lastMonth_status_12M = 'LONG'
  else:
      lastMonth_status_12M = 'SHORT'
  
  # Calculate for Last day of month before last 
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short
  endOfMonthBeforeLast_gain_flag_12M = gain_flag_12M.loc[previous_EOM_date]
  endOfMonthBeforeLast_spy_12M_gain = str(round((spy_12M_gain[previous_EOM_date][0])*100,2))
  endOfMonthBeforeLast_bil_12M_gain = str(round((bil_12M_gain[previous_EOM_date][0])*100,2))
  if (endOfMonthBeforeLast_gain_flag_12M[0] == 0):
      monthBeforeLast_status_12M = 'LONG'
  else:
      monthBeforeLast_status_12M = 'SHORT'
 
  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d')[0])
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d')[0])

  comment = "SPY 12M Gain > BIL 12M Gain"
  lastMonth_status_12M_str = lastMonth_status_12M + "(" + endOfLastMonth_spy_12M_gain + "%/" + endOfLastMonth_bil_12M_gain + "%)"
  monthBeforeLast_status_12M_str = monthBeforeLast_status_12M + "(" + endOfMonthBeforeLast_spy_12M_gain + "%/" + endOfMonthBeforeLast_bil_12M_gain + "%)"
  indicators = pd.DataFrame([{'Technical Indicator': indicatorType,
                              strLast_EOM_date:lastMonth_status_12M_str, 
                              strPrevious_EOM_date:monthBeforeLast_status_12M_str, 
                              'Comment': comment}], 
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)


  
  return {
          "Technical Indicator": indicatorType,
          "Frequency":"Monthly",
          "MonthBeforeLast":lastMonth_status_12M_str,
          "LastMonth":monthBeforeLast_status_12M_str,
          "Comment":comment} 



