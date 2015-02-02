## This file is to plot the graph1

library(sqldf)

setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 1")

file<-"household_power_consumption.txt"

## Reading needed data
mySql <- "SELECT * from file WHERE Date = '1/2/2007' OR Date = '2/2/2007'"
file<-"household_power_consumption.txt"
dat <- read.csv.sql(file,sql=mySql,sep=";")

## Getting data datatime
dat$Date<-as.Date(dat$Date,format="%d/%m/%Y")

attach(dat)
## Setting plot size
png("plot1.png",  width = 480, height = 480, units = "px")

## Plotting Histograph
hist(Global_active_power,freq=TRUE,main="Global Active Power",xlab="Global Active Power (kilowatts)",col="red",axes=FALSE)
## Adding axis tick
axis(side = 1, at = c(0,2,4,6))
axis(side = 2, at = c(0,200,400,600,800,1000,1200))
dev.off()
detach(dat)
