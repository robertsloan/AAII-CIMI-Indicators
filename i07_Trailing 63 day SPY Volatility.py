"""
6/6/2019
Robert Sloan

replicating Al Zmyslowski's AAII CIMI 10M SMA SPY Market timer

SPY trailing 63 day volatility (Standard Deviation)if less than 1% go Long if >1% go partialy to cash (BIL T-Bills)
Using Yahoo Adjusted Close for SPY in calculations.
Variations include use of SPLV, SDS for high and low vol markets; use of IEF, TLT, etc. instead of cash for volatility reduction instrument
Can implement in 5 or 10% increments to cut down on trading frequency
TO DO

Need to define % in Cash if Standard Deviation (SD) is >1%

"""
# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  # this library load is because of a pandas matplotlib FutureWarning
  from pandas.plotting import register_matplotlib_converters
  register_matplotlib_converters()

  indicatorType = "Trailing 63 day SPY Volatility"
  print("Calculating", indicatorType)

  # Get the spy_data timeseries. This now returns a Pandas Series object indexed by date.
  spy_data = dataframe["SPY"]
  # print("spy_data.head() = ", spy_data.head())
  # Calculate the 63 day moving averages of the adjusted closing prices
  spy_63d_sma = spy_data.rolling(window=63).mean()
  # Calculate the 63 day moving averages of the adjusted closing prices
  spy_63d_std = spy_data.rolling(window=63).std()

  # If record_date not in spy_63d_std, set it to last valid date
  if record_date not in spy_63d_std:
      record_date2 = str(spy_63d_std.index[len(spy_63d_std) - 1].strftime('%Y-%m-%d'))
      print("WARNING: record_date "+record_date+" not found, using "+record_date2)
      record_date = record_date2

  # Plot everything by leveraging the very powerful matplotlib package
  fig, ax = plt.subplots(figsize=(16,9))
  fig, ax = plt.subplots(figsize=(16,9))
  title = indicatorType + "\n" + record_date
  ax.set_title(title)
  ax.plot(spy_data.index, spy_data, label='SPY')
  ax.plot(spy_63d_sma.index, spy_63d_sma, label='63 day simple moving average')
  ax.plot(spy_63d_std.index, spy_63d_std, label='63 day volatility (standard deviation)')

  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price ($)')
  ax.legend()
  fig.savefig("Figures/" + indicatorType + ".png")
  #plt.show()

  # current 63 day volatility (Standard Deviation) SPY
  current_63d_std_spy = float(spy_63d_std[record_date])
  if (current_63d_std_spy>1):
      status = 'LONG'
  else:
      status = 'SHORT'
  print("Current Indicator: " + status + " (" + str(current_63d_std_spy) + "%)")

  # Last day of last month 63 day volatility (standard deviation) SPY
  endOfLastMonth_63d_std_spy = round(float(spy_63d_std[last_EOM_date].values), 2)
  if (endOfLastMonth_63d_std_spy>1):
      statusLastMonth = 'LONG'
  else:
      statusLastMonth = 'SHORT'
  print("Last Months Indicator: " + statusLastMonth + " (" + str(endOfLastMonth_63d_std_spy) + "%)")

  # Last day of last month 63 day volatility (standard deviation) SPY
  endOfMonthBeforeLasts_63d_std_spy = round(float(spy_63d_std[previous_EOM_date].values), 2)
  if (endOfMonthBeforeLasts_63d_std_spy>1):
      statusMonthBeforeLast = 'LONG'
  else:
      statusMonthBeforeLast = 'SHORT'
  print("Month before lasts Indicator: " + statusMonthBeforeLast + " (" + str(endOfMonthBeforeLasts_63d_std_spy) + "%)")

  # indicator frame
  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d')[0])
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d')[0])

  comment = "1% upper limit/leverage factor"
  lastMonth_status_str = statusLastMonth + " (" + str(endOfLastMonth_63d_std_spy) + "%)"
  monthBeforeLast_status_str = statusMonthBeforeLast + " (" + str(endOfMonthBeforeLasts_63d_std_spy) + "%)"
  indicators = pd.DataFrame([{'Technical Indicator': indicatorType,
                              strLast_EOM_date : lastMonth_status_str,
                              strPrevious_EOM_date : monthBeforeLast_status_str,
                              'Comment': comment}],
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  print (indicators)



  return {
          "Technical Indicator": indicatorType,
          "Frequency":"Daily",
          "MonthBeforeLast":monthBeforeLast_status_str,
          "LastMonth":lastMonth_status_str,
          "Comment":comment}
