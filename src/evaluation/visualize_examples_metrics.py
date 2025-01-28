import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# File paths for the two CSV files
csv_path_2 = "~/current_main_1.csv"  # First CSV file
csv_path_1 = "~/functional_anal.csv"  # Second CSV file

# Specify the order of the metrics
metrics_order = [
    # Group 1: Simple RDD Transformations
    "avg_individual_metrics.map",
    "avg_individual_metrics.mapPartitions",
    "avg_individual_metrics.flatMap",
    "avg_individual_metrics.sparkContext",
    "avg_individual_metrics.quinnRddSparkContext",
    # Group 2: Combined RDD Operations
    "avg_individual_metrics.filterReduce",
    "avg_individual_metrics.mapReduce",
    "avg_individual_metrics.sumSquares",
    "avg_individual_metrics.sumNumbers",
    "avg_individual_metrics.pi",
    # Group 3: Advanced RDD Operations
    "avg_individual_metrics.mixedRDD",
    "avg_individual_metrics.frequentWords",
    "avg_individual_metrics.frequentLetters",
    # Group 4: DataFrame and RDD Interplay
    "avg_individual_metrics.readJson",
    "avg_individual_metrics.readJsonCsv",
    # Group 5: Specialized Use Cases
    "avg_individual_metrics.prefixSpan",
    "avg_individual_metrics.sparkJvmOrigin",
    "avg_individual_metrics.probability",
]

iteration_solved_order = [
    # Group 1: Simple RDD Transformations
    "iteration_solved.map",
    "iteration_solved.mapPartitions",
    "iteration_solved.flatMap",
    "iteration_solved.sparkContext",
    "iteration_solved.quinnRddSparkContext",
    # Group 2: Combined RDD Operations
    "iteration_solved.filterReduce",
    "iteration_solved.mapReduce",
    "iteration_solved.sumSquares",
    "iteration_solved.sumNumbers",
    "iteration_solved.pi",
    # Group 3: Advanced RDD Operations
    "iteration_solved.mixedRDD",
    "iteration_solved.frequentWords",
    "iteration_solved.frequentLetters",
    # Group 4: DataFrame and RDD Interplay
    "iteration_solved.readJson",
    "iteration_solved.readJsonCsv",
    # Group 5: Specialized Use Cases
    "iteration_solved.prefixSpan",
    "iteration_solved.sparkJvmOrigin",
    "iteration_solved.probability",
]


# Function to create and save heatmaps
# Function to create and save heatmaps
def create_and_save_heatmap(data, columns, title, filename):
    # Filter and reorder data
    code_runs = data[data["Name"].str.contains("code")]
    api_ref_runs = data[data["Name"].str.contains("api_ref")]

    # Concatenate filtered data
    data = pd.concat([code_runs, api_ref_runs])
    if "avg_score" in data:
        data["avg_score"] = data["avg_score"] / 18.0
    data_filtered = data[columns]
    run_names = data["Name"]  # Use the "Name" column for labels
    print(run_names)
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        data_filtered,
        annot=False,
        cmap="viridis" if "avg" in columns[0] else "coolwarm",
    )

    plt.title(title)
    plt.xlabel("Metrics")
    plt.ylabel("Run Names")
    plt.xticks(ticks=range(len(columns)), labels=columns, rotation=45, ha="right")
    plt.yticks(ticks=range(len(run_names)), labels=run_names, rotation=0)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Heatmap saved as {filename}")


# Load the first CSV and save its heatmaps
data1 = pd.read_csv(csv_path_1)
create_and_save_heatmap(
    data1,
    metrics_order,
    "Heatmap of avg_individual_metrics (CSV 1)",
    "heatmap_avg_metrics_csv1.png",
)
create_and_save_heatmap(
    data1,
    iteration_solved_order,
    "Heatmap of iteration_solved (CSV 1)",
    "heatmap_iteration_solved_csv1.png",
)

# Load the second CSV
data2 = pd.read_csv(csv_path_2)

# Combine the two datasets vertically (concatenate)
combined_data = pd.concat([data1, data2], ignore_index=True)

# Save heatmaps for the combined data
create_and_save_heatmap(
    combined_data,
    metrics_order,
    "Heatmap of avg_individual_metrics (Combined)",
    "heatmap_avg_metrics_combined.png",
)
create_and_save_heatmap(
    combined_data,
    iteration_solved_order,
    "Heatmap of iteration_solved (Combined)",
    "heatmap_iteration_solved_combined.png",
)
