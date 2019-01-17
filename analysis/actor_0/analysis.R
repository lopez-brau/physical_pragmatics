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
         costlier=HighCost, possible=Difficulty, response=DoorChoice) %>%
  select(UserID, condition, object, side, costlier, possible, response)
data_1$side[which(data_1$side=="0")] = "right"
data_1$side[which(data_1$side=="1")] = "left"
data_1$costlier[which(data_1$costlier=="BaseDoor")] = "unmodified"
data_1$costlier[which(data_1$costlier=="TargetDoor")] = "modified"
data_1$possible[which(data_1$possible=="Yes")] = "yes"
data_1$possible[which(data_1$possible=="No")] = "no"
data_1$response[which(data_1$response=="ClearDoor")] = "unmodified"
data_1$response[which(data_1$response=="ModifiedDoor")] = "modified"

# Exclude participants who said the unmodified door was more difficult to walk
# through and omit missing data.
data_2 = data_1 %>% 
  filter(condition!="") %>%
  na.omit() %>%
  filter(costlier!="unmodified")

# Add pseudo-workerids to make it easier to distinguish participants across
# disjoint datasets.
data_3 = data.frame(pworkerid=c(0:(nrow(data_2)-1)), data_2) %>%
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
data_9 = data.frame()
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
        na.omit() %>%
        mutate(trial=gsub("num", "", paste(trial_type, num, sep=""))) %>%
        select(-trial_type, -num) %>%
        arrange(workerid)
      
      # Make a column of pseudo-workerids for joining the results.
      data_7 = data_6 %>%
        mutate(pworkerid=as.integer(workerid+id)) %>%
        select(-workerid)
      id = id + length(unique(data_6$workerid))
      
      # Import the setup information to know which side the low-cost door was
      # on.
      setup_0 = read_delim(paste(folder, "/", e, ".results", sep=""), 
                           delim="\t")$Answer.setup
      
      # Remove the quotes, backslashes, and braces.
      setup_1 = gsub("\\", "", setup_0, fixed=T)
      setup_2 = gsub("\"", "", setup_1, fixed=T)
      setup_3 = gsub("{", "", setup_2, fixed=T)
      setup_4 = gsub("}", "", setup_3, fixed=T)
      
      # Extract the side information.
      setup_5 = setup_4 %>%
        strsplit(",", fixed=T) %>%
        unlist()
      side = setup_5[which(grepl("side:", setup_5))] %>%
        lapply(substr, 6, nchar(.)) %>%
        unlist()
      
      # Reformat the data to make it the same as the first experiment.
      data_8 = data_7 %>% 
        spread(trial, target) %>%
        mutate(condition=unlist(strsplit(e, "_"))[1], object=unlist(strsplit(e, "_"))[2], 
               side=side, costlier=exclusion_1, possible=exclusion_2, response=trial_1) %>%
        select(-trial_1, -exclusion_1, -exclusion_2)
      
      # Finally, stitch everything together.
      data_9 = rbind(data_9, data_8)
    }
  }
}
data_9$costlier[which(data_9$costlier==0)] = "unmodified"
data_9$costlier[which(data_9$costlier==1)] = "modified"
data_9$costlier[which(data_9$costlier==2)] = "equal"
data_9$possible[which(data_9$possible==0)] = "yes"
data_9$possible[which(data_9$possible==1)] = "no"
data_9$response[which(data_9$response==0)] = "modified"
data_9$response[which(data_9$response==1)] = "unmodified"

# Exclude participants who said the unmodified door was more difficult to walk
# through.
data_10 = data_9 %>% 
  filter(costlier!="unmodified")

# Finally, combine the two datasets.
data_11 = rbind(data_3, data_10)

# Compute the (percent) participant endorsement of each door in each condition.
data_12 = data_11 %>% 
  do(left_join(., summarize(group_by(., condition),
                            unmodified=sum(response=="unmodified"), 
                            modified=sum(response=="modified"),
                            total=n()))) %>%
  mutate(unmodified=unmodified/total*100,
         modified=modified/total*100)
  
