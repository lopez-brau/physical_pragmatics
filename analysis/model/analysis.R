# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the model data.
data_0 = read_csv("data/model/enforcer_action_vs_actor_reward.csv")

# Set up the ways in which the actor can integrate social reward.
confidence = c(-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0)

# Plots the model predictions for how the enforcers action changes as a
# function of the actor's reward (as well as rationality, ToM, method of 
# integrating others' rewards, and cooperation.
plot_0 = data_0 %>%
  filter(Rationality==0.1) %>%
  ggplot(aes(x=Actor_Reward, y=Enforcer_Action, group=factor(ToM)))

plot_0 +
  geom_point(aes(color=factor(ToM)), size=3) +
  geom_line(aes(color=factor(ToM))) +
  facet_wrap(Method~Cooperation, nrow=3) +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  ylab("Enforcer Action") +
  xlab("Actor Preference (A <= B)") +
  scale_y_discrete(limits=c(0:9)) +
  coord_cartesian(ylim=c(0,9)) +
  scale_x_discrete(limits=c(0:9))

# Plot 2 - same but with actor ToM on x axis
#data_2 = data_0 %>%
#  filter(Rationality==0.1, Cooperation %in% cooperation_set) %>%
#  mutate(Actor_Preference=B-A)

# data_2 = data_0 %>%
#   filter(Rationality==1.0, Method=="confidence", Cooperation==10.0) %>%
#   mutate(Actor_Preference=B-A) %>%
#   filter(Actor_Preference %in% c(0, 2, 4, 6, 8))

plot_1 = data_0 %>%
  filter(Actor_Reward>=0) %>%
  mutate(Actor_Reward=factor(Actor_Reward)) %>%
  ggplot(aes(x=ToM, y=Enforcer_Action, group=Actor_Reward))

plot_1 +
  geom_point(aes(color=Actor_Reward), size=3) +
  geom_line(aes(color=Actor_Reward)) +
  facet_wrap(Method~Cooperation, nrow=3) +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  ylab("Enforcer Action") +
  xlab("ToM") +
  scale_y_discrete(limits=c(0:9)) +
  coord_cartesian(ylim=c(0,9)) +
  scale_x_discrete(limits=c(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))

# Plot 3.
data_2 = read_csv("data/model/actor_action_vs_enforcer_action.csv")

plot_2 = data_2 %>%
  filter(Rationality==0.1, ToM=="confidence") %>%
  ggplot(aes(x=Enforcer_Action, y=Actor_Action, group=Method))

plot_2 +
  geom_point(aes(color=Method), size=3) +
  geom_line(aes(color=Method)) +
  facet_wrap(Cooperation) +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  ylab("Actor Preference for A") +
  xlab("Enforcer Action") +
  scale_y_discrete(limits=c(0:1)) +
  scale_x_discrete(limits=c(0:9))
