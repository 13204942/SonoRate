import pandas as pd
import numpy as np
from scipy.stats import spearmanr, kruskal, mannwhitneyu
from statsmodels.stats.multitest import multipletests

CATE = 'hc18'  # hc18, estt
ROOT = f'stat_analysis/{CATE}/'

# ======================
# LOAD CSV
# ======================

df = pd.read_csv(f"{CATE}_rank.csv")

model_cols = ["M1", "M2", "M3", "M4", "M5"]

# ======================
# DOCTOR EXPERIENCE
# Update this mapping to your actual doctors
# ======================

doctor_experience = {
    "Doc_A": "senior",
    "Doc_B": "senior",
    "Doc_C": "junior",
    "Doc_D": "junior",
    "Doc_E": "non-expert",
    "Doc_F": "non-expert"
}

df["experience"] = df["doctor"].map(doctor_experience)

# ======================
# REFERENCE MODEL RANKING
# 5 = best, 1 = worst
# Update if needed
# ======================

reference_rank = {
    "M1": 1,
    "M2": 2,
    "M3": 3,
    "M4": 4,
    "M5": 5
}

# ======================
# COMPUTE SPEARMAN CORRELATION
# Spearman handles ties
# ======================

# def compute_spearman(row):
#     pred = row[model_cols].values.astype(float)
#     ref = np.array([reference_rank[m] for m in model_cols], dtype=float)
#     rho, p = spearmanr(pred, ref)
#     return pd.Series({"spearman": rho, "spearman_p": p})


def compute_spearman(row):
    pred = row[model_cols].values.astype(float)
    ref = np.array([reference_rank[m] for m in model_cols], dtype=float)

    # If pred is constant, Spearman is undefined
    if np.all(pred == pred[0]):
        return pd.Series({
            "spearman": np.nan,
            "spearman_p": np.nan,
            "is_constant_rating": True
        })

    rho, p = spearmanr(pred, ref)
    return pd.Series({
        "spearman": rho,
        "spearman_p": p,
        "is_constant_rating": False
    })
df[["spearman", "spearman_p", "is_constant_rating"]] = df.apply(compute_spearman, axis=1)
# df[["spearman", "spearman_p"]] = df.apply(compute_spearman, axis=1)

# ======================
# SUMMARY BY DOCTOR
# ======================

doctor_summary = (
    df.groupby(["doctor", "experience"])["spearman"]
    .agg(["count", "mean", "median", "std", "min", "max"])
    .reset_index()
)

print("\nSummary by doctor")
print(doctor_summary)

# ======================
# SUMMARY BY EXPERIENCE
# ======================

group_summary = (
    df.groupby("experience")["spearman"]
    .agg(["count", "mean", "median", "std", "min", "max"])
    .reset_index()
)

print("\nSummary by experience")
print(group_summary)

# ======================
# KRUSKAL-WALLIS TEST
# ======================

senior = df[df["experience"] == "senior"]["spearman"].dropna()
junior = df[df["experience"] == "junior"]["spearman"].dropna()
nonexpert = df[df["experience"] == "non-expert"]["spearman"].dropna()

kw_stat, kw_p = kruskal(senior, junior, nonexpert)

print("\nKruskal-Wallis test")
print(f"Statistic = {kw_stat:.4f}, p = {kw_p:.6f}")

# ======================
# PAIRWISE MANN-WHITNEY U TESTS
# ======================

pairs = [
    ("senior", "junior"),
    ("senior", "non-expert"),
    ("junior", "non-expert")
]

pairwise_results = []

for g1, g2 in pairs:
    x = df[df["experience"] == g1]["spearman"].dropna()
    y = df[df["experience"] == g2]["spearman"].dropna()
    stat, p = mannwhitneyu(x, y, alternative="two-sided")
    pairwise_results.append([g1, g2, stat, p])

pairwise_df = pd.DataFrame(
    pairwise_results,
    columns=["group1", "group2", "U_stat", "p_raw"]
)

reject, p_corr, _, _ = multipletests(pairwise_df["p_raw"], method="bonferroni")
pairwise_df["p_bonferroni"] = p_corr
pairwise_df["significant"] = reject