# Compute 95% bootstrapped CIs.
compute_mean = function(data, indices) {
  return(mean(data[indices]))
}

compute_bootstrap = function(data, cond) {
  bool_data = data %>%
    filter(condition==cond) %>%
    mutate(response=ifelse(response=="unmodified", 1, 0))
    
  simulations = boot(bool_data$response,
                     statistic=compute_mean,
                     R=10000)

  return(boot.ci(simulations, type="perc")$perc)
}

bootstrap_ci = compute_bootstrap(data_12, "none")
none_lower_ci = bootstrap_ci[4]*100
none_upper_ci = bootstrap_ci[5]*100

bootstrap_ci = compute_bootstrap(data_12, "low")
low_lower_ci = bootstrap_ci[4]*100
low_upper_ci = bootstrap_ci[5]*100

# Plot 0: Plot the data using our labels of difficulty.
data_13 = data_12 %>%
  gather(response, endorsement, unmodified, modified) %>%
  group_by(condition, endorsement, response) %>%
  summarize(Total=n())

data_13 %>%
  ggplot(aes(x=condition, y=endorsement, fill=response)) +
    geom_histogram(stat="identity") + 
    geom_errorbar(aes(x="none", ymin=none_lower_ci, ymax=none_upper_ci), width=0.3) +
    geom_errorbar(aes(x="low", ymin=low_lower_ci, ymax=low_upper_ci), width=0.3) +
    theme_bw() +
    scale_x_discrete(limits=c("none", "low"), 
                     labels=c("No-Cost", "Low-Cost")) +
    scale_fill_discrete(name="Response",
                        limits=c("modified", "unmodified"), 
                        labels=c("Modified", "Unmodified")) + 
    ylab("Endorsement (%)") +
    xlab("Condition")

# Re-do much of this analysis but with the participant labels of difficulty.

# Compute the (percent) participant endorsement of each door in each condition.
data_14 = data_11 %>% 
  do(left_join(., summarize(group_by(., costlier),
                            unmodified=sum(response=="unmodified"), 
                            modified=sum(response=="modified"),
                            total=n()))) %>%
  mutate(unmodified=unmodified/total*100,
         modified=modified/total*100)

# Compute 95% bootstrapped CIs.
compute_bootstrap = function(data, cost) {
  bool_data = data %>%
    filter(costlier==cost) %>%
    mutate(response=ifelse(response=="unmodified", 1, 0))
  
  simulations = boot(bool_data$response,
                     statistic=compute_mean,
                     R=10000)
  
  return(boot.ci(simulations, type="perc")$perc)
}

bootstrap_ci = compute_bootstrap(data_14, "equal")
none_lower_ci = bootstrap_ci[4] * 100
none_upper_ci = bootstrap_ci[5] * 100

bootstrap_ci = compute_bootstrap(data_14, "modified")
low_lower_ci = bootstrap_ci[4] * 100
low_upper_ci = bootstrap_ci[5] * 100

# Plot 1: Plot the data using participant labels of difficulty.
data_15 = data_14 %>%
  gather(response, endorsement, unmodified, modified) %>%
  group_by(costlier, endorsement, response) %>%
  summarize(total=n())

data_15 %>%
  ggplot(aes(x=costlier, y=endorsement, fill=response)) +
    geom_histogram(stat="identity") + 
    geom_errorbar(aes(x="equal", ymin=none_lower_ci, ymax=none_upper_ci), width=0.3) +
    geom_errorbar(aes(x="modified", ymin=low_lower_ci, ymax=low_upper_ci), width=0.3) +
    theme_bw() +
    scale_x_discrete(limits=c("equal", "modified"), 
                     labels=c("No-Cost", "Low-Cost")) +
    scale_fill_discrete(name="Response",
                        limits=c("modified", "unmodified"),
                        labels=c("Modified", "Unmodified")) +
    ylab("Endorsement (%)") +
    xlab("Participant-Judged Condition")
