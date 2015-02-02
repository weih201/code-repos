# server.R
library(mapproj)
library(maps)
library(ggplot2)
library(dplyr)

source("EmissionPM25.R")

shinyServer(
  function(input, output) 
    {
        output$map <- renderPlot(
          {
            years<-input$year
            types<-input$type
            regions<-input$region
            emission(years, regions, types)
        })
    }
)
