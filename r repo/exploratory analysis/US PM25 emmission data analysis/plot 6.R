## This script is to address task6, which is to compare emissions from motor vehicle sources in Baltimore City 
## with emissions from motor vehicle sources in Los Angeles County, California from 1999 to 2008

## From the plot output, we can see that in Baltimore City, emissions from vehicle had the significantly 
## decreased from 1999 to 2008. But in LAC, PM25 emissions from vehicle had some increasing suring this period

## Input needed package, setting work directory
library(ggplot2)
library(gridExtra)
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading dataSet
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Getting needed SCC code
vehSCC <- SCC[grepl("Veh", SCC$Short.Name) | grepl("Vehicle", SCC$Short.Name)|grepl("veh", SCC$Short.Name)|
                grepl("vehicle", SCC$Short.Name),]

## Subsetting Baltimore and LAC datasets
Baltimore <- subset(NEI,fips == "24510") 
LAC <- subset(NEI,fips == "06037") 

BalVehNEI <- subset(Baltimore, SCC %in% vehSCC$SCC)
LACVehNEI <- subset(LAC, SCC %in% vehSCC$SCC)

## Calculating Baltimore and LAC emissions
BalVehEmi <- tapply(BalVehNEI$Emissions, BalVehNEI$year, sum)
LACVehEmi <- tapply(LACVehNEI$Emissions, LACVehNEI$year, sum)

years<-unique(NEI$year)

## Preparing needed dataframe
df<-data.frame(Balemi=BalVehEmi, LAemi=LACVehEmi,years=factor(years))

png("plot6.png", width = 480, height = 480, units = "px")

## Plotting with ggplot function
p1<-ggplot(data=df,aes(x=years,y=Balemi,fill=years))+geom_bar(stat="identity")+ xlab("Years")+guides(fill=FALSE)+
  ylab("Tones")+ggtitle("Emissions of PM25 of Vehicles in Baltimore City per year")+
  theme(plot.title = element_text(size=11, face="bold"))

p2<-ggplot(data=df,aes(x=years,y=LACVehEmi,fill=years))+geom_bar(stat="identity")+ xlab("Years")+guides(fill=FALSE)+
  ylab("Tones")+ggtitle("Emissions of PM25 of Vehicles in Los Angeles County per year")+
  theme(plot.title = element_text(size=11, face="bold"))

## Output graph
grid.arrange(p1,p2, ncol=1)
dev.off()
print(p2)
