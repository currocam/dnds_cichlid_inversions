#!/usr/bin/env Rscript
library(tidyverse)
commands <- commandArgs(trailingOnly = TRUE)
infile <- commands[1]
outfile <- commands[2]
data <- read_csv(infile)
data |>
  ggplot(aes(x = r_bin, y = dNdS)) +
  geom_smooth(aes(group = SEED), color = "grey", alpha = 0.1, size = 0.5)+
  geom_boxplot(aes(group = r_bin), outlier.shape = NA)+
  geom_hline(yintercept = 1, linetype = "dashed")+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("dN/dS")+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0))+
  scale_y_log10()

ggsave(outfile, width = 5.7, height = 5.7, units = "cm", dpi = "retina", scale=3)


