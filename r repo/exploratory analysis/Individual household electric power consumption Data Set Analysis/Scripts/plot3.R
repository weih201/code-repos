## This file is to plot graph 3
library(sqldf)

setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 1")

file<-"household_power_consumption.txt"

## Reading needed data
mySql <- "SELECT * from file WHERE Date = '1/2/2007' OR Date = '2/2/2007'"
file<-"household_power_consumption.txt"
dat <- read.csv.sql(file,sql=mySql,sep=";")

## Getting datetime
datetime<-as.list(paste(dat$Date,dat$Time))
dt<-as.POSIXlt(strptime(datetime, "%d/%m/%Y %H:%M:%S"))

## Setting plot size
png("plot3.png",  width = 480, height = 480, units = "px")

## Plotting Sub_metering_1
plot(dt,dat$Sub_metering_1,ylab="Energy sub metering",xlab="",type="l",col="black")

## Plotting Sub_metering_2
lines(dt,dat$Sub_metering_2,type="l",col="red")

## Plotting Sub_metering_3
lines(dt,dat$Sub_metering_3,type="l",col="blue")

## Plotting legend
legend("topright",lty=1,col=c("black","red","blue"),
       legend=c("Sub_metering_1","Sub_metering_2","Sub_metering_3"))
dev.off()

