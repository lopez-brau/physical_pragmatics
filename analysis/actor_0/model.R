# Load libraries.
library(boot)
library(tidyverse)

# Set the path.
setwd("D:/Research/social_pragmatics")

# Import the model data.

data_0 = read_csv("analysis/actor_0/temp.csv", col_names=FALSE)
data_1 = read_csv("analysis/actor_0/temp2.csv", col_names=FALSE)

names(data_0) = c("Actor_Preference", "Enforcer_Action", "ToM")
names(data_1) = c("Actor_Preference", "Enforcer_Action", "ToM")

plot_0 = data_0 %>%
  mutate(ToM=factor(ToM)) %>%
  ggplot(aes(x=Actor_Preference, y=Enforcer_Action))

plot_0 +
  geom_point(aes(shape=ToM, color=ToM), size=5) + 
  theme_bw() +
  ggtitle("Cooperation = 0.0") +
  ylab("Enforcer Action") +
  xlab("Actor Preference (A <= B)") +
  scale_y_discrete(limit=c(0:9)) +
  scale_x_discrete(limit=c(0:9))

plot_1 = data_1 %>%
  mutate(ToM=factor(ToM)) %>%
  ggplot(aes(x=Actor_Preference, y=Enforcer_Action))

plot_1 +
  geom_point(aes(shape=ToM, color=ToM), size=5) + 
  theme_bw() +
  ylab("Enforcer Action") +
  xlab("Actor Preference (A <= B)") +
  scale_y_discrete(limit=c(0:9)) +
  scale_x_discrete(limit=c(0:9))

# y-axis: Enforcer behavior 
# x-axis: actor's preferences
# facet_wrap(~cooperation, nrow=1)
# Fix the enforcer reward and compute the relevant stuff

# Plot 2 - same but with actor ToM on x axis
#data_1 = read_csv("temp2.csv", col_names=FALSE)

data_2 = read_csv("plot_2.csv", col_names=FALSE)

names(data_2) = c("a", "b", "y", "p")

data_3 = data_2 %>%
  mutate(preference_B=b-a)

data_3 %>%
  filter(preference_B %in% c(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)) %>%
  ggplot(aes(x=p, y=y, group=preference_B)) + 
    theme_bw() + 
    geom_point(aes(color=factor(preference_B)), size=5) + 
    geom_line() +
    scale_x_discrete(limit=c(0:9)) +
    scale_y_discrete(limit=c(0:9))

data_3 %>%
  filter(preference_B %in% c(0, -1, -2, -3, -4, -5, -6, -7, -8, -9)) %>%
  ggplot(aes(x=p, y=y, group=preference_B)) + 
    theme_bw() + 
    geom_point(aes(color=factor(preference_B)), size=5) + 
    geom_line() +
    scale_x_discrete(limit=c(0:9)) +
    scale_y_discrete(limit=c(0:9))

# Plot 3.
data_4 = read_csv("plot_3.csv", col_names=FALSE)

names(data_4) = c("x", "a", "b", "p")

data_5 = data_4 %>%
  mutate(preference=a/(a+b))

plot_4 = data_5 %>%
  ggplot(aes(x=x, y=preference, group=p))


plot_4 +
  theme_bw() + 
  geom_point(aes(color=factor(p)), size=5) + 
  geom_line(aes(color=factor(p))) +
  scale_x_discrete(limit=c(0:9))


