def plot_correlations(correlation_df):
    """
    Plots correlations for each metric and atom combination.
    :param correlation_df: DataFrame containing correlation results
    """
    for metric in correlation_df["Metric"].unique():
        metric_df = correlation_df[correlation_df["Metric"] == metric]
        plt.figure(figsize=(10, 6))
        for combination in ATOM_COMBINATIONS:
            comb_name = "_".join(combination)
            subset = metric_df[metric_df["Combination"] == combination]
            plt.plot(subset["File"], subset["Spearman"], label=f"Spearman {comb_name}")
            plt.plot(subset["File"], subset["Pearson"], linestyle="--", label=f"Pearson {comb_name}")
        plt.title(f"Correlations for {metric}")
        plt.xlabel("Native Structures")
        plt.ylabel("Correlation")
        plt.legend()
        plt.show()