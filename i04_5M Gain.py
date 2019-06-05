"""
5/30/2019
Robert Sloan 

Replicating Al Zmyslowski's AAII CIMI Market Review - Technical & Economic Indicators
Using Yahoo Adjusted Close for SPY and BIL in calculations.

5 month gain - Compare 5 month gain of SPY vs. BIL

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
indicatorType = "5M Gain"

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating", indicatorType)
  # get SPY and BIL data from passed dataframe
  spy_data = dataframe["SPY"]
  bil_data = dataframe["BIL"]

  # Calculate 5 month gains
  spy_5M_gain = spy_data.pct_change(105)
  bil_5M_gain = bil_data.pct_change(105)

  # Determine which has greater gain SPY or BIL
  gain_flag_5M = spy_5M_gain - bil_5M_gain
  gain_flag_5M = gain_flag_5M.dropna()
  # gain is a series with 0 if SPY performed better or -1 if BIL performed better
  gain_flag_5M = gain_flag_5M.apply(lambda x: 0 if x >= 0 else -1) 
 
  # truncate SPY and BIL data to match the length of the gain series
  lengthOfGainFlag = len(gain_flag_5M)
  trunc_spy_data = spy_data[0:lengthOfGainFlag]
  trunc_bil_data = bil_data[0:lengthOfGainFlag]

  # Plot SPY and BIL
  fig, ax = plt.subplots(figsize=(16,9))
  title = indicatorType + "\n" + record_date + "\n areas in green SPY 5M gain is greater areas in red BIL 5M gain is greater"
  ax.set_title(title)
  ax.plot(trunc_spy_data.index, trunc_spy_data, label='SPY')
  ax.plot(trunc_bil_data.index, trunc_bil_data, label='BIL')
  # Add labels and legend
  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price SPY and BIL ($)')
  ax.legend()
  # fillin green or red bars depending if SPY or BIL had a better 5M year gain
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_5M==0, facecolor = 'green', alpha=0.5)
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_5M<0, facecolor = 'red', alpha=0.5)
  fig.savefig("Figures/" + indicatorType +".png") 
  #plt.show()

  # Calculate for Last day of last month
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short
  
  endOfLastMonth_gain_flag_5M = gain_flag_5M.loc[last_EOM_date] 
  endOfLastMonth_spy_5M_gain = str(round((spy_5M_gain.loc[last_EOM_date][0])*100,2))
  endOfLastMonth_bil_5M_gain = str(round((bil_5M_gain.loc[last_EOM_date][0])*100,2))

  if (endOfLastMonth_gain_flag_5M[0] == 0):
      lastMonth_status_5M = 'LONG'
  else:
      lastMonth_status_5M = 'SHORT'
  
  # Calculate for Last day of month before last 
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short
  endOfMonthBeforeLast_gain_flag_5M = gain_flag_5M.loc[previous_EOM_date]
  endOfMonthBeforeLast_spy_5M_gain = str(round((spy_5M_gain[previous_EOM_date][0])*100,2))
  endOfMonthBeforeLast_bil_5M_gain = str(round((bil_5M_gain[previous_EOM_date][0])*100,2))
  if (endOfMonthBeforeLast_gain_flag_5M[0] == 0):
      monthBeforeLast_status_5M = 'LONG'
  else:
      monthBeforeLast_status_5M = 'SHORT'
 
  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d')[0])
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d')[0])

  comment = "SPY 5M Gain > BIL 5M Gain"
  lastMonth_status_5M_str = lastMonth_status_5M + "(" + endOfLastMonth_spy_5M_gain + "%/" + endOfLastMonth_bil_5M_gain + "%)"
  monthBeforeLast_status_5M_str = monthBeforeLast_status_5M + "(" + endOfMonthBeforeLast_spy_5M_gain + "%/" + endOfMonthBeforeLast_bil_5M_gain + "%)"
  indicators = pd.DataFrame([{'Technical Indicator': indicatorType,
                              strLast_EOM_date:lastMonth_status_5M_str, 
                              strPrevious_EOM_date:monthBeforeLast_status_5M_str, 
                              'Comment': comment}], 
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)


  
  return {
          "Technical Indicator": indicatorType,
          "Frequency":"Monthly",
          "MonthBeforeLast":lastMonth_status_5M_str,
          "LastMonth":monthBeforeLast_status_5M_str,
          "Comment":comment} 



