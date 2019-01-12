# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the human data from the first experiment.
data_0 = read_csv("data/actor_0/data_0/data.csv")

# Update old formatting and remove irrelevant columns.
data_1 = data_0 %>%
  mutate(condition=CostCondition, object=Object, side=Counterbalancing,
         costlier=HighCost, response=DoorChoice, possible=Difficulty) %>%
  select(UserID, condition, object, side, costlier, response, possible)
data_1$response[which(data_1$response=="ClearDoor")] = "unmodified"
data_1$response[which(data_1$response=="ModifiedDoor")] = "modified"
data_1$costlier[which(data_1$costlier=="BaseDoor")] = "unmodified"
data_1$costlier[which(data_1$costlier=="TargetDoor")] = "modified"
data_1$possible[which(data_1$possible=="Yes")] = "yes"
data_1$possible[which(data_1$possible=="No")] = "no"

# Exclude participants who said the unmodified door was more difficult to walk
# through and omit missing data.
data_2 = data_1 %>% 
  filter(costlier!="unmodified") %>%
  filter(condition!="") %>%
  na.omit() 

# Add pseudo-workerids to make it easier to distinguish participants across
# disjoint datasets.
data_3 = data.frame(pworkerids=c(0:(nrow(data_2)-1)), data_2) %>%
  select(-UserID)

# Import the human data from a second set of experiments (to round out the 
# pre-reg sample size). First, set up the conditions and the different objects 
# participants can see.
conditions = c("none", "low")
objects = c("chair", "plant", "books", "cinderblocks", "tape", "rulers", "hat", "string")

# Populate the list of experimental manipulations.
experiment_list = c()
for (c in conditions) {
  for (o in objects) {
    experiment_list = c(experiment_list, paste(c, "_", o, sep=""))
  }
}

# Import the data.
# results_5 = data.frame()
id = nrow(data_3)
for (folder in list.dirs("./data/actor_0/data_1/")) {
  for (e in experiment_list) {
    if (grepl(e, folder)) {
      # Read in the results for this worker.
      data_4 = read_csv(paste(folder, "/", e, "-trials.csv", sep=""))
      
      # Convert the target column into integers.
      data_5 = data_4 %>%
        mutate(target=as.integer(substr(target, 2, 2)))
      
      # Combine the trial and exclusion columns.
      data_6 = data_5 %>%
        gather(trial_type, num, trial_num, exclusion_num) %>%
        mutate(trial=gsub("num", "", paste(trial_type, num, sep=""))) %>%
        select(-trial_type, -num) %>%
        na.omit() %>%
        arrange(workerid)
      
      # Make a column of pseudo-workerids for joining the results and the setup
      # information.
      data_7 = data_6 %>%
        mutate(pworkerid=as.integer(workerid+id)) %>%
        select(-workerid)
      id = id + length(unique(data_6$workerid))
      
      #
      # data_8 = 
      
      # Finally, stitch everything together.
      # results_5 = rbind(results_5, results_4)
    }
  }
}

data_x = read_csv("data/actor_0/data_0/")



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
