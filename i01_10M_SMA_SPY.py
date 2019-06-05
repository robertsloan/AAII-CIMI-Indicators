"""
5/30/2019 
Robert Sloan 

replicating Al Zmyslowski's AAII CIMI 10M SMA SPY Market timer 
SPY/10M Simple Moving Average (SMA) above 1 go long below 1 go short
Using Yahoo Adjusted Close for SPY in calculations.
TO DO

   Can excel spreadsheet be formatted including column width?
   
"""
# load libraries
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# from data in dataframe return Indicator
def Indicator(dataframe, record_date, last_EOM_date, previous_EOM_date):
  print("Calculating 10 month SMA SPY")
  # this library load is because of a pandas matplotlib FutureWarning
  from pandas.plotting import register_matplotlib_converters
  register_matplotlib_converters()
  # get SPY data from passed dataframe
  spy_data = dataframe["SPY"]

  # Calculate the 10 month (210 days) moving averages of the closing prices
  spy_10m_sma = spy_data.rolling(window=210).mean()

  # Plot everything by leveraging the very powerful matplotlib package
  fig, ax = plt.subplots(figsize=(16,9))
  title = "SPY 10 month Simple Moving Average\n" + record_date
  ax.set_title(title)
  ax.plot(spy_data.index, spy_data, label='SPY')
  ax.plot(spy_10m_sma.index, spy_10m_sma, label='10 month simple moving average')
  ax.set_xlabel('Date')
  ax.set_ylabel('Adjusted closing price ($)')
  ax.legend()
  fig.savefig("Figures/10M_SMA_SPY.png") #**********************
  #plt.show()

  # Last day of last month 10M SMA SPY
  endOfLastMonth_spy = float(spy_data[last_EOM_date].values)
  #print("endOfLastMonth_spy = " + str(spy_data[last_EOM_date]))
  endOfLastMonth_spy_10m_sma = float(spy_10m_sma[last_EOM_date].values)
  #print("endOfLastMonth_spy_10m_sma = " + str(spy_10m_sma[last_EOM_date]))
  lastMonths_sma_spy = endOfLastMonth_spy/endOfLastMonth_spy_10m_sma
  lastMonths_percent_sma_spy = round(((endOfLastMonth_spy/endOfLastMonth_spy_10m_sma)-1)*100,2)
  if (lastMonths_sma_spy>1):
      statusLastMonth = 'LONG'
  else:
      statusLastMonth = 'SHORT'
  #print("Last Months Indicator: " + statusLastMonth + " (" + str(lastMonths_percent_sma_spy) + "%)")

  # Last day of last month 10M SMA SPY
  endOfMonthBeforeLasts_spy = float(spy_data[previous_EOM_date].values)
  #print("endOfMonthBeforeLasts_spy = " + str(spy_data[previous_EOM_date]))
  endOfMonthBeforeLasts_spy_10m_sma = float(spy_10m_sma[previous_EOM_date].values)
  #print("endOfMonthBeforeLasts_spy_10m_sma = " + str(spy_10m_sma[previous_EOM_date]))
  MonthBeforeLasts_sma_spy = endOfMonthBeforeLasts_spy/endOfMonthBeforeLasts_spy_10m_sma
  MonthBeforeLasts_percent_sma_spy = round(((endOfMonthBeforeLasts_spy/endOfMonthBeforeLasts_spy_10m_sma)-1)*100,2)
  if (MonthBeforeLasts_sma_spy>1):
      statusMonthBeforeLast = 'LONG'
  else:
      statusMonthBeforeLast = 'SHORT'
  #print("Month before lasts Indicator: " + statusMonthBeforeLast + " (" + str(MonthBeforeLasts_percent_sma_spy) + "%)")
  strLast_EOM_date = str(last_EOM_date.strftime('%Y-%m-%d'))
  strPrevious_EOM_date = str(previous_EOM_date.strftime('%Y-%m-%d'))
  """
  # ### Cant figure out how to get last_EOM_data as simple string. ###########
  print("type(last_EOM_date) = ", type(last_EOM_date))
  print("type(previous_EOM_date) = ", type(previous_EOM_date))
  print("strLast_EOM_date = ", strLast_EOM_date)
  print("strPrevious_EOM_date = ", strPrevious_EOM_date)

  print("pd.to_datetime(last_EOM_date) = ", pd.to_datetime(last_EOM_date))
  print("pd.to_datetime(last_EOM_date).strftime('%Y-%m-%d') = ", pd.to_datetime(last_EOM_date).strftime('%Y-%m-%d'))
  print("str(pd.to_datetime(last_EOM_date).strftime('%Y-%m-%d')) = ", str(pd.to_datetime(last_EOM_date).strftime('%Y-%m-%d')))
  """ 

  mbl=statusMonthBeforeLast + " (" + str(MonthBeforeLasts_percent_sma_spy) + "%)"
  lm=statusLastMonth + " (" + str(lastMonths_percent_sma_spy) + "%)"
  comment=" SPY/10 month SMA; 1.0 is lower limit"
  indicators = pd.DataFrame([{'Technical Indicator': '10 month SMA SPY',
                              strLast_EOM_date:mbl, 
                              strPrevious_EOM_date:lm, 
                              'Comment': comment}], 
                             columns=['Technical Indicator', strLast_EOM_date, strPrevious_EOM_date,
                                      'Comment'])
  #print (indicators)
  

  return {
          "Technical Indicator": "10 month SMA SPY",
          "Frequency":"Monthly",
          "MonthBeforeLast":mbl,
          "LastMonth":lm,
          "Comment":comment} 

