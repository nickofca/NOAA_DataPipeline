"""
Module meant to handle data fromt the ISD/CDO hourly weather database. 
https://www.ncdc.noaa.gov/data-access/quick-links#dsi-3505

The main class formats and cleans data to get relevant data (Temperature & Time) to calculate bee flight conditions for the winter months (Oct-Jan).
With this data, flight days are flagged and subtotaled by year.

There is also a visualization portion used to plot winter flight percentages by year, while accounting for data coverage (completeness of each winter dataset)
Normalized plot has the baseline set around the average of each location dataset.
"""

import pandas
import matplotlib.pyplot as plt
import os
import seaborn as sns
import LoadingBar
import numpy
from matplotlib.ticker import MultipleLocator

class WeatherFile(object):
    def __init__(self,filepath,extensive=True,save=True,minCover = 0.990, flightTemp = 50):
        #Checks for Output folder
        if not os.path.isdir("Output"):
            raise Exception('No output folder found. Be sure folder labeled "Output" is within the directory')
        file = os.path.basename(filepath)
        self.filename = os.path.splitext(file)[0]
        #Read the file with fixed width
        data = pandas.read_fwf(filepath,header = 0, na_values=["****","***","-"],colspecs=[(13,17),(17,19),(19,21),(21,23),(83,87)])
        #Check if months are within winter and weather is 50F or over. Returns Boolean results.
        data["Flight"] = ((data["MO"]>=10) | (data["MO"]==1)) & (data["TEMP"]>=flightTemp)
        #Checks if months are within winter. Returns Boolean results.
        data["WinterDay"] = ((data["MO"]>=10) | (data["MO"]==1)) & (~data["TEMP"].isnull())
        #Find the difference between each Hour row and the previous row
        #Remove ones with 0 difference 
        data = data.drop(data[data["HR"].diff()==0].index)
        #Collect a list of years so they're listed only once
        years = data["YR--"].unique()
        #Initialize DataFrame with years as index and flight sums as columns
        yData = pandas.DataFrame(index = years, columns = ["Winter Flight Hours","Winter Hours Observed", "Winter Flight Weather Percentage", "Data Coverage (%)"])
        #Sum flight days for that year and write into Dataframe
        for year in years:
            yearFrame = data[data["YR--"]==year]
            yData.loc[year,"Winter Flight Hours"] = yearFrame["Flight"].sum()
            yData.loc[year,"Winter Hours Observed"] = yearFrame["WinterDay"].sum()
        #Calculate percent flight hours over total reported winter hours
        yData["Winter Flight Weather Percentage"] = yData["Winter Flight Hours"]/yData["Winter Hours Observed"]
        #Reported winter hours divided by maximum hours in winter period
        yData["Data Coverage (%)"] = yData["Winter Hours Observed"]/2952
        #Gives the Percentage relative to the average
        #Useful for Normalized Bar Graph
        yData["Normalized Winter Flight Weather Percentage"] = yData["Winter Flight Weather Percentage"]-numpy.mean(yData["Winter Flight Weather Percentage"])
        #Find the years that are not included in the initial dataset and creates a row with all NaN
        addedYears = [x for x in range(years.min(),years.max(),1) if x not in years]
        for year in addedYears:
            yData.loc[year] = numpy.NaN
        #Orders the years
        yData = yData.sort_index()
        #Store attributes for later use
        self.years = years
        self.minCover = minCover
        self.extensive = extensive
        self.save = save
        self.data = data
        self.yData = yData.copy()
        #Filters out data below threshold coverage levels
        yData.loc[yData["Data Coverage (%)"]<=minCover,"Winter Flight Hours":"Normalized Winter Flight Weather Percentage"] = numpy.NaN
        self.yDataFilt = yData
        
    def export(self):
        #Exports DataFrames into CSV's. Extensive includes data without subtotaling
        self.yData.to_csv("Output/"+self.filename+"WrangledByYear.csv",index=True)
        if self.extensive:
            self.data.to_csv("Output/"+self.filename+"WrangledExtensive.csv",index=True)
        
    def scatterPlot(self):
        #Initialize plot
        fig,ax = plt.subplots()
        #Scatter plot with coloring based on coverage. Color bar range coerced to [0,1]
        sc = ax.scatter(x=self.yData.index.values,y=self.yData["Winter Flight Weather Percentage"],c=self.yData["Data Coverage (%)"], edgecolors = "grey", cmap = plt.get_cmap('Greys'),vmin= 0, vmax= 1)
        cb = fig.colorbar(sc)
        ax.set_xlabel("Year")
        ax.set_ylabel("Winter Flight Weather Percentage")
        cb.ax.set_ylabel("Data Coverage (%)", rotation = 270, labelpad=10)
        plt.title("ScatterPlot for "+self.filename)
        self.fig = fig
        #Saved if specified
        if self.save:
            fig.savefig("Output/"+self.filename+"Scatter.jpg",dpi = 300)

    def barPlotNorm(self):
        fig,ax = plt.subplots()
        #Barplot with static color
        sns.barplot(x=self.yDataFilt.index.values,y=self.yDataFilt["Normalized Winter Flight Weather Percentage"], bottom = numpy.mean(self.yDataFilt["Winter Flight Weather Percentage"]),color = "black")
        ax.set_xlabel("Year")
        #Set major ticks to every 5 and minor ticks to every 1
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        #Coerced labels and locations for xTicks. Without coercion, x axis only increments every major tick
        plt.xticks(range(0,max(self.years)-min(self.years)+5,5),range(min(self.years),max(self.years)+5,5))
        fig.autofmt_xdate()
        ax.set_ylabel("Winter Flight Weather Percentage")
        #Save metadata as title of plot
        plt.title("NormalizedBarPlot for "+self.filename+f" (Coverage Min:{format(self.minCover,'.3f')})")
        #Conditional save to an output directory. Must be created
        self.fig = fig
        if self.save:
            fig.savefig("Output/"+self.filename+"BarNormalized.jpg",dpi = 300)
            
    def barPlot(self):
        #Refer to BarPlotNorm  for annotation
        fig,ax = plt.subplots()
        sns.barplot(x=self.yDataFilt.index.values,y=self.yDataFilt["Winter Flight Weather Percentage"], color = "black")
        ax.set_xlabel("Year")
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.xaxis.set_minor_locator(MultipleLocator(1))
        plt.xticks(range(0,max(self.years)-min(self.years)+5,5),range(min(self.years),max(self.years)+5,5))  
        fig.autofmt_xdate()
        ax.set_ylabel("Winter Flight Weather Percentage")
        plt.title("BarPlot for "+self.filename+f" (Coverage Min:{format(self.minCover,'.3f')})")
        self.fig = fig
        if self.save:
            fig.savefig("Output/"+self.filename+"Bar.jpg",dpi = 300)
    
def main():
    #initialize LoadingBar class. See nickofca repository to download. Optional. Delete LB lines to proceed without
    i = 0
    LB = LoadingBar.LoadBar("...initializing...")
    LB.loading()
    #Runs through all files in an input directory. In the event of error, loading thread still closes
    try:
        for i, file in enumerate(os.listdir("Input")):
            LB.m = f"file {i+1} of {len(os.listdir('Input'))}       "
            WF = WeatherFile("Input/"+file)
            WF.export()
            WF.barPlot()
            WF.barPlotNorm()
            WF.scatterPlot()
    finally:
        LB.done()
 
if __name__ == "__main__":
     main()
 
