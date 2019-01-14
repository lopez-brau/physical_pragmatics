# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the demographics and the data.
data_0 = read_csv("data/tsimane_1/data_0/data.csv")

# Filter out Pachual.
data_1 = data_0 %>%
  separate(UniqueId, into=c("Date", "Community", "Participant"), "_") %>%
  filter(Community != "Pachual")

# Plot the data.
data_1 %>%
  filter(First_Trial != "no_cost") %>%
  ggplot(aes(x=Response, fill=First_Trial)) + 
    geom_histogram(stat="count", position="dodge") +
    facet_wrap(~Door) + 
    theme_bw()

# Compute bootstrapped 95% CIs.

