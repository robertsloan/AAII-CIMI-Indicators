"""
6/3/2019
Robert Sloan

Replicating Al Zmyslowski's AAII CIMI Market Review - Technical & Economic Indicators
Using Yahoo Adjusted Close for SPY and BIL in calculations.

FundX Score - Compare FundX Score of SPY vs BIL
Where FundX Score = average of (1 month + 3M + 5M + 12M gains) If SPY<BIL go to cashTODO

  Find out why some areas of the graph are not boxed in green (SPY better) or red (BIL better)

"""

# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
# this library load is because pandas matplotlib FutureWarning
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
indicatorType = "FundX Score"

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating", indicatorType)
  # get SPY and BIL data from passed dataframe
  spy_data = dataframe["SPY"]
  bil_data = dataframe["BIL"]

  # Calculate 1, 3, 6 month gains
  spy_1M_gain = spy_data.pct_change(21)
  bil_1M_gain = bil_data.pct_change(21)
  spy_3M_gain = spy_data.pct_change(3*21)
  bil_3M_gain = bil_data.pct_change(3*21)
  spy_6M_gain = spy_data.pct_change(6*21)
  bil_6M_gain = bil_data.pct_change(6*21)
  spy_12M_gain = spy_data.pct_change(252)
  bil_12M_gain = bil_data.pct_change(252)

  spy_fundX_score = (spy_1M_gain + spy_3M_gain + spy_6M_gain + spy_12M_gain)/4
  bil_fundX_score = (bil_1M_gain + bil_3M_gain + bil_6M_gain + bil_12M_gain)/4

  # Determine which has greater gain SPY or BIL
  gain_flag_FX = spy_fundX_score - bil_fundX_score
  gain_flag_FX = gain_flag_FX.dropna()
  # gain is a series with 0 if SPY performed better or -1 if BIL performed better
  gain_flag_FX = gain_flag_FX.apply(lambda x: 0 if x >= 0 else -1)

  # truncate SPY and BIL data to match the length of the gain series
  lengthOfGainFlag = len(gain_flag_FX)
  trunc_spy_data = spy_data[0:lengthOfGainFlag]
  trunc_bil_data = bil_data[0:lengthOfGainFlag]

  # Plot SPY and BIL
  fig, ax = plt.subplots(figsize=(16,9))
  title = indicatorType + "\n" + record_date + "\n areas in green SPY FundX gain is greater areas in red BIL FundX is greater"
  ax.set_title(title)
  ax.plot(trunc_spy_data.index, trunc_spy_data, label='SPY')
  ax.plot(trunc_bil_data.index, trunc_bil_data, label='BIL')
  # Add labels and legend
  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price SPY and BIL ($)')
  ax.legend()
  # fillin green or red bars depending if SPY or BIL had a better FundX Score
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_FX==0, facecolor = 'green', alpha=0.5)
  ax.fill_between(trunc_spy_data.index, 80, 300, where = gain_flag_FX<0, facecolor = 'red', alpha=0.5)
  indicatorName = "i06_1FundX Score"
  filepath = "Figures/"+record_date+"_"+indicatorName+".png"
  if os.path.exists(filepath) == False:
      fig.savefig(filepath)
  #fig.savefig("Figures/" + indicatorType +".png")
  #plt.show()

  # Calculate for Last day of last month
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short

  endOfLastMonth_gain_flag_FX = gain_flag_FX.loc[last_EOM_date]
  endOfLastMonth_spy_fundX_score = str(round((spy_fundX_score.loc[last_EOM_date][0])*100,2))
  endOfLastMonth_bil_fundX_score = str(round((bil_fundX_score.loc[last_EOM_date][0])*100,2))

  if (endOfLastMonth_gain_flag_FX[0] == 0):
      lastMonth_status_FX = 'LONG'
  else:
      lastMonth_status_FX = 'SHORT'

  # Calculate for Last day of month before last
  # If the 5 month SPY gain greater than BIL go LONG
  # otherwise go Short
  endOfMonthBeforeLast_gain_flag_FX = gain_flag_FX.loc[previous_EOM_date]
  endOfMonthBeforeLast_spy_fundX_score = str(round((spy_fundX_score[previous_EOM_date][0])*100,2))
  endOfMonthBeforeLast_bil_fundX_score = str(round((bil_fundX_score[previous_EOM_date][0])*100,2))
  if (endOfMonthBeforeLast_gain_flag_FX[0] == 0):
      monthBeforeLast_status_FX = 'LONG'
  else:
      monthBeforeLast_status_FX = 'SHORT'

  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d')[0])
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d')[0])

  comment = "SPY FX Score > BIL FX Score"
  lastMonth_status_FX_str = lastMonth_status_FX + "(" + endOfLastMonth_spy_fundX_score + "%/" + endOfLastMonth_bil_fundX_score + "%)"
  monthBeforeLast_status_FX_str = monthBeforeLast_status_FX + "(" + endOfMonthBeforeLast_spy_fundX_score + "%/" + endOfMonthBeforeLast_bil_fundX_score + "%)"
  indicators = pd.DataFrame([{'Technical Indicator': indicatorType,
                              strLast_EOM_date:lastMonth_status_FX_str,
                              strPrevious_EOM_date:monthBeforeLast_status_FX_str,
                              'Comment': comment}],
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)



  return {
          "Technical Indicator": indicatorType,
          "Frequency":"Monthly",
          "MonthBeforeLast":monthBeforeLast_status_FX_str,
          "LastMonth":lastMonth_status_FX_str,
          "Comment":comment}