print("\nPairwise Mann-Whitney U tests")
print(pairwise_df)

# ======================
# TOP-1 ANALYSIS WITH TIES
# 5 = best, so use max()
# ======================

def get_top_models(row):
    ranks = row[model_cols]
    max_rank = ranks.max()
    top_models = [m for m in model_cols if row[m] == max_rank]
    return top_models

df["top_models"] = df.apply(get_top_models, axis=1)

print("\nExample top models")
print(df[["img", "doctor", "top_models"]].head())

# ======================
# TOP-1 INCLUSIVE COUNTS
# Each tied top model gets 1 count
# Example: [M3, M4, M5] -> each gets +1
# ======================

top1_inclusive_records = []

for _, row in df.iterrows():
    for m in row["top_models"]:
        top1_inclusive_records.append({
            "img": row["img"],
            "doctor": row["doctor"],
            "experience": row["experience"],
            "top_model": m
        })

top1_inclusive_df = pd.DataFrame(top1_inclusive_records)

top1_overall = (
    top1_inclusive_df["top_model"]
    .value_counts()
    .sort_index()
    .reset_index()
)
top1_overall.columns = ["model", "count"]

top1_overall["percentage"] = 100 * top1_overall["count"] / top1_overall["count"].sum()

print("\nTop-1 inclusive counts overall")
print(top1_overall)

top1_by_group = (
    top1_inclusive_df.groupby(["experience", "top_model"])
    .size()
    .reset_index(name="count")
)

top1_by_group["percentage"] = (
    top1_by_group.groupby("experience")["count"]
    .transform(lambda x: 100 * x / x.sum())
)

print("\nTop-1 inclusive counts by experience")
print(top1_by_group)

# ======================
# OPTIONAL: FRACTIONAL TOP-1 COUNTS
# Example: [M3, M4, M5] -> each gets 1/3
# This avoids one row contributing >1 total count
# ======================

top1_fractional_records = []

for _, row in df.iterrows():
    top_models = row["top_models"]
    w = 1.0 / len(top_models)
    for m in top_models:
        top1_fractional_records.append({
            "img": row["img"],
            "doctor": row["doctor"],
            "experience": row["experience"],
            "top_model": m,
            "weight": w
        })

top1_fractional_df = pd.DataFrame(top1_fractional_records)

top1_fractional_overall = (
    top1_fractional_df.groupby("top_model")["weight"]
    .sum()
    .reset_index()
    .rename(columns={"top_model": "model", "weight": "weighted_count"})
)

top1_fractional_overall["percentage"] = (
    100 * top1_fractional_overall["weighted_count"] / top1_fractional_overall["weighted_count"].sum()
)

print("\nTop-1 fractional counts overall")
print(top1_fractional_overall)

top1_fractional_by_group = (
    top1_fractional_df.groupby(["experience", "top_model"])["weight"]
    .sum()
    .reset_index()
    .rename(columns={"weight": "weighted_count"})
)

top1_fractional_by_group["percentage"] = (
    top1_fractional_by_group.groupby("experience")["weighted_count"]
    .transform(lambda x: 100 * x / x.sum())
)

print("\nTop-1 fractional counts by experience")
print(top1_fractional_by_group)

# ======================
# SAVE RESULTS
# ======================

df.to_csv(f"{ROOT}spearman_results.csv", index=False)
doctor_summary.to_csv(f"{ROOT}doctor_summary.csv", index=False)
group_summary.to_csv(f"{ROOT}experience_summary.csv", index=False)
pairwise_df.to_csv(f"{ROOT}pairwise_tests.csv", index=False)
top1_inclusive_df.to_csv(f"{ROOT}top1_inclusive_records.csv", index=False)
top1_overall.to_csv(f"{ROOT}top1_inclusive_overall.csv", index=False)
top1_by_group.to_csv(f"{ROOT}top1_inclusive_by_group.csv", index=False)
top1_fractional_df.to_csv(f"{ROOT}top1_fractional_records.csv", index=False)
top1_fractional_overall.to_csv(f"{ROOT}top1_fractional_overall.csv", index=False)
top1_fractional_by_group.to_csv(f"{ROOT}top1_fractional_by_group.csv", index=False)

print("\nAll result files saved.")