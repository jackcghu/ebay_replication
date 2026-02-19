#!/usr/bin/env python3
# preprocess.py
# Preprocess eBay PaidSearch data and reproduce Figures 5.2 and 5.3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------
# Step 1 — Load and prepare the data
# ---------------------------------------------------

df = pd.read_csv('../input/PaidSearch.csv')

df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# ---------------------------------------------------
# Step 2 — Create treated and untreated pivot tables
# ---------------------------------------------------

treated = df[df['search_stays_on'] == 0]
untreated = df[df['search_stays_on'] == 1]

# Create pivot tables
treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

# Rename columns
treated_pivot = treated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

untreated_pivot = untreated_pivot.rename(columns={
    0: 'log_revenue_pre',
    1: 'log_revenue_post'
})

# Compute difference
treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] -
    treated_pivot['log_revenue_pre']
)

untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] -
    untreated_pivot['log_revenue_pre']
)

# Ensure temp directory exists
os.makedirs('../temp', exist_ok=True)

# Save pivot tables
treated_pivot.to_csv('../temp/treated_pivot.csv')
untreated_pivot.to_csv('../temp/untreated_pivot.csv')

# ---------------------------------------------------
# Step 3 — Print summary statistics
# ---------------------------------------------------

num_treated = treated['dma'].nunique()
num_untreated = untreated['dma'].nunique()
date_min = df['date'].min().date()
date_max = df['date'].max().date()

print(f"Treated DMAs: {num_treated}")
print(f"Untreated DMAs: {num_untreated}")
print(f"Date range: {date_min} to {date_max}")

# ---------------------------------------------------
# Step 4 — Reproduce Figure 5.2
# ---------------------------------------------------

avg_revenue = (
    df.groupby(['date', 'search_stays_on'])['revenue']
    .sum()
    .reset_index()
)

pivot_rev = avg_revenue.pivot(
    index='date',
    columns='search_stays_on',
    values='revenue'
)

plt.figure(figsize=(10, 6))

plt.plot(pivot_rev.index, pivot_rev[1],
         label='Control (search stays on)')
plt.plot(pivot_rev.index, pivot_rev[0],
         label='Treatment (search goes off)')

plt.axvline(pd.to_datetime('2012-05-22'),
            linestyle='--')

plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Figure 5.2: Average Revenue Over Time')
plt.legend()

os.makedirs('../output/figures', exist_ok=True)

plt.savefig('../output/figures/figure_5_2.png')
plt.close()

# ---------------------------------------------------
# Step 5 — Reproduce Figure 5.3
# ---------------------------------------------------

avg_log_rev = (
    df.groupby(['date', 'search_stays_on'])['log_revenue']
    .sum()
    .reset_index()
)

pivot_log = avg_log_rev.pivot(
    index='date',
    columns='search_stays_on',
    values='log_revenue'
)

pivot_log['log_diff'] = (
    pivot_log[1] - pivot_log[0]
)

plt.figure(figsize=(10, 6))

plt.plot(pivot_log.index, pivot_log['log_diff'])

plt.axvline(pd.to_datetime('2012-05-22'),
            linestyle='--')

plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Figure 5.3: Log Revenue Difference Over Time')

plt.savefig('../output/figures/figure_5_3.png')
plt.close()
