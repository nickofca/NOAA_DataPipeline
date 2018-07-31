
# NOAA Data Pipeline
### _by Nick Ziolkowski under the direction of Dr. Gloria Degrandi-Hoffman_

Module meant to handle data from the ISD/CDO hourly weather database. 
https://www.ncdc.noaa.gov/data-access/quick-links#dsi-3505

The main class formats and cleans data to get relevant data (Temperature & Time) to calculate bee flight conditions for the winter months (Oct-Jan).
With this data, flight days are flagged and subtotaled by year.

There is also a visualization portion used to plot winter flight percentages by year, while accounting for data coverage (completeness of each winter dataset)
Normalized plot has the baseline set around the average of each location dataset.

# Examples

## Files
KentuckyHrly.zip - Compressed version of NOAA output data file

KentuckyHrlyWrangledByYear.csv - Subtotaled yearly data

KentuckyHrlyWrangledExtensive.cvw - Wrangled data hourly

## Scatter Plot
![Scatter Plot](https://github.com/nickofca/NOAA_DataPipeline/blob/master/KentuckyHrlyScatter.jpg)
KentuckyHrlyScatter.jpg

## Normalized Bar Plot
![Normalized Bar Plot](https://github.com/nickofca/NOAA_DataPipeline/blob/master/KentuckyHrlyBarNormalized.jpg)
KentuckyHrlyBarNormalized.jpg

## Bar Plot
![Bar Plot](https://github.com/nickofca/NOAA_DataPipeline/blob/master/KentuckyHrlyBar.jpg)
KentuckyHrlyBar.jpg
