# Load libraries.
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics/")

# Set up the conditions and the different objects participants can see.
conditions = c("congruent", "incongruent")
objects = c("chair", "plant", "books", "cinderblocks", "tape", "rulers", "hat", "string")

# Read in the data.
data_0 = read_csv("data/symbols_1/pilot_1/symbols_1-trials.csv") %>%
  mutate(workerid=(workerid+9)) %>%
  rbind(read_csv("data/symbols_1/pilot_0/symbols_1-trials.csv")) %>%
  arrange(workerid)

# Convert the target column into integers.
data_1 = data_0 %>%
  mutate(target=as.integer(substr(target, 2, 2)))
      
# Combine the trial and exclusion columns.
data_2 = data_1 %>%
  gather(trial_type, num, trial_num, exclusion_num) %>%
  na.omit() %>%
  arrange(workerid)
      
# Import the setup information.
setup_0 = c(
  read_csv("data/symbols_1/pilot_0/symbols_1-mturk.csv")$Answer.setup,
  read_csv("data/symbols_1/pilot_1/symbols_1-mturk.csv")$Answer.setup
)

# Remove the quotes, backslashes, and braces.
setup_1 = gsub("\\", "", setup_0, fixed=T)
setup_2 = gsub("\"", "", setup_1, fixed=T)
setup_3 = gsub("{", "", setup_2, fixed=T)
setup_4 = gsub("}", "", setup_3, fixed=T)
      
# Stitch the setup information to the data.
setup_6 = data.frame()
for (id in 0:17) {
  # Do some string processing to transform the json into something usable.
  setup_5 = setup_4[id+1] %>%
    strsplit(",", fixed=T) %>%
    unlist()
  condition = setup_5[which(grepl("condition:", setup_5))] %>%
    lapply(substr, 11, nchar(.)) %>%
    unlist()
  side = setup_5[which(grepl("side:", setup_5))] %>%
    lapply(substr, 6, nchar(.)) %>%
    unlist()
  first_object = setup_5[which(grepl("first_object:", setup_5))] %>%
    lapply(substr, 14, nchar(.)) %>%
    unlist()
  second_object = setup_5[which(grepl("second_object:", setup_5))] %>%
    lapply(substr, 15, nchar(.)) %>%
    unlist()
  doors = setup_5[which(grepl("doors:", setup_5))] %>%
    lapply(substr, 7, nchar(.)) %>%
    unlist()
  
  # Add the workerids to stich the setup information to the data.
  setup_6 = rbind(setup_6, data.frame(workerid=id, condition, side, first_object, 
                                      second_object, doors))
}
data_3 = data_2 %>%
  left_join(setup_6)
      
# Combine trial type and trial number into the same column.
data_4 = data_3 %>%
  mutate(trial=gsub("num", "", paste(trial_type, num, sep=""))) %>%
  select(-trial_type, -num)

# Filter out exclusions.
exclusions = c()
for (id in unique(data_4$workerid)) {
  data_5 = data_4 %>% 
    filter(workerid==id)

  if (filter(data_5, trial=="exclusion_1")["target"] != 1) {
    exclusions = c(exclusions, id)
  }
}
data_6 = data_4 %>%
  filter(!(workerid %in% exclusions))

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

lower_ci = c()
upper_ci = c()

bootstrap_ci = compute_bootstrap(data_6, "congruent", "trial_1")
# lower_ci = c(lower_ci, bootstrap_ci[4])
# upper_ci = c(upper_ci, bootstrap_ci[5])
lower_ci = c(lower_ci, 1)
upper_ci = c(upper_ci, 1)

bootstrap_ci = compute_bootstrap(data_6, "congruent", "trial_2")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

bootstrap_ci = compute_bootstrap(data_6, "incongruent", "trial_1")
lower_ci = c(lower_ci, bootstrap_ci[4]*100)
upper_ci = c(upper_ci, bootstrap_ci[5]*100)

bootstrap_ci = compute_bootstrap(data_6, "incongruent", "trial_2")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

# Plot the endorsement for the unmodified door (as percentages).
data_7 = data_6 %>% 
  filter(first_object!="hat") %>%
  filter(trial %in% c("trial_1", "trial_2")) %>%
  group_by(condition, trial) %>%
  summarize(unmodified=(sum(target)/n()*100)) %>%
  mutate(modified=100-unmodified) %>%
  gather(door, endorsement, unmodified, modified) %>%
  ungroup() %>%
  mutate(lower_ci=(c(lower_ci, lower_ci)*100), upper_ci=(c(upper_ci, upper_ci)*100))

data_7 %>%
  ggplot(aes(x=trial, y=endorsement, fill=door)) + 
  geom_histogram(stat="identity") +
  theme_bw() +
  facet_wrap(~condition) +
  geom_errorbar(aes(ymin=lower_ci, ymax=upper_ci), width=0.3) +
  scale_x_discrete(limits=c("trial_1", "trial_2"), 
                   labels=c("Object", "Symbol")) +
  scale_fill_discrete(name="Response",
                      limits=c("modified", "unmodified"),
                      labels=c("Modified", "Unmodified")) +
  ylab("Endorsement (%)") +
  xlab("Trial")
  