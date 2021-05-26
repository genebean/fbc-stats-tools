import os
import pandas

ymdt = '2021-05-09 08:30'
yt_concurrent = 2

ss_live = 0
ss_same_day = 0
ss_on_demand = 0

yt_same_day = 0 - yt_concurrent
yt_on_demand = 0

# standardize file name
path = os.getcwd()
for files in os.listdir(path):
    if os.path.isfile(os.path.join(path, files)):
        if '-unique-viewers' in files:
            os.rename(files, 'streamspot.csv')
            break

streamspot_data = pandas.read_csv('streamspot.csv', parse_dates=['start', 'end'])
live_date = pandas.to_datetime(ymdt).date()
for index, row in streamspot_data.iterrows():
    watch_date = row['start'].date()
    if watch_date == live_date:
        if row['viewerType'] == 'live':
            ss_live += 1
        else:
            ss_same_day += 1
    else:
        ss_on_demand += 1

youtube_data = pandas.read_csv('Totals.csv', parse_dates=['Date'])
for index, row in youtube_data.iterrows():
    watch_date = row['Date'].date()
    if watch_date == live_date:
        yt_same_day += row['Unique viewers']
    else:
        yt_on_demand += row['Unique viewers']

if yt_same_day < 0:
    yt_same_day = 0

generated_data = {
  '*': ['StreamSpot', 'YouTube', 'Formulas'],
  'Totals': [
      ss_live + ss_same_day + ss_on_demand,
      yt_concurrent + yt_same_day + yt_on_demand,
      ss_live + ss_same_day + ss_on_demand + yt_concurrent + yt_same_day + yt_on_demand
  ],
  'Live Stream': [
      ss_live,
      yt_concurrent,
      "=sum(%d+%d)" % (ss_live, yt_concurrent)],
  'Later Same Day': [
      ss_same_day,
      yt_same_day,
      "=sum(%d+%d)" % (ss_same_day, yt_same_day)],
  'On-Demand Views': [
      ss_on_demand,
      yt_on_demand,
      "=sum(%d+%d)" % (ss_on_demand, yt_on_demand)]
}
output = pandas.DataFrame(data=generated_data)

print()
print("Stream date: %s" % ymdt)
print()
print(output)
