from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "reports" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid", context="talk")

metrics = pd.read_csv(PROCESSED / "response_level_metrics.csv")
presence = pd.read_csv(PROCESSED / "language_presence_statistics.csv")
scores = pd.read_csv(PROCESSED / "semantic_similarity_scores.csv")
metric_columns = [
    "cosine_similarity", "bertscore_precision", "bertscore_recall", "bertscore_f1",
    "rougeL_precision", "rougeL_recall", "rougeL_f1",
]

# Preprocessing: length and lexical diversity.
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(data=metrics, x="response_type", y="word_count", ax=axes[0], palette="Set2", hue="response_type", legend=False)
axes[0].set_title("Response length")
axes[0].set_xlabel("")
axes[0].set_ylabel("Words")
sns.boxplot(data=metrics, x="response_type", y="lexical_diversity", ax=axes[1], palette="Set2", hue="response_type", legend=False)
axes[1].set_title("Lexical diversity")
axes[1].set_xlabel("")
axes[1].set_ylabel("Unique words / words")
fig.tight_layout()
fig.savefig(FIGURES / "preprocessing_distributions.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Preprocessing: language indicators.
presence_plot = presence.copy()
presence_plot["metric"] = presence_plot["metric"].str.replace("has_", "", regex=False).str.replace("mentions_", "", regex=False).str.replace("_", " ")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=presence_plot, x="percent", y="metric", hue="response_type", ax=ax, palette="Set1")
ax.set_title("Language and lifestyle-topic presence")
ax.set_xlabel("Responses containing signal (%)")
ax.set_ylabel("")
ax.legend(title="Response type", loc="lower right")
fig.tight_layout()
fig.savefig(FIGURES / "language_presence.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Semantic metrics: distributions.
long_scores = scores.melt(id_vars=["Question Category"], value_vars=metric_columns, var_name="metric", value_name="score")
fig, ax = plt.subplots(figsize=(15, 6))
sns.boxplot(data=long_scores, x="metric", y="score", color="#f4a261", ax=ax)
ax.set_title("Semantic and lexical-overlap score distributions")
ax.set_xlabel("")
ax.set_ylabel("Score")
ax.tick_params(axis="x", rotation=35)
fig.tight_layout()
fig.savefig(FIGURES / "semantic_metric_distributions.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Semantic metrics: category means.
category_means = scores.groupby("Question Category")[metric_columns].mean().sort_values("cosine_similarity", ascending=False)
fig, ax = plt.subplots(figsize=(14, 6))
category_means.plot(kind="bar", ax=ax, colormap="viridis")
ax.set_title("Mean evaluation scores by question category")
ax.set_xlabel("")
ax.set_ylabel("Mean score")
ax.tick_params(axis="x", rotation=25)
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
fig.tight_layout()
fig.savefig(FIGURES / "semantic_category_means.png", dpi=180, bbox_inches="tight")
plt.close(fig)

# Semantic metrics: correlation.
fig, ax = plt.subplots(figsize=(11, 8))
sns.heatmap(scores[metric_columns].corr(), annot=True, fmt=".2f", cmap="vlag", center=0, square=True, ax=ax)
ax.set_title("Correlation among evaluation metrics")
fig.tight_layout()
fig.savefig(FIGURES / "semantic_metric_correlations.png", dpi=180, bbox_inches="tight")
plt.close(fig)

print(f"Generated {len(list(FIGURES.glob('*.png')))} figures in {FIGURES}")
