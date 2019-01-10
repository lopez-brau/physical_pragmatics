# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the model data.
data_0 = read_csv("data/model/enforcer_action_vs_actor_reward.csv")

# For the plots for the paper, we only want to set the rationality to 0.1, 
# use the confidence method, and set the cooperation parameter to 10. 
data_1 = data_0 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==10)

# Plot 1: Plots the model predictions for how the enforcer's action changes as
# a function of the actor's reward (as well as rationality, ToM, method of 
# integrating others' rewards, cooperation, and the enforcer's reward).
data_1 %>%
  filter(Enforcer_Reward==9, ToM %in% c(0.0, 0.3, 0.7, 1.0)) %>%
  ggplot(aes(x=Actor_Reward, y=Enforcer_Action, group=factor(ToM))) + 
    geom_point(aes(color=factor(ToM)), size=3) +
    geom_line(aes(color=factor(ToM))) +
    theme_bw() +
    theme(plot.title=element_text(hjust=0.5)) +
    ylab("Enforcer Action") +
    xlab("Actor Preference (A <= B)") +
    scale_y_continuous(breaks=c(0:9)) +
    scale_x_continuous(breaks=c(-9:9)) +
    coord_cartesian(ylim=c(0,9))

# Plot 2: Plots the model predictions for how the enforcer's action changes as
# a function of the actor's ToM (as well as rationality, actor's reward, method 
# of integrating others' rewards, cooperation, and the enforcer's reward).
data_1 %>%
  filter(Enforcer_Reward==9, 
         Actor_Reward %in% c(0, 3, 7, 9)) %>%
  ggplot(aes(x=ToM, y=Enforcer_Action, group=factor(Actor_Reward))) +
    geom_point(aes(color=factor(Actor_Reward)), size=3) +
    geom_line(aes(color=factor(Actor_Reward))) +
    theme_bw() +
    theme(plot.title=element_text(hjust=0.5)) +
    ylab("Enforcer Action") +
    xlab("ToM") +
    scale_y_continuous(breaks=c(0:9)) +
    scale_x_continuous(breaks=c(0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)) + 
    coord_cartesian(ylim=c(0,9))
    

# Plot 3: Plots the model predictions for how the actor's action changes as a
# function of the enforcer's actions.
data_2 = read_csv("data/model/actor_action_vs_enforcer_action.csv")

# For the plots for the paper, we only want to set the rationality to 0.1, 
# use the confidence method, and set the cooperation parameter to 10.  
data_3 = data_2 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==10, Actor_Reward==4)

data_3 %>%
  ggplot(aes(x=Enforcer_Action, y=Actor_Action_A, group=ToM)) +
    geom_point(aes(color=factor(ToM)), size=3) +
    geom_line(aes(color=factor(ToM))) +
    theme_classic() +
    theme(plot.title=element_text(hjust=0.5)) +
    ylab("Actor Choice") +
    xlab("Enforcer Action") +
    scale_y_continuous(breaks=c(0:1), labels=c("A", "B")) +
    scale_x_continuous(breaks=c(0:9)) + 
    scale_color_manual(name="Theory of Mind", labels=c("None", "Full"), 
                       values=c("cyan","red"))
