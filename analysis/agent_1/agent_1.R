# Load libraries.
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

data = read.csv("data/agent_1/agent_1.csv")

# Exclude participants who said the unmodified door was more difficult to walk
# through and omit missing data.
data = data %>% filter(HighCost != "BaseDoor") %>% na.omit()


data = data %>% 
  group_by(CostCondition) %>% 
  summarize(ClearDoor=sum(DoorChoice=="ClearDoor"), ModifiedDoor=sum(DoorChoice=="ModifiedDoor")) %>%
  gather(Choice,Value,ClearDoor,ModifiedDoor) %>%