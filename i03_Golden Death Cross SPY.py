"""
5/30/2019
Robert Sloan

Replicating Al Zmyslowski's AAII CIMI Market Review - Technical & Economic Indicators<br>
Death/Golden Cross SPDR S&P 500 ETF (SPY)<br>
Using Yahoo Adjusted Close for SPY in calculations.<br>
This measures the 50 day simple moving average (SMA) vs the 200 day SMA on the SPY.<br>
If the 50 day is above the 200 day SMA conditions are bullish; if below the 200 day conditions are bearish.<br>

TODO
  Verify how to calculate %
  Add Red and Green bars on graph to show Long and Short regions


"""
# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating Death Golden Cross SPY")
  # this library load is because pandas matplotlib FutureWarning
  from pandas.plotting import register_matplotlib_converters
  register_matplotlib_converters()
  # get SPY data from passed dataframe
  spy_data = dataframe["SPY"]

  # Get the spy_data timeseries. This now returns a Pandas Series object indexed by date.

  # Calculate the fifty day and 200 day simple moving averages of the closing prices of the SPY
  spy_50d_sma = spy_data.rolling(window=50).mean()
  spy_200d_sma = spy_data.rolling(window=200).mean()

  # Plot everything by leveraging the very powerful matplotlib package
  fig, ax = plt.subplots(figsize=(16,9))
  title = "Death Golden Cross SPY\n" + record_date
  ax.set_title(title)
  ax.plot(spy_data.index, spy_data, label='SPY')
  ax.plot(spy_50d_sma.index, spy_50d_sma, label='50 day SPY SMA')
  ax.plot(spy_200d_sma.index, spy_200d_sma, label='200 day SPY SMA')
  plt.axvline(x=previous_EOM_date, color='k', linestyle='--') # add vertical dashed line for previous_EOM_date
  plt.axvline(x=last_EOM_date, color='k', linestyle='--')     # add vertical dashed line for last_EOM_date

  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price SPY ($)')
  ax.legend()
  fig.savefig("Figures/Death Golden Cross.png")
  #plt.show()

  # Last day of last month 50 day and 200 day SPY SMA
  # Current Day 50 day and 200 day SPY SMA
  endOfLastMonth_spy = spy_data.loc[last_EOM_date]

  # print("endOfLastMonth_spy " + str(endOfLastMonth_spy))
  endOfLastMonth_50d_sma = spy_50d_sma.loc[last_EOM_date]
  # print("50 day " + str(endOfLastMonth_50d_sma))
  endOfLastMonth_200d_sma = spy_200d_sma.loc[last_EOM_date]
  # print("200 day " + str(endOfLastMonth_200d_sma))
  # Determin if 50 day SPY SMA is greater than 200 day SMA and how much
  cross_spy = float(endOfLastMonth_50d_sma - endOfLastMonth_200d_sma)
  # print("50 day SMA - 200 day SMA " + str(cross_spy))
  cross_spy_percent = round(cross_spy/endOfLastMonth_spy,1)
  # print(cross_spy_percent)
  if (cross_spy>1):
      lastMonth_status_cross = 'LONG'
  else:
      lastMonth_status_cross = 'SHORT'
  # print("lastMonth_status_cross = ", lastMonth_status_cross)

# Last day of last month 50 day and 200 day SPY SMA
  endOfMonthBeforeLast_spy = spy_data.loc[previous_EOM_date]
  # print("endOfMonthBeforeLast_spy " + str(endOfMonthBeforeLast_spy))
  endOfMonthBeforeLast_50d_sma = spy_50d_sma.loc[previous_EOM_date]
  # print("50 day " + str(endOfMonthBeforeLast_50d_sma))
  endOfMonthBeforeLast_200d_sma = spy_200d_sma.loc[previous_EOM_date]
  # print("200 day " + str(endOfMonthBeforeLast_200d_sma))
  # Determin if 50 day SPY SMA is greater than 200 day SMA and how much
  cross_spy = float(endOfMonthBeforeLast_50d_sma - endOfMonthBeforeLast_200d_sma)
  # print("50 day SMA - 200 day SMA " + str(cross_spy))
  cross_spy_percent = round(cross_spy/endOfMonthBeforeLast_spy,1)
  # print(cross_spy_percent)
  if (cross_spy>1):
      monthBeforeLast_status_cross = 'LONG'
  else:
      monthBeforeLast_status_cross = 'SHORT'
  # print("monthBeforeLast_status_cross = ", monthBeforeLast_status_cross)

  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d'))
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d'))

  comment = "50d/200d EMA crossover"
  indicators = pd.DataFrame([{'Technical Indicator': 'Golden/Death Cross SPY',
                              strLast_EOM_date:lastMonth_status_cross,
                              strPrevious_EOM_date:monthBeforeLast_status_cross,
                              'Comment': comment}],
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)



  return {
          "Technical Indicator": "Golden/Death Cross SPY",
          "Frequency":"Daily",
          "MonthBeforeLast":monthBeforeLast_status_cross,
          "LastMonth":lastMonth_status_cross,
          "Comment":comment}
