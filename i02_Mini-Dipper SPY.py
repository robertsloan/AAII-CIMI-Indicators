"""
5/30/2019
Robert Sloan

Replicating Al Zmyslowski's AAII CIMI Market Review - Technical & Economic Indicators
Mini-Dipper (SPY)
Using Yahoo Adjusted Close for SPY in calculations.
This measures the 40 day simple moving average (SMA) vs the 170 day SMA on the SPY.
Bullish if 40dSMA of the unadjusted price of the S&P Composite is greater than the 170dSMA

TODO
  Verify how to calculate % and add it to the indicator output LONG (3.13%)
  Add Red and Green bars on graph to show Long and Short regions

"""
# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating Mini-Dipper")
  # this library load is because pandas matplotlib FutureWarning
  from pandas.plotting import register_matplotlib_converters
  register_matplotlib_converters()
  # get SPY data from passed dataframe
  spy_data = dataframe["SPY"]

  # Get the spy_data timeseries. This now returns a Pandas Series object indexed by date.

  # Calculate the 40 day and 170 day simple moving averages of the closing prices of the SPY
  spy_40d_sma = spy_data.rolling(window=40).mean()

  # Calculate the 170 day exponential moving average of the closing prices of the SPY
  spy_170d_ema = spy_data.ewm(span=170, adjust=False).mean()

  # Plot everything by leveraging the very powerful matplotlib package
  fig, ax = plt.subplots(figsize=(16,9))
  title = "Mini-Dipper SPY\n" + record_date
  ax.set_title(title)
  ax.plot(spy_data.index, spy_data, label='SPY')
  ax.plot(spy_40d_sma.index, spy_40d_sma, label='40 day SMA SPY')
  ax.plot(spy_170d_ema.index, spy_170d_ema, label='170 day EMA SPY')
  plt.axvline(x=previous_EOM_date, color='k', linestyle='--') # add vertical dashed line for previous_EOM_date
  plt.axvline(x=last_EOM_date, color='k', linestyle='--')     # add vertical dashed line for last_EOM_date

  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price SPY ($)')
  ax.legend()
  fig.savefig("Figures/Mini-Dipper.png")
  #plt.show()

  # Last day of last month 40 day SMA and 170 day SPY EMA
  endOfLastMonth_spy_40d_sma = float(spy_40d_sma[last_EOM_date].values)
  # print("40 day " + str(endOfLastMonth_spy_40d_sma))
  endOfLastMonth_spy_170d_ema = float(spy_170d_ema[last_EOM_date].values)
  # print("170 day " + str(endOfLastMonth_spy_170d_ema))
  # Determin if 40 day SPY SMA is greater than 170 day SMA and how much
  mini_dipper_spy = endOfLastMonth_spy_40d_sma - endOfLastMonth_spy_170d_ema
  # print("40 day SMA - 170 day EMA " + str(mini_dipper_spy))
  # Dont know how to calculate this percent
  # lastMonth_mini_dipper_spy_percent = round(mini_dipper_spy/endOfLastMonth_spy,1)
  # print(lastMonth_mini_dipper_spy_percent)
  # print("mini_dipper_spy = ", mini_dipper_spy)
  if (mini_dipper_spy>1):
      lastMonth_status_mini_dipper = 'LONG'
  else:
      lastMonth_status_mini_dipper = 'SHORT'
  # print("lastMonth_status_mini_dipper = ", lastMonth_status_mini_dipper)

  # Last day of month before last 40 day SMA and 170 day SPY EMA
  endOfMonthBeforeLast_spy_40d_sma = float(spy_40d_sma[previous_EOM_date].values)
  # print("40 day " + str(endOfMonthBeforeLast_spy_40d_sma))
  endOfMonthBeforeLast_spy_170d_ema = float(spy_170d_ema[previous_EOM_date].values)
  # print("170 day " + str(endOfMonthBeforeLast_spy_170d_ema))
  # Determin if 40 day SPY SMA is greater than 170 day SMA and how much
  mini_dipper_spy = endOfMonthBeforeLast_spy_40d_sma - endOfMonthBeforeLast_spy_170d_ema
  # print("40 day SMA - 170 day EMA " + str(mini_dipper_spy))
  # Dont know how to calculate this percent
  # monthBeforeLast_mini_dipper_spy_percent = round(mini_dipper_spy/endOfMonthBeforeLast_spy,1)
  # print(monthBeforeLast_mini_dipper_spy_percent)
  # print("mini_dipper_spy = ", mini_dipper_spy)

  if (mini_dipper_spy>1):
      monthBeforeLast_status_mini_dipper = 'LONG'
  else:
      monthBeforeLast_status_mini_dipper = 'SHORT'
  # print("monthBeforeLast_status_mini_dipper = ", monthBeforeLast_status_mini_dipper)
  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d'))
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d'))

  comment = "50d SMA/170d EMA"
  indicators = pd.DataFrame([{'Technical Indicator': 'Mini-Dipper SPY',
                              strLast_EOM_date:lastMonth_status_mini_dipper,
                              strPrevious_EOM_date:monthBeforeLast_status_mini_dipper,
                              'Comment': comment}],
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)



  return {
          "Technical Indicator": "Mini-Dipper SPY",
          "Frequency":"Daily",
          "MonthBeforeLast":monthBeforeLast_status_mini_dipper,
          "LastMonth":lastMonth_status_mini_dipper,
          "Comment":comment}
