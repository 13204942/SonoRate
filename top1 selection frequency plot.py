import pandas as pd
import matplotlib.pyplot as plt

# color website: https://huemint.com/gradient-5/#palette=d8e8f8-c8aade-98689d-654b89-0c0f71

CATE = 'hc18'  # hc18, estt
ROOT = f'stat_analysis/{CATE}/'

# =========================
# Load CSV
# =========================
df = pd.read_csv(f"{CATE}_rank.csv")

# Change this if you have 6 models
model_cols = ["M1", "M2", "M3", "M4", "M5"]
# model_cols = ["M1", "M2", "M3", "M4", "M5", "M6"]

# =========================
# Find tied top-1 models
# 5 = best, 1 = worst
# =========================
def get_top_models(row):
    scores = row[model_cols]
    max_score = scores.max()
    top_models = [m for m in model_cols if row[m] == max_score]
    return top_models

df["top_models"] = df.apply(get_top_models, axis=1)

# =========================
# Fractional top-1 counts
# Each image-rater pair contributes total weight = 1
# =========================
records = []

for _, row in df.iterrows():
    top_models = row["top_models"]
    weight = 1.0 / len(top_models)
    for m in top_models:
        records.append({
            "img": row["img"],
            "doctor": row["doctor"],
            "model": m,
            "weight": weight
        })

top1_frac_df = pd.DataFrame(records)

# Sum weights per model
top1_summary = (
    top1_frac_df.groupby("model")["weight"]
    .sum()
    .reindex(model_cols)
    .reset_index()
)

top1_summary.columns = ["model", "weighted_count"]
top1_summary["percentage"] = 100 * top1_summary["weighted_count"] / top1_summary["weighted_count"].sum()

print(top1_summary)

# =========================
# Plot bar chart
# =========================
plt.figure(figsize=(5, 3.5))

bars = plt.bar(
    top1_summary["model"],
    top1_summary["percentage"],
    color=["#d8e8f8", "#c8aade", "#98689d", "#654b89", "#0c0f71"],
    edgecolor="black"
)

# Add count + percentage labels
for bar, count, pct in zip(
        bars,
        top1_summary["weighted_count"],
        top1_summary["percentage"]):

    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.5,
        f"{count:.0f}\n({pct:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=13
    )

plt.xticks(fontsize=13)
plt.xlabel("Model")
plt.ylabel("Top-1 selection frequency (%)", fontsize=13)
# plt.title("Top-1 selection frequency across models")
plt.ylim(0, top1_summary["percentage"].max() + 9)

plt.tight_layout()
plt.savefig(f"{CATE}_fig1_top1_selection_frequency.png", dpi=300,
            bbox_inches="tight")
plt.savefig(f"{CATE}_fig1_top1_selection_frequency.pdf", bbox_inches="tight")
plt.show()
