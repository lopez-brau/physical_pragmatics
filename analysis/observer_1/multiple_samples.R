# Load libraries.
library(tidyverse)
library(gridExtra)

# Set working directory.
setwd("D:/Research/social_pragmatics/")

# Load data.

# trials_1 = read.csv("pilot_1/observer_1-trials.csv")
# trials_2 = read.csv("pilot_2/observer_1-trials.csv")
#trials_3 = read.csv("pilot_3/observer_1-trials.csv")
#trials_4 = read.csv("pilot_4/observer_1-trials.csv")
#trials_5 = read.csv("pilot_5/observer_1-trials.csv")
trials_6 = read.csv("data/observer_1/human/pilot_6/observer_1-trials.csv")
# trials_7 = read.csv("pilot_7/observer_1-trials.csv")
total_trials = list(trials_3, trials_4, trials_5, trials_6)
total_trials = list(trials_6)
# catch_trial = read.csv("observer_1-catch_trials.csv")
# subj_info = read.csv("observer_1-subject_information.csv")

# Set up the stimuli.
stimuli = c(
  "[2 2]_[0 0]",
  "[2 2]_[1 0]",
  "[2 2]_[2 0]", 
  "[2 2]_[3 0]", 
  "[2 3]_[0 0]",
  "[2 3]_[1 0]",
  "[2 3]_[2 0]",
  "[2 3]_[3 0]",
  "[2 4]_[0 0]",
  "[2 4]_[1 0]",
  "[2 4]_[2 0]",
  "[2 4]_[3 0]",
  "[3 2]_[0 0]",
  "[3 2]_[1 0]",
  "[3 2]_[2 0]",
  "[3 2]_[3 0]",
  "[3 3]_[0 0]",
  "[3 3]_[1 0]",
  "[3 3]_[2 0]",
  "[3 3]_[3 0]",
  "[3 4]_[0 0]",
  "[3 4]_[1 0]",
  "[3 4]_[2 0]",
  "[3 4]_[3 0]",
  "[4 2]_[0 0]",
  "[4 2]_[1 0]",
  "[4 2]_[2 0]",
  "[4 2]_[3 0]",
  "[4 3]_[0 0]",
  "[4 3]_[1 0]",
  "[4 3]_[2 0]",
  "[4 3]_[3 0]",
  "[4 4]_[0 0]",
  "[4 4]_[1 0]",
  "[4 4]_[2 0]",
  "[4 4]_[3 0]"
)

total_scaled_agent_rewards = data.frame()
total_scaled_ToM = data.frame()
for (trials in total_trials) {
  # Extract model predictions.
  filenames = c()
  model_agent_rewards = c()
  model_ToM = c()
  for (i in 1:nrow(trials)) {
      
    filename = trials[i,][,"filename"] %>%
      as.character() %>%
      substr(2, 12)
    filenames = c(filenames, filename)
    # Enforcer actions = [[0, 0], [1, 0], [2, 0], [3, 0]]
    # filepath = paste("../../model_full/", filename, ".txt.dat", sep="")
    # Enforcer actions = [[0, 0], [1, 0], [0, 1], [1, 1], [2, 0], ...
    # filepath = paste("../../model/", filename, ".txt.dat", sep="")
    # Enforcer actions = [[1, 0], [2, 0], [3, 0]]
    filepath = paste("data/observer_1/model/0123/1.0/", filename, ".txt", sep="")
    model_predictions = read.csv(filepath, header=FALSE)
    
    # Store model predictions.
    model_agent_rewards = c(model_agent_rewards, model_predictions[2,])
    model_ToM = c(model_ToM, model_predictions[3,])
  }
  
  # Package human and model predictions.
  agent_rewards = data.frame(
    workerid = trials[,"workerid"],
    model = model_agent_rewards,
    human = trials[,"target_0"],
    filenames = filenames
  )
  ToM = data.frame(
    workerid = trials[,"workerid"],
    model = model_ToM,
    human = trials[,"target_1"],
    filenames = filenames
  )
  
  # z-score human (within-subject) and model predictions.
  scaled_agent_rewards = agent_rewards %>%
    group_by(workerid) %>%
    do(data.frame(model=.$model,zmodel=scale(.$model)[,1],
                  human=.$human,zhuman=scale(.$human)[,1]))
  scaled_agent_rewards = data.frame(scaled_agent_rewards, agent_rewards["filenames"])
  scaled_ToM = ToM %>%
    group_by(workerid) %>%
    do(data.frame(model=.$model,zmodel=scale(.$model)[,1],
                  human=.$human,zhuman=scale(.$human)[,1]))
  scaled_ToM = data.frame(scaled_ToM, ToM["filenames"])
  total_scaled_agent_rewards = rbind(total_scaled_agent_rewards, scaled_agent_rewards)
  total_scaled_ToM = rbind(total_scaled_ToM, scaled_ToM)
}
scaled_agent_rewards = total_scaled_agent_rewards
scaled_ToM = total_scaled_ToM

