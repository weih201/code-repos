## This file is to plot graph2

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

## Plotting
png("plot2.png",  width = 480, height = 480, units = "px")
plot(dt,dat$Global_active_power,ylab="Global Active Power (kilowatts)",type="l",xlab="")
dev.off()


