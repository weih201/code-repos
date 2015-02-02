library(sqldf)

## This file is to plot plot4

setwd("C:/my home/coursera/Data Science Specialization/Explortary Data Analysis/Assignments/Assignment 1")

file<-"household_power_consumption.txt"

## Reading needed dat
mySql <- "SELECT * from file WHERE Date = '1/2/2007' OR Date = '2/2/2007'"
file<-"household_power_consumption.txt"
dat <- read.csv.sql(file,sql=mySql,sep=";")

## Getting Data datetime
datetime<-as.list(paste(dat$Date,dat$Time))
dt<-as.POSIXlt(strptime(datetime, "%d/%m/%Y %H:%M:%S"))

## Setting plot size and arrangement
png("plot4.png",  width = 480, height = 480, units = "px")
par(mfrow=c(2,2),lwd=0)

## plotting
plot(dt,dat$Global_active_power,ylab="Global Active Power (kilowatts)",type="l",xlab="")
plot(dt,dat$Voltage,ylab="Voltage",type="l",xlab="datetime")
plot(dt,dat$Sub_metering_1,ylab="Energy sub metering",xlab="",type="l",col="black")
lines(dt,dat$Sub_metering_2,type="l",col="red")
lines(dt,dat$Sub_metering_3,type="l",col="blue")
legend("topright",lty=1,col=c("black","red","blue"), bty="n",
       legend=c("Sub_metering_1","Sub_metering_2","Sub_metering_3"))
plot(dt, dat$Global_reactive_power, ylab="Global_reactive_power", xlab="datetime", type="s")
dev.off()

