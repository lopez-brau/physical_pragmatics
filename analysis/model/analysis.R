# Load libraries.
library(boot)
library(latex2exp)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the model data.
data_0 = read_csv("data/model/enforcer_action_vs_actor_reward.csv")

# Plot 0: Plots the model predictions for how the enforcer's action changes as
# a function of the actor's reward (as well as rationality, ToM, method of 
# integrating others' rewards, cooperation, and the enforcer's reward). For 
# the plots for the paper, we only want to set the rationality to 0.1, use the
# confidence method, set the cooperation parameter to 10, max out the 
# enforcer's preference, and use a subset of the ToM parameters. 
data_0 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==10,
         Enforcer_Reward==5, ToM %in% c(0.0, 1.0), Actor_Reward %in% c(0:5)) %>%
  ggplot(aes(x=Actor_Reward, y=Enforcer_Action, group=factor(ToM))) + 
    geom_line(aes(color=factor(ToM))) +  
    geom_point(aes(color=factor(ToM)), size=2) +
    theme_classic() +
    theme(plot.title=element_text(hjust=0.5),
          axis.text=element_text(size=12),
          axis.title=element_text(size=12)) +
    ylab("Enforcer's action\n\n\n\n\n\n") +
    xlab("\n\n\nActor preference of \ \ - - - - - - \ \ over \ \ - - - - - -") +
    scale_y_continuous(breaks=c(0:5), labels=rep(c(""), 6)) +
    scale_x_continuous(breaks=c(0:5), 
                       labels=c("0\nNot at all", "1", "2", "3", "4", "5\nVery much")) +
    coord_cartesian(ylim=c(0,5)) +
    scale_color_manual(name="Theory of Mind", labels=c("None", "Full"), 
                       values=c("#F8766D", "#00BFC4"))

# Plot 1: Similar to Plot 1, except cooperation is set to 0 (i.e., the agent
# is not cooperative). For the plots for the paper, we want to keep everything
# else the same as in Plot 1.
data_0 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==0,
         Enforcer_Reward==5, ToM %in% c(0.0, 1.0), Actor_Reward %in% c(0:5)) %>%
  ggplot(aes(x=Actor_Reward, y=Enforcer_Action, group=factor(ToM))) + 
    geom_line(aes(color=factor(ToM))) +
    geom_point(aes(color=factor(ToM)), size=2) +
    theme_classic() +
    theme(plot.title=element_text(hjust=0.5),
          axis.text=element_text(size=12),
          axis.title=element_text(size=12)) +
    ylab("Enforcer's action\n\n\n\n\n\n") +
    xlab("\n\n\nActor preference of \ \ - - - - - - \ \ over \ \ - - - - - -") +
    scale_y_continuous(breaks=c(0:5), labels=rep(c(""), 6)) +
    scale_x_continuous(breaks=c(0:5), 
                       labels=c("0\nNot at all", "1", "2", "3", "4", "5\nVery much")) +
    coord_cartesian(ylim=c(0,5)) +
    scale_color_manual(name="Theory of Mind", labels=c("None", "Full"), 
                       values=c("#F8766D", "#00BFC4"))

# Plot 2: Plots the model predictions for how the enforcer's action changes as
# a function of the actor's ToM (as well as rationality, actor's reward, method 
# of integrating others' rewards, cooperation, and the enforcer's reward).
data_0 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==10,
         Enforcer_Reward==5, Actor_Reward %in% c(0, 2, 5)) %>%
  ggplot(aes(x=ToM, y=Enforcer_Action, group=factor(Actor_Reward))) +
    geom_line(aes(color=factor(Actor_Reward))) +
    geom_point(aes(color=factor(Actor_Reward)), size=2) +
    theme_classic() +
    theme(plot.title=element_text(hjust=0.5),
          axis.text=element_text(size=12),
          axis.title=element_text(size=12)) +
    ylab("Enforcer's action\n\n\n\n\n\n") +
    xlab("Theory of Mind") +
    scale_y_continuous(breaks=c(0:5), labels=rep(c(""), 6)) +
    scale_x_continuous(breaks=seq(0.0, 1.0, by=0.1), 
                       labels=c("0.0\nNone", "0.1", "0.2", "0.3", "0.4", "0.5",
                                "0.6", "0.7", "0.8", "0.9", "1.0\nFull")) + 
    coord_cartesian(ylim=c(0,5)) +
    scale_color_manual(name="Actor Preference", 
                       labels=c("Not at all", "Somewhat", "Very much"),
                       values=c("#F8766D","#00BA38", "#00BFC4"))
    
# Plot 3: Plots the model predictions for how the actor's action changes as a
# function of the enforcer's actions.
data_1 = read_csv("data/model/actor_action_vs_enforcer_action.csv")

data_1 %>%
  filter(Rationality==0.1, Method=="confidence", Cooperation==10, Actor_Reward==2,
         Enforcer_Action %in% c(0:5)) %>%
  ggplot(aes(x=Enforcer_Action, y=Actor_Action_A, group=ToM)) +
    geom_point(aes(color=factor(ToM)), size=2) +
    geom_line(aes(color=factor(ToM))) +
    theme_classic() +
    theme(plot.title=element_text(hjust=0.5),
          axis.text=element_text(size=12),
          axis.title=element_text(size=12)) +
    ylab("Probability of actor picking \ \ - - - - - - \n\n\n") +
    xlab("\n\n\n\n\nEnforcer's action") +
    scale_y_continuous(breaks=c(0.0, 0.5, 1.0), labels=c("0.0", "0.5", "1.0")) +
    scale_x_continuous(breaks=c(0:9), labels=rep(c(""), times=10)) + 
    scale_color_manual(name="Theory of Mind", labels=c("None", "Full"), 
                       values=c("#F8766D","#00BFC4"))
