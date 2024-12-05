#!/usr/bin/env Rscript
library(tidyverse)
commands <- commandArgs(trailingOnly = TRUE)
infile <- commands[1]
outfile <- commands[2]
data <- read_csv(infile)
expected_ratio <- (data$FRACTION_D+data$FRACTION_C) / data$FRACTION_S
data |>
  mutate(expected = expected_ratio) |>
  mutate(
    dNdS = `Non-synonymous` / `Synonymous` / expected,
    dDdS = Deleterious / `Synonymous` / expected,
  ) |>
  pivot_longer(c(dNdS, dDdS), names_to = "type", values_to = "value") |>
  ggplot(aes(x = r_bin, y = value, color = type)) +
  geom_boxplot(aes(group = interaction(r_bin, type)))+
  geom_hline(yintercept = 1, linetype = "dashed")+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("Deviation from expected ratio")+
  scale_y_log10()+
  scale_color_manual(
    name = "",
    values = c("dNdS" = "firebrick", "dDdS" = "lightblue"),
    labels = c("dNdS" = "Non-synonymous / Synonymous", "dDdS" = "Deleterious non-synonymous / Synonymous")
    )+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0))
ggsave(outfile, width = 5.7, height = 5.7, units = "cm", dpi = "retina", ratio=3)


