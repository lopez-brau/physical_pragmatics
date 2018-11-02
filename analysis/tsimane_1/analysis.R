library(tidyverse)

setwd("D:/Research/social_pragmatics")
demographics = read_csv("data/tsimane_1/demographics.csv")
data = read_csv("data/tsimane_1/doors.csv") %>%
  select(-Comments) %>%
  left_join(demographics)

# Print the data.
data %>%
  separate(UniqueId, into=c("Date", "Community", "Participant"), "_") %>%
  filter(Community != "Pachual") %>% 
  group_by(First_Trial, Door, Object) %>% summarize(Total=n()) %>%
  spread(First_Trial, Total)

# Plot the data.
data %>%
  filter(First_Trial != "no_cost") %>%
  separate(UniqueId, into=c("Date", "Community", "Participant"), "_") %>%
  filter(Community != "Pachual") %>% 
  ggplot(aes(x=Response, fill=First_Trial)) + 
    geom_histogram(stat="count", position="dodge") +
    facet_wrap(~Door) + 
    theme_bw()

# Compute bootstrapped 95% CIs.

group_by(CostCondition) %>% 
  summarize(ClearDoor=sum(DoorChoice=="leave"), ModifiedDoor=sum(DoorChoice=="ModifiedDoor")) %>%
  gather(Choice,Value,ClearDoor,ModifiedDoor)