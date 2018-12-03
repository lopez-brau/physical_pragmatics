# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the model data.
data_0 = read_csv("data/model/enforcer_action_vs_actor_reward.csv")

# Set up the ways in which the actor can integrate social reward.
social_reward = data.frame(
  confidence=c(-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0),
  preference=c(-25.0, -20.0, -15.0, -10.0, -5.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0),
  proportional=c(-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5)
)

# Plots the model predictions for how the enforcers action changes as a
# function of the actor's reward (as well as rationality, ToM, method of 
# integrating others' rewards, and cooperation.
data_1 = data_0 %>%
  filter(Rationality==0.1) %>%
  mutate(Actor_Preference=B-A)

plot_0 = data_1 %>%
  ggplot(aes(x=Actor_Preference, y=Enforcer_Action, group=factor(ToM)))

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
data_2 = data_0 %>% 

# data_2 = data_0 %>%
#   filter(Rationality==1.0, Method=="confidence", Cooperation==10.0) %>%
#   mutate(Actor_Preference=B-A) %>%
#   filter(Actor_Preference %in% c(0, 2, 4, 6, 8))

plot_1 = data_2 %>%
  filter(Actor_Preference>=0) %>%
  mutate(Actor_Preference=factor(B-A)) %>%
  ggplot(aes(x=ToM, y=Enforcer_Action, group=Actor_Preference))

plot_1 +
  geom_point(aes(color=Actor_Preference), size=3) +
  geom_line(aes(color=Actor_Preference)) +
  facet_wrap(Method~Cooperation, nrow=3) +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  ylab("Enforcer Action") +
  xlab("ToM") +
  scale_y_discrete(limits=c(0:9)) +
  coord_cartesian(ylim=c(0,9)) +
  scale_x_discrete(limits=c(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))

# Plot 3.
#data_3 = read_csv("data/actor_0/model/actor_choice_vs_enforcer_action.csv")
data_3 = read_csv("data/actor_0/model/new_0.csv")

data_4 = data_3 %>%
  filter(Rationality==1.0, Cooperation %in% cooperation_set) %>%
  mutate(Actor_Choice=A/(A+B), ToM=factor(ToM))
    
plot_2 = data_4 %>%
  ggplot(aes(x=Enforcer_Action, y=Actor_Choice, group=ToM))

plot_2 +
  geom_point(aes(color=ToM), size=3) +
  geom_line(aes(color=ToM)) +
  facet_wrap(Method~Cooperation, nrow=3) +
  theme_bw() +
  theme(plot.title=element_text(hjust=0.5)) +
  ylab("Actor Preference for A") +
  xlab("Enforcer Action") +
  scale_y_discrete(limits=c(0:1)) +
  scale_x_discrete(limits=c(0:9))
