library(mapproj)
library(maps)
library(ggplot2)
library(dplyr)

# Load Data
NEI <- tbl_df(readRDS("./data/SCC_PM25_2005.rds"))

# sum per fips per year per type
dt <- summarize(group_by(NEI,fips,year,type),Emissions=sum(Emissions))

dt$Emissions <- round(dt$Emissions / 1000, digits = 2)
dt$fips <- as.integer(as.character(dt$fips))
dt$year <- as.integer(as.character(dt$year))
dt <- na.omit(dt)

# get fips of county data 
data(county.fips)
county_fips <- tbl_df(county.fips)

# join the country fips data with the emission data
dt<-left_join(dt, county_fips, by="fips")
dt<-na.omit(dt)

# Extracting the state and counyty names
dt$polyname<-as.character(dt$polyname)
dt<-mutate(dt,region= sub(",.*", "", polyname))
dt<-mutate(dt,subregion= sub(".*,", "", polyname)) 
dt<-ungroup(dt)

# join the got emission dat set with the county geographic data set 
# via state and county names
all_county <- tbl_df(map_data('county'))
dt <- left_join(all_county,dt)


## emission fun to precess the data selecting and presentation
## The selecting can base on the years, emission types and states name
emission <- function(years, regions, types) {
  
  if(years=="all"){
    dtplot<-dt
    years<-"2005 ~ 2008"
  }else {
    dtplot<-dt[as.numeric(dt$year)==as.numeric(years),]
  }
  
  if(types=="all"){
    dtplot<-dtplot
    types<- "all types"
  }else {
    dtplot<-dtplot[dtplot$type==types,]    
  } 
  
  if(regions=="USA"){
    dtplot<-dtplot
  }else {
    regions<-tolower(regions)
    dtplot<-dtplot[dtplot$region==regions,] 
    regions<-toupper(regions)
  } 
  
## calculating the emission based on the given selecting options  
  dtplot<-summarize(group_by(dtplot,long,lat,group),Emissions=sum(Emissions))

## color range setting
  colors<-switch(types, 
                "all types"= c("AliceBlue","DarkRed"),
                "POINT" = c("AliceBlue","DarkRed"),
                "NONPOINT"= c("AliceBlue","DarkRed"),
                "ON-ROAD"= c("AliceBlue","DarkRed"),
                "NON-ROAD" = c("AliceBlue","DarkRed")
                )
  
  ggplot() + geom_polygon(data=dtplot, aes(x=long, y=lat, group=group, fill = Emissions), colour=colors[1]) +
    scale_fill_continuous(low = colors[1], high = colors[2], guide="colorbar") + coord_map() +
    labs(fill = "Emissions in Kilo Ton ", title = paste("Emissions of PM25[",tolower(types),"] across ", 
     regions, " in ", years,sep="", collapse='')) + xlab("Longitude") +  ylab("Latitude")
}