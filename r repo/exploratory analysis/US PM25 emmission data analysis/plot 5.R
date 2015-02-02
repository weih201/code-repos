## This script is to address task5, which is to show PM25 emissions from vehicle 
## in Baltimore City from 1999 to 2008

## From the plot output, we can see that in Baltimore City, emissions from vehicle had the significantly 
## decreased from 1999 to 2008 

## Input needed package, setting work directory
library(ggplot2)
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading data
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subsetting Baltimore Vehicle datasets
Baltimore <- subset(NEI,fips == "24510") 
vehSCC <- SCC[grepl("Veh", SCC$Short.Name) | grepl("Vehicle", SCC$Short.Name)|grepl("veh", SCC$Short.Name)|
                grepl("vehicle", SCC$Short.Name),]
vehNEI <- subset(Baltimore, SCC %in% vehSCC$SCC)

## Calculating total vehicle emissions in Baltimore City
vehEmi <- tapply(vehNEI$Emissions, vehNEI$year, sum)
years<-unique(NEI$year)

## Constructing needed dataframe
df<-data.frame(emi=vehEmi, years=factor(years))

png("plot5.png", width = 480, height = 480, units = "px")

## Plotting with ggplot function
ggplot(data=df,aes(x=years,y=emi,fill=years))+geom_bar(stat="identity")+ xlab("Years")+guides(fill=FALSE)+
  ylab("Tones")+ggtitle("Emissions of PM25 of Vehicles in Baltimore City per year")+
  theme(plot.title = element_text(size=14, face="bold"))

dev.off()
