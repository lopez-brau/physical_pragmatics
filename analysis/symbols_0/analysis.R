# Load libraries.
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics/")

# Set up the conditions and the different objects participants can see.
conditions = c("object", "symbol")
objects = c("chair", "plant", "books", "cinderblocks", "tape", "rulers", "hat", "string")

# Populate the list of experimental manipulations.
experiment_list = c()
for (c in conditions) {
  for (o in objects) {
    experiment_list = c(experiment_list, paste(c, "_", o, sep=""))
  }
}

# Import the results.
setup = c()
results_0 = data.frame()
results_5 = data.frame()
id = 0
for (folder in list.dirs("./data/symbols_0/symbols_0/")) {
  for (e in experiment_list) {
    if (grepl(e, folder)) {
      # Read in the results for this worker.
      results_0 = read_csv(paste(folder, "/", e, "-trials.csv", sep=""))
      
      # Convert the target column into integers.
      results_1 = results_0 %>%
        mutate(target=as.integer(substr(target, 2, 2)))
      
      # Combine the trial and exclusion columns.
      results_2 = results_1 %>%
        gather(trial_type, num, trial_num, exclusion_num) %>%
        na.omit() %>%
        arrange(workerid)
      
      # Make a column of pseudo-workerids for joining the results and the setup
      # information.
      results_3 = results_2 %>%
        mutate(pworkerid=as.integer(workerid+id))
      pworkerid = as.integer(unique(results_2$workerid)+id)
      id = id + length(unique(results_2$workerid))
      
      # Import the setup information.
      setup_0 = read_csv(paste(folder, "/", e, "-mturk.csv", sep=""))$Answer.setup

      # Remove the quotes, backslashes, and braces.
      setup_1 = gsub("\\", "", setup_0, fixed=T)
      setup_2 = gsub("\"", "", setup_1, fixed=T)
      setup_3 = gsub("{", "", setup_2, fixed=T)
      setup_4 = gsub("}", "", setup_3, fixed=T)
      
      # Do some string processing to transform the json into something usable.
      setup_5 = setup_4 %>%
        strsplit(",", fixed=T) %>%
        unlist()
      condition = setup_5[which(grepl("condition:", setup_5))] %>%
        lapply(substr, 11, nchar(.)) %>%
        unlist()
      side = setup_5[which(grepl("side:", setup_5))] %>%
        lapply(substr, 6, nchar(.)) %>%
        unlist()
      object = setup_5[which(grepl("object:", setup_5))] %>%
        lapply(substr, 8, nchar(.)) %>%
        unlist()
      doors = setup_5[which(grepl("doors:", setup_5))] %>%
        lapply(substr, 7, nchar(.)) %>%
        unlist()
      
      # Add the pseudo-workerids to the setup information.
      setup_6 = data.frame(pworkerid, condition, side, object, doors)
      
      # Add the setup information to the results.
      results_4 = results_3 %>%
        left_join(setup_6)
      
      # Finally, stitch everything together.
      results_5 = rbind(results_5, results_4)
    }
  }
}

# Combine trial type and trial number into the same column.
results_6 = results_5 %>%
  mutate(trial=gsub("num", "", paste(trial_type, num, sep=""))) %>%
  select(-trial_type, -num)

# Filter out exclusions.
exclusions = c()
for (id in unique(results_6$pworkerid)) {
  results_7 = results_6 %>% 
    filter(pworkerid==id)
  
  if (results_7$condition[1] == "object") {
    if (filter(results_7, trial=="exclusion_1")["target"] != 1) {
      exclusions = c(exclusions, results_7$pworkerid[1])
    }
  }
  else if (results_7$condition[1] == "symbol") {
    if (filter(results_7, trial=="exclusion_2")["target"] != 1) {
      exclusions = c(exclusions, results_7$pworkerid[1])
    }
  }
}
results_8 = results_6 %>%
  filter(!(pworkerid %in% exclusions))

# Compute a Fisher's exact test to see if the condition (i.e., trial order) has
# an effect.
# results_9 = results_8 %>%
#   filter(trial %in% c("trial_1", "trial_2")) %>%
#   group_by(condition, trial) %>%
#   summarize(unmodified=sum(target), modified=(n()-unmodified)) %>%
#   filter((condition=="object"&trial=="trial_2")|(condition=="symbol"&trial=="trial_1")) %>%
#   ungroup() %>%
#   select(-condition, -trial)
# fisher.test(results_9)

