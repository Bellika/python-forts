"""
Seaborn Examples - Statistical data visualization
Demonstrates seaborn's high-level plotting interface and statistical visualizations
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

# Use non-interactive backend for saving plots
plt.switch_backend('Agg')

# Create output directory for plots
OUTPUT_DIR = Path(__file__).parent / "output" / "seaborn"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_sample_dataset():
    """Create a sample dataset for demonstrations"""
    np.random.seed(42)
    n = 200

    data = {
        'age': np.random.randint(18, 70, n),
        'income': np.random.normal(50000, 20000, n),
        'spending': np.random.normal(30000, 15000, n),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Other'], n),
        'satisfaction': np.random.randint(1, 6, n),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n),
        'experience_years': np.random.randint(0, 30, n)
    }

    df = pd.DataFrame(data)
    # Make spending correlate with income
    df['spending'] = df['income'] * 0.6 + np.random.normal(0, 5000, n)
    return df


def set_style():
    """Set seaborn style for all plots"""
    sns.set_theme(style="whitegrid")
    sns.set_palette("husl")


def scatter_plot_with_regression():
    """Create scatter plot with regression line"""
    df = create_sample_dataset()

    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='income', y='spending', scatter_kws={'alpha': 0.5})
    plt.title('Income vs Spending with Regression Line')
    plt.xlabel('Income ($)')
    plt.ylabel('Spending ($)')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '01_scatter_regression.png', dpi=300, bbox_inches='tight')
    plt.close()


def categorical_scatter_plot():
    """Create scatter plot with categories"""
    df = create_sample_dataset()

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x='income', y='spending', hue='category',
                   size='satisfaction', sizes=(50, 200), alpha=0.6)
    plt.title('Income vs Spending by Category and Satisfaction')
    plt.xlabel('Income ($)')
    plt.ylabel('Spending ($)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '02_categorical_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()


def distribution_plot():
    """Create distribution plots (histograms with KDE)"""
    df = create_sample_dataset()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Distribution Analysis with KDE', fontsize=16)

    # Income distribution
    sns.histplot(data=df, x='income', kde=True, ax=axes[0], color='skyblue')
    axes[0].set_title('Income Distribution')
    axes[0].set_xlabel('Income ($)')

    # Spending distribution
    sns.histplot(data=df, x='spending', kde=True, ax=axes[1], color='lightcoral')
    axes[1].set_title('Spending Distribution')
    axes[1].set_xlabel('Spending ($)')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '03_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()


def box_plot_comparison():
    """Create box plots for categorical comparison"""
    df = create_sample_dataset()

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='category', y='spending', hue='region')
    plt.title('Spending by Category and Region')
    plt.xlabel('Category')
    plt.ylabel('Spending ($)')
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '04_box_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def violin_plot():
    """Create violin plots showing distribution shape"""
    df = create_sample_dataset()

    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df, x='category', y='income', hue='region', split=False)
    plt.title('Income Distribution by Category and Region')
    plt.xlabel('Category')
    plt.ylabel('Income ($)')
    plt.legend(title='Region')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '05_violin_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def heatmap_correlation():
    """Create a correlation heatmap"""
    df = create_sample_dataset()

    # Select numerical columns
    numerical_cols = df.select_dtypes(include=[np.number])
    correlation_matrix = numerical_cols.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '06_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()


def pair_plot():
    """Create pair plot for multiple variables"""
    df = create_sample_dataset()

    # Select subset of columns for clarity
    subset_df = df[['income', 'spending', 'age', 'satisfaction', 'category']]

    g = sns.pairplot(subset_df, hue='category', diag_kind='kde', corner=True)
    g.fig.suptitle('Pair Plot - Relationships Between Variables', y=1.01)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '07_pair_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def count_plot():
    """Create count plot for categorical data"""
    df = create_sample_dataset()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Categorical Distribution', fontsize=16)

    # Category counts
    sns.countplot(data=df, x='category', ax=axes[0], palette='Set2')
    axes[0].set_title('Count by Category')
    axes[0].set_xlabel('Category')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)

    # Satisfaction counts by region
    sns.countplot(data=df, x='satisfaction', hue='region', ax=axes[1], palette='Set3')
    axes[1].set_title('Satisfaction Ratings by Region')
    axes[1].set_xlabel('Satisfaction (1-5)')
    axes[1].set_ylabel('Count')
    axes[1].legend(title='Region')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '08_count_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def bar_plot_with_ci():
    """Create bar plot with confidence intervals"""
    df = create_sample_dataset()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='category', y='spending', hue='region',
                errorbar='ci', errwidth=2)
    plt.title('Average Spending by Category and Region (with 95% CI)')
    plt.xlabel('Category')
    plt.ylabel('Average Spending ($)')
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '09_bar_plot_ci.png', dpi=300, bbox_inches='tight')
    plt.close()


def joint_plot():
    """Create joint plot with marginal distributions"""
    df = create_sample_dataset()

    joint = sns.jointplot(data=df, x='income', y='spending',
                         kind='scatter', hue='category', alpha=0.6)
    joint.fig.suptitle('Joint Distribution - Income vs Spending', y=1.02)
    joint.savefig(OUTPUT_DIR / '10_joint_plot.png', dpi=300, bbox_inches='tight')


def facet_grid_example():
    """Create multi-panel plots using FacetGrid"""
    df = create_sample_dataset()

    g = sns.FacetGrid(df, col='category', row='region', hue='category',
                     height=3, aspect=1.2)
    g.map(sns.scatterplot, 'income', 'spending', alpha=0.6)
    g.add_legend()
    g.fig.suptitle('Income vs Spending - Faceted by Category and Region', y=1.01)
    g.savefig(OUTPUT_DIR / '11_facet_grid.png', dpi=300, bbox_inches='tight')


def swarm_plot():
    """Create swarm plot showing individual data points"""
    df = create_sample_dataset()

    # Take a subset to avoid overplotting
    subset = df.sample(n=100, random_state=42)

    plt.figure(figsize=(12, 6))
    sns.swarmplot(data=subset, x='category', y='satisfaction',
                 hue='region', dodge=True, size=6)
    plt.title('Individual Satisfaction Ratings by Category and Region')
    plt.xlabel('Category')
    plt.ylabel('Satisfaction (1-5)')
    plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '12_swarm_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def line_plot_with_ci():
    """Create line plot with confidence interval"""
    # Create time series data
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100)
    categories = ['Product A', 'Product B', 'Product C']

    data = []
    for cat in categories:
        for i, date in enumerate(dates):
            value = 100 + i * 2 + np.random.normal(0, 10)
            data.append({'Date': date, 'Sales': value, 'Product': cat})

    df = pd.DataFrame(data)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='Date', y='Sales', hue='Product',
                errorbar='ci', linewidth=2.5)
    plt.title('Sales Trends Over Time (with 95% CI)')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend(title='Product')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '13_line_plot_ci.png', dpi=300, bbox_inches='tight')
    plt.close()


def run_all_examples():
    """Run all seaborn examples"""
    set_style()

    print("=== Seaborn Examples ===\n")
    print(f"Saving plots to: {OUTPUT_DIR}\n")

    print("1. Scatter Plot with Regression")
    scatter_plot_with_regression()
    print(f"   Saved: 01_scatter_regression.png")

    print("\n2. Categorical Scatter Plot")
    categorical_scatter_plot()
    print(f"   Saved: 02_categorical_scatter.png")

    print("\n3. Distribution Plot")
    distribution_plot()
    print(f"   Saved: 03_distribution.png")

    print("\n4. Box Plot Comparison")
    box_plot_comparison()
    print(f"   Saved: 04_box_plot.png")

    print("\n5. Violin Plot")
    violin_plot()
    print(f"   Saved: 05_violin_plot.png")

    print("\n6. Correlation Heatmap")
    heatmap_correlation()
    print(f"   Saved: 06_heatmap.png")

    print("\n7. Pair Plot")
    pair_plot()
    print(f"   Saved: 07_pair_plot.png")

    print("\n8. Count Plot")
    count_plot()
    print(f"   Saved: 08_count_plot.png")

    print("\n9. Bar Plot with Confidence Intervals")
    bar_plot_with_ci()
    print(f"   Saved: 09_bar_plot_ci.png")

    print("\n10. Joint Plot")
    joint_plot()
    print(f"   Saved: 10_joint_plot.png")

    print("\n11. Facet Grid")
    facet_grid_example()
    print(f"   Saved: 11_facet_grid.png")

    print("\n12. Swarm Plot")
    swarm_plot()
    print(f"   Saved: 12_swarm_plot.png")

    print("\n13. Line Plot with Confidence Intervals")
    line_plot_with_ci()
    print(f"   Saved: 13_line_plot_ci.png")

    print(f"\nAll plots saved successfully to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_all_examples()
