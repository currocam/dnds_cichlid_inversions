#!/usr/bin/env Rscript
library(tidyverse)
commands <- commandArgs(trailingOnly = TRUE)
infile <- commands[1]
outfile <- commands[2]
data <- read_csv(infile)
data |>
  pivot_longer(c(`dNdS`, `dDdS`), names_to = "type", values_to = "value") |>
  ggplot(aes(x = r_bin, y = value, color = type)) +
  geom_boxplot(aes(group = interaction(r_bin, type)))+
  geom_hline(yintercept = 1, linetype = "dashed")+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("Deviation from expected ratio")+
  scale_color_manual(
    name = "",
    values = c("dNdS" = "firebrick", "dDdS" = "lightblue"),
    labels = c("dNdS" = "Non-synonymous / Synonymous", "dDdS" = "Deleterious non-synonymous / Synonymous")
    )+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0))+
  scale_y_log10()

data |>
  pivot_longer(c(`dNdS`, `dDdS`), names_to = "type", values_to = "value") |>
  ggplot(aes(x = r_bin, y = value, color = type)) +
  geom_boxplot(aes(group = interaction(r_bin, type)))+
  geom_hline(yintercept = 1, linetype = "dashed")+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("Deviation from expected ratio")+
  scale_color_manual(
    name = "",
    values = c("dNdS" = "firebrick", "dDdS" = "lightblue"),
    labels = c("dNdS" = "Non-synonymous / Synonymous", "dDdS" = "Deleterious non-synonymous / Synonymous")
    )+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0))+
  scale_y_log10()

ggsave(outfile, width = 5.7, height = 5.7, units = "cm", dpi = "retina", scale=3)


