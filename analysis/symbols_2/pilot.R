# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics/")

# Set up the conditions and the different objects participants can see.
conditions = c("congruent", "incongruent")
objects = c("chair", "plant", "books", "cinderblocks", "tape", "rulers", "hat", "string")

# Read in the data.
data_0 = read_csv("data/symbols_2/pilot_1/symbols_2-trials.csv") %>%
  mutate(workerid=workerid+9) %>%
  rbind(read_csv("data/symbols_2/pilot_0/symbols_2-trials.csv")) %>%
  arrange(workerid) %>%
  mutate(pworkerid=as.integer(workerid)) %>%
  select(-workerid)

# Combine the trial and exclusion columns.
data_1 = data_0 %>%
  gather(trial_type, num, trial_num, exclusion_num) %>%
  na.omit() %>%
  mutate(trial=gsub("num", "", paste(trial_type, num, sep=""))) %>%
  select(-trial_type, -num) %>%
  mutate(target=gsub("\"", "", target))

# Import the setup information.
setup_0 = c(
  read_csv("data/symbols_2/pilot_0/symbols_2-mturk.csv")$Answer.setup,
  read_csv("data/symbols_2/pilot_1/symbols_2-mturk.csv")$Answer.setup
)

# Remove the quotes, backslashes, and braces.
setup_1 = gsub("\\", "", setup_0, fixed=T)
setup_2 = gsub("\"", "", setup_1, fixed=T)
setup_3 = gsub("{", "", setup_2, fixed=T)
setup_4 = gsub("}", "", setup_3, fixed=T)

# Stitch the setup information to the data.
setup_6 = tibble()
for (id in unique(data_1$pworkerid)) {
  # Do some string processing to transform the json into something usable.
  setup_5 = setup_4[id+1] %>%
    strsplit(",", fixed=T) %>%
    unlist()
  condition = setup_5[which(grepl("condition:", setup_5))] %>%
    lapply(substr, 11, nchar(.)) %>%
    unlist()
  first_side = setup_5[which(grepl("first_side:", setup_5))] %>%
    lapply(substr, 12, nchar(.)) %>%
    unlist()
  second_side = setup_5[which(grepl("second_side:", setup_5))] %>%
    lapply(substr, 13, nchar(.)) %>%
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
  
  # Stich the setup information to the data.
  setup_6 = rbind(setup_6, tibble(pworkerid=id, condition, first_side, second_side,
                                  first_object, second_object, doors))
}
data_2 = data_1 %>%
  left_join(setup_6)

# Filter out exclusions.
exclusions = c()
for (id in unique(data_2$pworkerid)) {
  data_3 = data_2 %>% 
    filter(pworkerid==id, trial=="exclusion_1")
  
  if (data_3$target != data_3$first_side) {
    exclusions = c(exclusions, id)
  }
}
data_4 = data_2 %>%
  filter(!(pworkerid %in% exclusions))

# Compute 95% bootstrapped CIs.
compute_mean = function(data, indices) {
  return(mean(data[indices]))
}

compute_bootstrap = function(data, cond, tri) {
  bool_data = data %>%
    filter(condition==cond, trial==tri)
  
  simulations = boot(as.integer(bool_data$target),
                     statistic=compute_mean,
                     R=10000)
  
  return(boot.ci(simulations, type="perc")$perc)
}

lower_ci = c()
upper_ci = c()

bootstrap_ci = compute_bootstrap(data_4, "congruent", "trial_1")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

bootstrap_ci = compute_bootstrap(data_4, "congruent", "trial_2")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

bootstrap_ci = compute_bootstrap(data_4, "incongruent", "trial_1")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

bootstrap_ci = compute_bootstrap(data_4, "incongruent", "trial_2")
lower_ci = c(lower_ci, bootstrap_ci[4])
upper_ci = c(upper_ci, bootstrap_ci[5])

# Plot the endorsement for the unmodified door (as percentages).
data_5 = data_4 %>% 
  filter(trial %in% c("trial_1", "trial_2")) %>%
  mutate(target=as.integer(target)) %>%
  group_by(condition, trial) %>%
  summarize(unmodified=(sum(target)/n()*100)) %>%
  mutate(modified=100-unmodified) %>%
  gather(door, endorsement, unmodified, modified) %>%
  ungroup() %>%
  mutate(lower_ci=(c(lower_ci, lower_ci)*100), upper_ci=(c(upper_ci, upper_ci)*100))

data_5 %>%
  ggplot(aes(x=trial, y=endorsement, fill=door)) + 
  geom_histogram(stat="identity") +
  theme_bw() +
  facet_wrap(~factor(condition, 
                     levels=c("congruent", "incongruent"),
                     labels=c("Congruent","Incongruent"))) +
  geom_errorbar(aes(ymin=lower_ci, ymax=upper_ci), width=0.3) +
  scale_x_discrete(limits=c("trial_1", "trial_2"), 
                   labels=c("Object", "Symbol")) +
  scale_fill_discrete(name="Response",
                      limits=c("modified", "unmodified"),
                      labels=c("Modified", "Unmodified")) +
  ylab("Endorsement (%)") +
  xlab("Trial")
