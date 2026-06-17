import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Example:
# corr_matrix index/columns = ["Senior clinicians", "Junior clinicians", "Non-experts"]

CATE = 'hc18'  # hc18, estt
ROOT = f'stat_analysis/{CATE}'

rename_map = {
    "senior": "Expert\n(Obstetrics)",
    "junior": "Generalist\n(Ultrasound)",
    "non-expert": "Non-expert"
}

# Define your colors (low → high)
colors = ["#fdfefa", "#a9dcf5", "#7c8bee"]  # light →
# medium →
# dark
custom_cmap = LinearSegmentedColormap.from_list(
    "custom_blue",
    colors
)

# ----------------------------
# 1. Load dataframe
# ----------------------------
df = pd.read_csv(f"{ROOT}/spearman_results.csv")
df = df[df['doctor'] != "AI"]

df_clean = df[["img", "experience", "spearman"]].copy()
df_clean = df_clean.dropna(subset=["spearman"])
df_clean["img"] = df_clean["img"].astype(str).str.strip()
df_clean["experience"] = df_clean["experience"].astype(str).str.strip()
df_clean["spearman"] = pd.to_numeric(df_clean["spearman"], errors="coerce")

# average Spearman per image per group
group_img_df = (
    df_clean.groupby(["img", "experience"])["spearman"]
    .mean()
    .reset_index()
)

pivot = group_img_df.pivot(index="img", columns="experience", values="spearman")
pivot = pivot.dropna()
print("Number of images used for group correlation:", len(pivot))
print(pivot.head())

# groups = pivot.columns
groups = pivot.columns.tolist()

corr_matrix = pd.DataFrame(index=groups, columns=groups, dtype=float)
pval_matrix = pd.DataFrame(index=groups, columns=groups, dtype=float)

def p_to_star(p):
    if pd.isna(p):
        return ""
    elif p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return ""

for g1 in groups:
    for g2 in groups:
        rho, p = spearmanr(pivot[g1], pivot[g2])
        corr_matrix.loc[g1, g2] = rho
        pval_matrix.loc[g1, g2] = p

# Create annotation with rho + p-value
annot = corr_matrix.copy().astype(str)

for i in range(len(groups)):
    for j in range(len(groups)):
        rho = corr_matrix.iloc[i, j]
        p = pval_matrix.iloc[i, j]
        annot.iloc[i, j] = f"{rho:.2f}\n{p_to_star(p)}"

corr_matrix = corr_matrix.rename(index=rename_map, columns=rename_map)
pval_matrix = pval_matrix.rename(index=rename_map, columns=rename_map)

# Convert matrix to long format
plot_df = corr_matrix.stack().reset_index()
plot_df.columns = ["group_y", "group_x", "corr"]

# Optional: add p-values
pval_df = pval_matrix.stack().reset_index()
pval_df.columns = ["group_y", "group_x", "pval"]

plot_df = plot_df.merge(pval_df, on=["group_y", "group_x"])

# Preserve displayed order
x_labels = list(corr_matrix.columns)
y_labels = list(corr_matrix.index)

x_map = {label: i for i, label in enumerate(x_labels)}
y_map = {label: i for i, label in enumerate(y_labels)}

fig, ax = plt.subplots(figsize=(5, 3.5))

# Draw lower triangle heatmap only
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

sns.heatmap(
    corr_matrix.astype(float),
    mask=mask,
    annot=annot,
    fmt="",
    cmap=custom_cmap,
    vmin=0,
    vmax=1,
    linewidths=2,
    linecolor="white",
    cbar_kws={"label": "Spearman correlation"},
    annot_kws={"size": 13, "color": "black"},
    ax=ax
)

# plt.title("Agreement between experience groups")
plt.xticks(fontsize=11)
plt.tight_layout()
plt.show()
