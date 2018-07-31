# NOAA_DataPipeline

Module meant to handle data fromt the ISD/CDO hourly weather database. 
https://www.ncdc.noaa.gov/data-access/quick-links#dsi-3505

The main class formats and cleans data to get relevant data (Temperature & Time) to calculate bee flight conditions for the winter months (Oct-Jan).
With this data, flight days are flagged and subtotaled by year.

There is also a visualization portion used to plot winter flight percentages by year, while accounting for data coverage (completeness of each winter dataset)
Normalized plot has the baseline set around the average of each location dataset.

![alt text]