# Simulate having the full data.
# results_10 = results_9 * data.frame(c(4, 8), c(4, 8))
# fisher.test(results_10)

# Compute 95% bootstrapped CIs.
compute_mean = function(data, indices) {
  return(mean(data[indices]))
}

compute_bootstrap = function(data, cond, tri) {
  bool_data = data %>%
    filter(condition==cond, trial==tri)

  simulations = boot(bool_data$target,
                     statistic=compute_mean,
                     R=10000)
  
  return(boot.ci(simulations, type="perc")$perc)
}

bootstrap_ci = compute_bootstrap(results_8, "object", "trial_1")
object_1_lower_ci = bootstrap_ci[4]
object_1_upper_ci = bootstrap_ci[5]

bootstrap_ci = compute_bootstrap(results_8, "object", "trial_2")
object_2_lower_ci = bootstrap_ci[4]
object_2_upper_ci = bootstrap_ci[5]

bootstrap_ci = compute_bootstrap(results_8, "symbol", "trial_1")
symbol_1_lower_ci = bootstrap_ci[4]
symbol_1_upper_ci = bootstrap_ci[5]

bootstrap_ci = compute_bootstrap(results_8, "symbol", "trial_2")
symbol_2_lower_ci = bootstrap_ci[4]
symbol_2_upper_ci = bootstrap_ci[5]

lower_ci = c(object_1_lower_ci, object_2_lower_ci, symbol_1_lower_ci, symbol_2_lower_ci,
             object_1_lower_ci, object_2_lower_ci, symbol_1_lower_ci, symbol_2_lower_ci)
upper_ci = c(object_1_upper_ci, object_2_upper_ci, symbol_1_upper_ci, symbol_2_upper_ci,
             object_1_upper_ci, object_2_upper_ci, symbol_1_upper_ci, symbol_2_upper_ci)

# Compute the endorsement for the unmodified door (as percentages).
results_11 = results_8 %>% 
  filter(trial %in% c("trial_1", "trial_2")) %>%
  group_by(condition, trial) %>%
  summarize(unmodified=sum(target)/n()) %>%
  mutate(modified=1-unmodified) %>%
  gather(door, endorsement, unmodified, modified) %>%
  ungroup() %>%
  mutate(lower_ci=lower_ci, upper_ci=upper_ci)

# Plot the data. * Make plots prettier and add CIs.
results_11 %>%
  ggplot(aes(x=trial, y=endorsement, fill=door)) + 
  geom_histogram(stat="identity") +
  theme_bw() +
  facet_wrap(~condition) +
  geom_errorbar(aes(ymin=lower_ci, ymax=upper_ci), width=0.3) +
  coord_cartesian(ylim=c(0.0, 1.0))

# Filter by object.
p0 = results_6 %>% 
  filter(object=="tape") %>%
  filter(trial %in% c("trial_1", "trial_2")) %>% 
  group_by(condition, trial) %>% 
  summarize(unmodified=sum(target)/n()) %>% 
  mutate(modified=1-unmodified) %>% 
  gather(door, endorsement, unmodified, modified)

p0 %>% ggplot(aes(x=trial, y=endorsement, fill=door)) + 
  geom_histogram(stat="identity") +
  theme_bw() +
  facet_wrap(~condition) +
  coord_cartesian(ylim=c(0.0, 1.0))

p1 = results_8 %>% 
  filter(object=="fishbowl") %>%
  filter(trial %in% c("trial_1", "trial_2")) %>% 
  group_by(condition, trial) %>% 
  summarize(unmodified=sum(target)/n()) %>% 
  mutate(modified=1-unmodified) %>% 
  gather(door, endorsement, unmodified, modified)

p1 %>% ggplot(aes(x=trial, y=endorsement, fill=door)) + 
  geom_histogram(stat="identity") +
  theme_bw() +
  facet_wrap(~condition) +
  coord_cartesian(ylim=c(0.0, 1.0))

