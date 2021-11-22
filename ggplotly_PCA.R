library(plotly)
library(tidyverse)
library(htmlwidgets)
library(ggplot2)

library(data.table)

setwd("~/showing_interactive")
htmlwidgets::saveWidget(as_widget(p), "namn.html") <- fread("pcs.txt", header = T)

## Simple ggplot PCA
ggplot(data=data,aes(x=PC1,y=PC2 ,group = FID))+
  geom_point( aes(colour  = FID)     )

## Save to a ggplot object
p <- ggplot(data=data,aes(x=PC1,y=PC2 ,group = FID))+
  geom_point( aes(colour  = FID)     )

## Show
ggplotly(p)

## Save as ggplotly object
l <- ggplotly(p)

## Save to html file
htmlwidgets::saveWidget(as_widget(l), "my_output_name.html")
