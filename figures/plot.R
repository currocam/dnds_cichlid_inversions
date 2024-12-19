library(conflicted)
library(tidyverse)
library(patchwork)

# Settings
options(digits = 3)
options(pillar.sigfig = 3)
text_base_size   <- 16   # in pt
fig.width        <- 180  # in mm
fig.height       <- 125  # in mm
ggplot2::theme_set(
  cowplot::theme_cowplot(
    font_size = text_base_size, rel_small = 1,
    rel_tiny = 1, rel_large = 1
  )
)
ggplot_text_size <- text_base_size / ggplot2::.pt

# Load data
infiles <- c(
  "X = 100" = "~/Downloads/scenarios/high_x_sims.csv",
  "X = 2" = "~/Downloads/scenarios/low_x_sims.csv"
)

data <- infiles |>
  map(read_csv) |>
  bind_rows(.id = "scenario") |>
  dplyr::filter(scenario %in% c("X = 100", "X = 2"))


p1 <- data |>
  dplyr::filter(Synonymous>0) |>
  ggplot(aes(x = r_bin, y = dNdS, colour = scenario)) +
  geom_jitter(alpha = 0.02, height = 0)+
  geom_pointrange(
    data =  data |>
      group_by(r_bin, scenario) |>
      summarise(
        y = median(dNdS, na.rm = TRUE),
        ymin = quantile(dNdS, 0.25, na.rm = TRUE),
        ymax = quantile(dNdS, 0.75, na.rm = TRUE),
      ), position = position_dodge(width=0.05),
    aes(
      x = r_bin, y = y,
      ymin = ymin, ymax = ymax,
    ),
    size = 0.5,
  )+
  scale_y_log10() +
  geom_hline(yintercept = 1, linetype = "dashed")+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("dN/dS")+
  scale_colour_manual(
    name = "",
    values = c("X = 100" = "black", "X = 2" = "red"),
  )+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0)) +
  ggtitle("**A**")+
  theme(plot.title = ggtext::element_markdown())

# Simulation-based p-value
set.seed(1000)
sim_pvalue <- function(observed_dnds, n_sites, fraction_s, replicates=5000){
  S <- rbinom(replicates, n_sites, fraction_s)
  N <- n_sites - S
  dNdS <- N / S / ((1-fraction_s) / fraction_s) 
  mean(dNdS >= observed_dnds)
}

data2 <- data |>
  group_by(scenario, r_bin, SEED) |>
  summarise(
    n_sites = unique(Synonymous + `Non-synonymous`),
    fraction_s = unique(FRACTION_S),
    dNdS = unique(dNdS),
  ) |>
  rowwise() |>
  mutate(pvalue = sim_pvalue(dNdS, n_sites, fraction_s))

p2 <- data2 |>
  group_by(scenario, r_bin) |>
  summarise(
    below05 = mean(pvalue<0.05, na.rm = T),
    below01 = mean(pvalue<0.01, na.rm = T),
  ) |>
  ggplot(aes(x = r_bin, colour = scenario)) +
  geom_line(aes(y = below01, linetype = "p-value < 0.01"),linewidth=1)+
  geom_line(aes(y = below05, linetype = "p-value < 0.05"),linewidth=1)+
  theme_minimal()+
  xlab("Pearson correlation coefficient")+
  ylab("Fraction of simulations where we\n reject the null hypothesis")+
  scale_colour_manual(
    name = "",
    values = c("X = 100" = "black", "X = 2" = "red"),
  )+
  scale_linetype_manual(
    name = "",
    values = c("p-value < 0.01" = "dotted", "p-value < 0.05" = "solid"),
    # Change the order of the legend, so p.value < 0.01 goes after
    breaks = c("p-value < 0.05", "p-value < 0.01")
  )+
  theme(legend.position = "bottom")+
  theme(plot.margin = margin(0, 0, 0, 0))+
  ggtitle("**B**")+
  theme(plot.title = ggtext::element_markdown())

final <- p1 + p2


outfiles <- c(
  "fig_slim_s53.png", "fig_slim_s53.pdf", "fig_slim_s53.svg"
)

outfiles |>
  walk(\(x) ggsave(
    x, final,
    width = fig.width,
    height = fig.height,
    units = "mm",
    scale=1.4,
    dpi = "retina")
  )
