# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the human data.
data_0 = read_csv("data/actor_0/human/data.csv")

# Update old formatting and remove irrelevant columns.
data_1 = data_0 %>%
  select(-Key, -CompletionDate, -UserID)
names(data_1)[which(names(data_1)=="CostCondition")] = "Condition"
names(data_1)[which(names(data_1)=="DoorChoice")] = "Response"
names(data_1)[which(names(data_1)=="HighCost")] = "Costlier"
data_1$Response[which(data_1$Response=="ClearDoor")] = "unmodified"
data_1$Response[which(data_1$Response=="ModifiedDoor")] = "modified"
data_1$Costlier[which(data_1$Costlier=="BaseDoor")] = "unmodified"
data_1$Costlier[which(data_1$Costlier=="TargetDoor")] = "modified"
data_1$Difficulty[which(data_1$Difficulty=="Yes")] = "yes"
data_1$Difficulty[which(data_1$Difficulty=="No")] = "no"

# Exclude participants who said the unmodified door was more difficult to walk
# through and omit missing data.
data_2 = data_1 %>% 
  filter(Costlier != "unmodified") %>%
  filter(Condition != "") %>%
  na.omit() 

# Compute the (percent) participant endorsement of each door in each condition.
data_3 = data_2 %>% 
  do(left_join(., summarize(group_by(., Condition),
                            Unmodified=sum(Response=="unmodified"), 
                            Modified=sum(Response=="modified"),
                            Total=n()))) %>%
  mutate(Unmodified=Unmodified/Total*100,
         Modified=Modified/Total*100)
  
# Compute 95% bootstrapped CIs.
compute_mean = function(data, indices) {
  return(mean(data[indices]))
}

compute_bootstrap = function(data, condition) {
  bool_data = data %>%
    filter(Condition==condition) %>%
    mutate(Response=ifelse(Response=="unmodified", 1, 0))
    
  simulations = boot(bool_data$Response,
                     statistic=compute_mean,
                     R=10000)

  return(boot.ci(simulations, type="perc")$perc)
}

bootstrap_ci = compute_bootstrap(data_3, "none")
none_lower_ci = bootstrap_ci[4]*100
none_upper_ci = bootstrap_ci[5]*100

bootstrap_ci = compute_bootstrap(data_3, "low")
low_lower_ci = bootstrap_ci[4]*100
low_upper_ci = bootstrap_ci[5]*100

# Plot the data using our labels of difficulty.
plot_0 = data_3 %>%
  gather(Response, Endorsement, Unmodified, Modified) %>%
  group_by(Condition, Endorsement, Response) %>%
  summarize(Total=n()) %>%
  ggplot(aes(x=Condition, y=Endorsement, fill=Response))

plot_0 + 
  geom_histogram(stat="identity") + 
  geom_errorbar(aes(x="none", ymin=none_lower_ci, ymax=none_upper_ci), width=0.3) +
  geom_errorbar(aes(x="low", ymin=low_lower_ci, ymax=low_upper_ci), width=0.3) +
  theme_bw() +
  scale_x_discrete(limits=c("none", "low"), labels=c("None", "Low")) +
  scale_fill_discrete(breaks=c("Unmodified", "Modified")) + 
  ylab("Endorsement (%)")

# Re-do much of this analysis but with the participant labels of difficulty.

# Compute the (percent) participant endorsement of each door in each condition.
data_4 = data_2 %>% 
  do(left_join(., summarize(group_by(., Costlier),
                            Unmodified=sum(Response=="unmodified"), 
                            Modified=sum(Response=="modified"),
                            Total=n()))) %>%
  mutate(Unmodified=Unmodified/Total*100,
         Modified=Modified/Total*100)

# Compute 95% bootstrapped CIs.
compute_bootstrap = function(data, costlier) {
  bool_data = data %>%
    filter(Costlier==costlier) %>%
    mutate(Response=ifelse(Response=="unmodified", 1, 0))
  print(bool_data$Response)
  simulations = boot(bool_data$Response,
                     statistic=compute_mean,
                     R=10000)
  
  return(boot.ci(simulations, type="perc")$perc)
}

bootstrap_ci = compute_bootstrap(data_4, "equal")
none_lower_ci = bootstrap_ci[4]*100
none_upper_ci = bootstrap_ci[5]*100

bootstrap_ci = compute_bootstrap(data_4, "modified")
low_lower_ci = bootstrap_ci[4]*100
low_upper_ci = bootstrap_ci[5]*100

# Plot the data using participant labels of difficulty.
plot_1 = data_4 %>%
  gather(Response, Endorsement, Unmodified, Modified) %>%
  group_by(Costlier, Endorsement, Response) %>%
  summarize(Total=n()) %>%
  ggplot(aes(x=Costlier, y=Endorsement, fill=Response))

plot_1 + 
  geom_histogram(stat="identity") + 
  geom_errorbar(aes(x="equal", ymin=none_lower_ci, ymax=none_upper_ci), width=0.3) +
  geom_errorbar(aes(x="modified", ymin=low_lower_ci, ymax=low_upper_ci), width=0.3) +
  theme_bw() +
  scale_x_discrete(limits=c("equal", "modified"), labels=c("Equal", "Modified")) +
  scale_fill_discrete(breaks=c("Unmodified", "Modified")) +
  ylab("Endorsement (%)")
