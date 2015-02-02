## This script is to address task2, which is to plot total emissions from PM2.5 in the 
## Baltimore City, Maryland from 1999 to 2008 with base plotting system 

## From the plot output from the below code, we can see that Baltimore City's PM2.5 emission fluctuated 
## during 1999 to 2008, but the overall treand was gradually decreasing

## Seeting working directory
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading Data
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subset baltimore
Baltimore <- subset(NEI,fips == "24510") 

## Calculating pm25 emission in Baltimore
totEmissions <- tapply(Baltimore$Emissions, Baltimore$year, sum)
totEmissions <- totEmissions/1.0e3
years<-unique(NEI$year)

png("plot2.png", width = 480, height = 480, units = "px")

## PLotting with base plot system
plot(years,totEmissions, ylab="Total Emissions from PM2.5(kilo tons) per year from Baltimore City, Maryland",
     xlab="Years", main="Emissions of PM25 per year from Baltimore City, Maryland",
     xaxt="n", yaxt="n", pch=17, type="b",col="red")
axis(1, at=years, labels=years)
for(emission in totEmissions)
  axis(2, at=emission, labels=format(round(emission,1),nsmall=1))

dev.off()


