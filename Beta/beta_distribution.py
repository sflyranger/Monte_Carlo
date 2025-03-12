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

# --- SIMULATION ---

def a_beta_params(mean, std):
    """
    Function to calculate the alpha and beta parameters needed get the beta distribution
    Inputs:
    mean (float) - The mean of the data.
    std (float) - The standard deviation of the data.
    Returns:
    alpha (float): The calculated alpha needed for the beta distribution.
    beta (float): The calculated beta needed for the beta distribution.

    """
    variance = std**2
    k = mean * (1-mean)/variance-1
    alpha = mean * k
    beta = (1-mean) * k
    return alpha, beta

# Getting alpha and beta for the default rate and the lgd
alpha_d, beta_d = a_beta_params(mean_default_rate, std_default_rate)
alpha_l, beta_l = a_beta_params(mean_loss_given_default, std_lgd)

# Using a Beta distribution to more accurately reflect real world conditions.
default_rates = np.random.beta(alpha_d, beta_d, num_simulations)
lgd_rates = np.random.beta(alpha_l, beta_l, num_simulations)

# Calculating losses
total_losses = default_rates * lgd_rates * total_exposure


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

print("\n Summary of Monte Carlo Simulations - Beta Distribution")
for key, value in summary_stats.items():
    print(f"{key}: ${value:,.2f}")


# Plot Results
plt.figure(figsize = (10, 8))
plt.hist(total_losses, bins = 50, color="skyblue", edgecolor="black")
plt.axvline(n