# [Agent Rewards] Plot z-scored model comparisons for each participant.
ggplot(scaled_agent_rewards, aes(x=zmodel, y=zhuman)) + 
  geom_point() + facet_wrap(~workerid, scales="free") + geom_smooth(method="lm") +
  ggtitle("Model Comparison of Agent Rewards per participant")

# [Agent Rewards] Summarize over all trials.
filtered_agent_rewards = scaled_agent_rewards %>%
  group_by(filenames) %>%
  summarize(mean_zmodel=mean(zmodel), mean_zhuman=mean(zhuman))
r2 = cor(filtered_agent_rewards$mean_zmodel, filtered_agent_rewards$mean_zhuman)
ggplot(filtered_agent_rewards, aes(x=mean_zmodel, y=mean_zhuman)) + geom_point() + 
  geom_smooth(method="lm") + ggtitle("Model Comparison of Agent Rewards") +
  theme_classic() + 
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab("Mean Model Performance") +
  ylab("Mean Human Predictions") + 
  geom_text(x=-0.8, y=1, label=paste("r = ", r2, sep=""))
  
ggsave("agent_rewards.png", g1)

# [Agent Rewards] Summarize over all data.
filtered_agent_rewards = scaled_agent_rewards
ggplot(filtered_agent_rewards, aes(x=zmodel, y=zhuman)) + geom_point() + 
  ggtitle("Model Comparison of Agent Rewards") + geom_smooth(method="lm")

# [ToM] Plot z-scored model comparisons for each participant.
ggplot(scaled_ToM, aes(x=zmodel, y=zhuman)) + geom_point() + 
  facet_wrap(~workerid, scales="free") + geom_smooth(method="lm") + 
  ggtitle("Model Comparison of ToM per participant")

# [ToM] Summarize over all trials.
filtered_ToM = scaled_ToM %>%
  group_by(filenames) %>%
  summarize(mean_zmodel=mean(zmodel), mean_zhuman=mean(zhuman))
r2 = cor(filtered_ToM$mean_zmodel, filtered_ToM$mean_zhuman)
g2 = ggplot(filtered_ToM, aes(x=mean_zmodel, y=mean_zhuman)) + geom_point() + 
  geom_smooth(method="lm") + ggtitle("Model Comparison of ToM") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab("Mean Model Performance") +
  ylab("Mean Human Predictions") + 
  geom_text(x=-1.2, y=0.8, label=paste("r = ", r2, sep=""))
g2
# ggsave("ToM.png", g2)

# [ToM] Summarize over all data.
filtered_ToM = scaled_ToM 
ggplot(filtered_ToM, aes(x=zmodel, y=zhuman)) + geom_point() + 
  ggtitle("Model Comparison of ToM") + geom_smooth(method="lm")
