# Load libraries.
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the human data.
data_0 = read_csv("data/agent_1/agent_1.csv")

# Update old formatting.
data_1 = data_0
names(data_1)[which(names(data_1) == "CostCondition")] = "Condition"
names(data_1)[which(names(data_1) == "DoorChoice")] = "Response"
names(data_1)[which(names(data_1) == "HighCost")] = "Costlier"
levels(data_1$Response)[which(levels(data_1$Response) == "ClearDoor")] = "unmodified"
levels(data_1$Response)[which(levels(data_1$Response) == "ModifiedDoor")] = "modified"
levels(data_1$Costlier)[which(levels(data_1$Costlier) == "BaseDoor")] = "unmodified"
levels(data_1$Costlier)[which(levels(data_1$Costlier) == "TargetDoor")] = "modified"
levels(data_1$Difficulty)[which(levels(data_1$Difficulty) == "Yes")] = "yes"
levels(data_1$Difficulty)[which(levels(data_1$Difficulty) == "No")] = "no"

# Exclude participants who said the unmodified door was more difficult to walk
# through and omit missing data.
data_2 = data_1 %>% 
  filter(Costlier != "unmodified") %>%
  filter(Condition != "") %>%
  na.omit()

# Compute participant endorsement of each door in each condition.
data_3 = data_2 %>% 
  do(left_join(., summarize(group_by(., Condition), Total=n()))) %>%
  do(left_join(., summarize(group_by(., Condition), 
                            Unmodified=sum(Response == "unmodified"), 
                            Modified=sum(Response == "modified")))) %>%
  mutate(Unmodified=Unmodified/Total*100,
         Modified=Modified/Total*100)
  

temp_0 = data_3 %>%
  gather(Response, Endorsement, Unmodified, Modified) %>%
  ggplot(aes(x=Condition, y=Endorsement, fill=Response)) + 
  geom_histogram(stat="identity")

remove()

temp_0 = data_0 %>% 
  group_by(CostCondition) %>%
  summarize(Total=n())
temp_1 = data_0 %>% 
  group_by(CostCondition) %>% 
  summarize(ClearDoor=sum(DoorChoice == "ClearDoor"), 
            ModifiedDoor=sum(DoorChoice == "ModifiedDoor")) %>%
  gather(Choice, Value, ClearDoor, ModifiedDoor) %>%
  left_join(temp_0) %>%
  mutate(Endorsement=Value/Total*100)

# Compute 95% bootstrapped CIs.
get_average = function(data, indices) {
  subset = data[indices]
  average = mean(subset)
  return(average)
}

simulations = boot(data=0, statistic=get_average, R=10000)
boot.ci(simulations, type="perc")

# Plot the data using our labels


geom_errorbar(aes(x="none", ymin=28.77, ymax=50.68), width=0.2)
# Plot the data using participant labels.




# Plot.
data %>%
  ggplot(aes(x=CostCondition, y=Endorsement, fill=Choice)) + 
    geom_histogram(stat="identity")
