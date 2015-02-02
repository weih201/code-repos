## This script is to address task1, which is to: 
## Using the base plotting system, make a plot showing the total PM2.5 emission 
## from all sources for each of the years 1999, 2002, 2005, and 2008.

## From the plot output from the below code, we can see that PM2.5 significantly 
## decreased in the United States from 1999 to 2008

## Seeting working directory
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading data
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Calculating total emissions in United States from 1999 to 2008
totEmissions <- tapply(NEI$Emissions, NEI$year, sum)
totEmissions <- totEmissions/1.0e+6
years<-unique(NEI$year)


png("plot1.png", width = 480, height = 480, units = "px")

## Using base plotting system to plot graph
plot(years,totEmissions, ylab="Total Emissions from PM2.5(mega tons) per year",xlab="Years",
     main = "Emissions of PM25 per year of all sources",
     xaxt="n", yaxt="n", pch=17, type="b",col="red")
axis(1, at=years, labels=years)

for(emission in totEmissions)
  axis(2, at=emission, labels=format(round(emission,1),nsmall=1))

dev.off()


