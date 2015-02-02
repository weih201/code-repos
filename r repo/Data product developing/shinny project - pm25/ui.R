library(shiny)

states<-c("USA","Alabama",  "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
          "Florida","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana",
          "Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
          "Nebraska","Nevada","Ohio","Oklahoma","Oregon","Pennsylvania","Tennessee","Texas",
          "Utah","Vermont","Virginia","Washington")

shinyUI(
  
  navbarPage("PM25 Emission", 

  tabPanel("Plot",
    sidebarLayout(
    
    sidebarPanel(
      
      fluidRow(
        
       column(6,
             radioButtons("year", "Years",
                         c("2005" = "2005",
                           "2008" = "2008",
                           "2005~2008" = "all"))),
      
       column(6,
              radioButtons("type", "Source",
                   c("Point" = "POINT",
                     "Non-Point" = "NONPOINT",
                     "On-Road" = "ON-ROAD",
                     "Non-Road" = "NON-ROAD",
                     "All Types" = "all")))
      ),
      
      selectInput("region","State Name",states)
    ),
    
    mainPanel(
          plotOutput("map")
      )
    )
  ),
  
    tabPanel("About",
      mainPanel(includeMarkdown("about.md")
    )
  )
)
)
