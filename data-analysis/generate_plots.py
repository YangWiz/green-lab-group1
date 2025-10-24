import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load the dataset
df = pd.read_csv("/Users/nisha/Downloads/run_table.csv")

# Define metrics and units
metrics = [
    ('energy_consumption', 'Energy Consumption (J)'),
    ('execution_time', 'Execution Time (s)')
]

# Create subplots
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(18, 12), sharex=True)
plt.subplots_adjust(hspace=0.3)

# Soft pastel-like palette (elegant and readable)
palette = {
    'pure_python': '#F4A582',  # warm peach
    'cython': '#92C5DE',       # soft sky blue
    'swig': '#A6D854'          # fresh light green
}

for i, (col_name, title) in enumerate(metrics):
    sns.violinplot(
        x='_benchmark',
        y=col_name,
        hue='_compiler',
        data=df,
        ax=axes[i],
        palette=palette,
        inner='quartile',
        density_norm='width',   # safe for newer seaborn
        bw_adjust=0.4,          # controls smoothness
        linewidth=1,
        cut=0,
        alpha=0.8               # gentle transparency
    )

    # Clean up labels and title
    axes[i].set_title(f'Distribution of {title}', fontsize=16, pad=10)
    axes[i].set_xlabel('Benchmark Task', fontsize=13)
    axes[i].set_ylabel(title, fontsize=13)

    # Legend cleanup
    handles, labels = axes[i].get_legend_handles_labels()
    new_labels = [label.replace('pure_python', 'Pure Python').capitalize() for label in labels]
    axes[i].legend(handles, new_labels, title='Compiler', loc='upper right', fontsize=10)

    # Rotate x-axis labels for better readability
    axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/Users/nisha/Downloads/distribution_plots_energy_time_light.png', dpi=300)
plt.show()
