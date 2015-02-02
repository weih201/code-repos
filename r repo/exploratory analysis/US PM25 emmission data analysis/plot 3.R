## This script is to address task3, which is to plot the four types of pm25 emission in Baltimore citry
## from 1999 to 2008 with ggplot2 plottingsystem

## From the plot output, we will see that the Point type emission had some increasing, while all the other 
## three types emissions decreased during the period 1999-2008

## Input ggplt2 package, setting work directory
library(ggplot2)
setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 2/exdata_data_NEI_data")

## Reading data
NEI <- readRDS("summarySCC_PM25.rds")
SCC <- readRDS("Source_Classification_Code.rds")

## Subsettting Baltimore data set
Baltimore <- subset(NEI,fips == "24510") 

## Subsetting four types emissions data
point<-subset(Baltimore,type=="POINT")
nonpoint <- subset(Baltimore,type=="NONPOINT")
onRoad <- subset(Baltimore,type=="ON-ROAD")
nonRoad <- subset(Baltimore,type=="NON-ROAD")

## Calculating four types emissions
ptEmi <- tapply(point$Emissions, point$year, sum)
npEmi <- tapply(nonpoint$Emissions, nonpoint$year, sum)
orEmi <- tapply(onRoad$Emissions, onRoad$year, sum)
nrEmi <- tapply(nonRoad$Emissions, nonRoad$year, sum)
years<-unique(NEI$year)

## Creating the ggplot needed dataframe
df<-data.frame(emi=c(ptEmi,orEmi,npEmi,nrEmi),year=factor(rep(years,4)),
          label= factor(rep(c("Point","On-Road","Non-Point","Non-Road"),each=4)))
df$label <- factor(df$label,levels=c("Point","On-Road","Non-Point","Non-Road"))

png("plot3.png", width = 480, height = 480, units = "px")

## PLotting with ggplot function
p<- ggplot(data=df,aes(year,emi,fill=label)) + geom_bar(stat="identity") + 
  xlab("Years") + ylab("PM25 Emissions (Tones)")+
  ggtitle("Total Emissions in Baltimore city, Maryland")+
  theme(plot.title = element_text(size=12,face="bold")) + facet_wrap(~label,ncol=2)

print(p)

dev.off()
