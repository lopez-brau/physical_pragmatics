# Load libraries.
library(tidyverse)

# Set working directory and which csv file you're getting the data from.
setwd("D:/Research/social_pragmatics")
#data = read.csv("data/observer_1/human/pilot_5/observer_1-trials.csv")
data = read.csv("analysis/observer_1/amanda.json")

# Initialize some storage arrays.
filenames = c()
model_agent_rewards = c()
model_ToM = c()

# Loop through the data and match it with its corresponding model counterpart.
for (i in 1:nrow(data)) {
  # Find the correct file.
  filename = data[i,][,"filename"] %>%
    as.character() %>%
    #substr(2, 12)
    substr(1, 11)
  filenames = c(filenames, filename)
  filepath = paste("data/observer_1/model/0123/1.0/", filename, ".txt", sep="")
  model_predictions = read.csv(filepath, header=FALSE)
  
  # Store model predictions.
  model_agent_rewards = c(model_agent_rewards, model_predictions[2,])
  model_ToM = c(model_ToM, model_predictions[3,])
}

# Package human and model predictions.
agent_rewards = data.frame(
  model = model_agent_rewards,
  human = data[,"target_0"],
  filenames = filenames
)
ToM = data.frame(
  model = model_ToM,
  human = data[,"target_1"],
  filenames = filenames
)

# z-score human and model predictions.
scaled_agent_rewards = agent_rewards %>%
  do(data.frame(model=.$model,zmodel=scale(.$model)[,1],
                human=.$human,zhuman=scale(.$human)[,1]))
scaled_agent_rewards = data.frame(scaled_agent_rewards, agent_rewards["filenames"])
scaled_ToM = ToM %>%
  do(data.frame(model=.$model,zmodel=scale(.$model)[,1],
                human=.$human,zhuman=scale(.$human)[,1]))
scaled_ToM = data.frame(scaled_ToM, ToM["filenames"])

# [Agent Rewards] Plot z-scored model comparisons for each participant.
ggplot(scaled_agent_rewards, aes(x=zmodel, y=zhuman)) + geom_point() + 
  geom_smooth(method="lm") + ggtitle("Model Comparison of Agent Rewards")
cor(scaled_agent_rewards$zmodel, scaled_agent_rewards$zhuman)

# [ToM] Plot z-scored model comparisons for each participant.
ggplot(scaled_ToM, aes(x=zmodel, y=zhuman)) + geom_point() +
  geom_smooth(method="lm") + ggtitle("Model Comparison of ToM per participant")
cor(scaled_ToM$zmodel, scaled_ToM$zhuman)
