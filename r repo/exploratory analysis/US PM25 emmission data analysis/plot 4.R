## This script is to address task4, which is to show PM25 emissions from coal combustion-related sources 
## changing from 1999-2008 across United States

## From the plot output, we can see that the coal combustion-related emission decreased in the United Stars,
## but the decreasing was relative slow, especailly before 2005.

## Input needed package, setting work directory
library(ggplot2)
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading Data
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Getting Coal comb realted data-set
coalSCC <- SCC[grepl("Coal", SCC$SCC.Level.Three) | grepl("Lignite", SCC$SCC.Level.Three),]
coalNEI <- subset(NEI, SCC %in% coalSCC$SCC)

## Calcaulating emissions
coalEmissions <- tapply(coalNEI$Emissions, coalNEI$year, sum)
coalEmissions <- coalEmissions/1.0e+3
years<-unique(NEI$year)

## Constructing needed dataframe
df<-data.frame(emi=coalEmissions, years=factor(years))

png("plot4.png", width = 480, height = 480, units = "px")

## Plotting with ggplot function
ggplot(data=df,aes(x=years,y=emi,fill=years))+geom_bar(stat="identity")+ xlab("Years")+guides(fill=FALSE)+
  ylab("(Kilo) Tones")+ggtitle("Emissions of PM25 of coal combustion per year")+
  theme(plot.title = element_text(size=14, face="bold"))

dev.off()
