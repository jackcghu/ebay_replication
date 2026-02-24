#!/usr/bin/env python3
# code/did_estimation.py
# Compute DID estimate and output LaTeX table

import pandas as pd
import numpy as np

# Load precomputed pivot tables
treated = pd.read_csv('temp/treated_pivot.csv', index_col=0)
untreated = pd.read_csv('temp/untreated_pivot.csv', index_col=0)

# Compute pre-post differences
treated['r'] = treated['log_revenue_post'] - treated['log_revenue_pre']
untreated['r'] = untreated['log_revenue_post'] - untreated['log_revenue_pre']

# Means and standard errors
mean_treated = treated['r'].mean()
mean_control = untreated['r'].mean()
var_treated = treated['r'].var(ddof=1)
var_control = untreated['r'].var(ddof=1)
n_treated = treated.shape[0]
n_control = untreated.shape[0]

SE = np.sqrt(var_treated/n_treated + var_control/n_control)
did_estimate = mean_treated - mean_control

# LaTeX table
latex_table = f"""
\\begin{{tabular}}{{lcc}}
\\hline
Group & Mean Log Difference & Standard Error \\\\
\\hline
Treated & {mean_treated:.4f} & {np.sqrt(var_treated/n_treated):.4f} \\\\
Control & {mean_control:.4f} & {np.sqrt(var_control/n_control):.4f} \\\\
DID Estimate & {did_estimate:.4f} & {SE:.4f} \\\\
\\hline
\\end{{tabular}}
"""

# Write table to file
with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex_table)

print("DID table written to output/tables/did_table.tex")
