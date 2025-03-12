# Import needed packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the seed for reproducibility
np.random.seed(42)

# PARAMETERS
num_simulations = 10000 # The number of simulations to run
total_exposure = 100000000 # Total value of the loan portfolio
mean_default_rate = 0.05 # Using 5% as the default to start
std_default_rate = 0.01 # Standard deviation of default rate (1%)
mean_loss_given_default = 0.40 # 40% loss on the porfolio if it goes into default
std_lgd = 0.05 # Standard deviation of the loss (5%)

# Simulation

# Using normal as a baseline, I could use beta right now as a distribution but I'll just clip them afterwards.
default_rates = np.random.normal(mean_default_rate, std_default_rate, num_simulations)
loss_given_default_rates = np.random.normal(mean_loss_given_default, std_lgd, num_simulations)

# Clip to ensure between 0 and 1
default_rates = np.clip(default_rates, 0, 1)
loss_given_default_rates = np.clip(loss_given_default_rates, 0, 1)

# Calculating the total loss for each simulation
total_losses = default_rates * loss_given_default_rates * total_exposure



# Analysis and Results

summary_stats = {
    "Mean Loss": np.mean(total_losses), 
    "Median Loss": np.median(total_losses), 
    "95th percentile (VaR)": np.percentile(total_losses, 95), 
    "99th percentile (VaR)": np.percentile(total_losses, 99),
    "5th Percentile (VaR)": np.percentile(total_losses, 5), 
    "1st Percentile (VaR)": np.percentile(total_losses, 1), 
    "Max Loss": np.max(total_losses), 
    "Min Loss": np.min(total_losses) 
}


print("\n Summary of Monte Carlo Simulations - Normal w/ clipping")
for key, value in summary_stats.items():
    print(f"{key}: ${value:,.2f}")


# Plot Results
plt.figure(figsize = (10, 8))
plt.hist(total_losses, bins = 50, color="skyblue", edgecolor="black")
plt.axvline(np.percentile(total_losses, 1), color="g", linestyle="dashed", linewidth=2, label="1st Percentile")
plt.axvline(np.percentile(total_losses, 5), color="b", linestyle="dashed", linewidth=2, label="5th Percentile")
plt.axvline(np.percentile(total_losses, 95), color="orange", linestyle="dashed", linewidth=2, label="95th Perce