# DID Analysis Script
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
#!/usr/bin/env python3
# code/did_analysis.py
# Difference-in-Differences estimation for eBay Paid Search experiment

import pandas as pd
import numpy as np

# ---------------------------------------------------
# Step 1 — Load preprocessed pivot tables
# ---------------------------------------------------

treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# ---------------------------------------------------
# Step 2 — Compute DID estimate
# ---------------------------------------------------

# Means
r1_bar = treated_pivot['log_revenue_diff'].mean()
r0_bar = untreated_pivot['log_revenue_diff'].mean()

# DID estimate
gamma_hat = r1_bar - r0_bar

# Sample variances (pandas var() uses ddof=1 by default)
var_treated = treated_pivot['log_revenue_diff'].var()
var_untreated = untreated_pivot['log_revenue_diff'].var()

# Sample sizes
n_treated = treated_pivot.shape[0]
n_untreated = untreated_pivot.shape[0]

# Standard error
se = np.sqrt(var_treated / n_treated + var_untreated / n_untreated)

# 95% Confidence Interval
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# ---------------------------------------------------
# Step 3 — Print results to console
# ---------------------------------------------------

print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# ---------------------------------------------------
# Step 4 — Output LaTeX table
# ---------------------------------------------------

latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex)

print("\nLaTeX table written to output/tables/did_table.tex")
