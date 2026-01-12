"""
Pandas Examples - Data manipulation and visualization
Demonstrates pandas DataFrames and built-in plotting capabilities
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Use non-interactive backend for saving plots
plt.switch_backend('Agg')

# Create output directory for plots
OUTPUT_DIR = Path(__file__).parent / "output" / "pandas"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_sample_dataframe():
    """Create a sample DataFrame for demonstrations"""
    np.random.seed(42)
    data = {
        'Date': pd.date_range('2024-01-01', periods=100),
        'Sales': np.random.randint(100, 1000, 100),
        'Temperature': np.random.uniform(15, 35, 100),
        'Category': np.random.choice(['A', 'B', 'C', 'D'], 100),
        'Revenue': np.random.uniform(1000, 5000, 100)
    }
    return pd.DataFrame(data)


def dataframe_basics():
    """Demonstrate basic DataFrame operations"""
    df = create_sample_dataframe()

    print("DataFrame Head:")
    print(df.head(10))
    print("\nDataFrame Info:")
    print(df.info())
    print("\nDescriptive Statistics:")
    print(df.describe())
    print("\nValue Counts for Category:")
    print(df['Category'].value_counts())


def pandas_line_plot():
    """Create line plots using pandas"""
    df = create_sample_dataframe()

    # Simple line plot
    plt.figure(figsize=(12, 6))
    df.set_index('Date')['Sales'].plot(kind='line', title='Sales Over Time', color='blue')
    plt.ylabel('Sales')
    plt.xlabel('Date')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '01_line_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_bar_plot():
    """Create bar plots using pandas"""
    df = create_sample_dataframe()

    # Group by category and plot
    category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    category_sales.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Total Sales by Category')
    plt.ylabel('Total Sales')
    plt.xlabel('Category')
    plt.xticks(rotation=0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '02_bar_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_histogram():
    """Create histograms using pandas"""
    df = create_sample_dataframe()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Distribution Analysis', fontsize=16)

    # Sales distribution
    df['Sales'].plot(kind='hist', bins=20, ax=axes[0], color='lightcoral', edgecolor='black')
    axes[0].set_title('Sales Distribution')
    axes[0].set_xlabel('Sales')
    axes[0].set_ylabel('Frequency')
    axes[0].grid(True, alpha=0.3)

    # Temperature distribution
    df['Temperature'].plot(kind='hist', bins=20, ax=axes[1], color='lightgreen', edgecolor='black')
    axes[1].set_title('Temperature Distribution')
    axes[1].set_xlabel('Temperature (°C)')
    axes[1].set_ylabel('Frequency')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '03_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_box_plot():
    """Create box plots using pandas"""
    df = create_sample_dataframe()

    plt.figure(figsize=(10, 6))
    df.boxplot(column='Sales', by='Category', figsize=(10, 6))
    plt.suptitle('')  # Remove default title
    plt.title('Sales Distribution by Category')
    plt.xlabel('Category')
    plt.ylabel('Sales')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '04_box_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_scatter_plot():
    """Create scatter plots using pandas"""
    df = create_sample_dataframe()

    plt.figure(figsize=(10, 6))
    df.plot(kind='scatter', x='Temperature', y='Sales', c='Revenue',
            cmap='viridis', s=50, alpha=0.6, colorbar=True, figsize=(10, 6))
    plt.title('Sales vs Temperature (colored by Revenue)')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Sales')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '05_scatter_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_area_plot():
    """Create area plots using pandas"""
    # Create data for stacked area chart
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=50)
    df = pd.DataFrame({
        'Product A': np.random.randint(50, 200, 50),
        'Product B': np.random.randint(50, 200, 50),
        'Product C': np.random.randint(50, 200, 50),
        'Product D': np.random.randint(50, 200, 50)
    }, index=dates)

    plt.figure(figsize=(12, 6))
    df.plot(kind='area', stacked=True, alpha=0.6, figsize=(12, 6))
    plt.title('Product Sales Over Time (Stacked Area)')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend(loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '06_area_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_pivot_table_visualization():
    """Create pivot tables and visualize them"""
    df = create_sample_dataframe()

    # Add month column
    df['Month'] = df['Date'].dt.month

    # Create pivot table
    pivot = df.pivot_table(values='Sales', index='Month', columns='Category', aggfunc='mean')

    print("\nPivot Table - Average Sales by Month and Category:")
    print(pivot)

    # Visualize pivot table
    plt.figure(figsize=(12, 6))
    pivot.plot(kind='bar', figsize=(12, 6))
    plt.title('Average Sales by Month and Category')
    plt.xlabel('Month')
    plt.ylabel('Average Sales')
    plt.legend(title='Category')
    plt.xticks(rotation=0)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '07_pivot_table.png', dpi=300, bbox_inches='tight')
    plt.close()


def pandas_correlation_heatmap():
    """Create a correlation matrix visualization"""
    df = create_sample_dataframe()

    # Select numerical columns
    numerical_cols = df.select_dtypes(include=[np.number])
    correlation_matrix = numerical_cols.corr()

    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Visualize using matplotlib
    plt.figure(figsize=(8, 6))
    plt.imshow(correlation_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
    plt.colorbar(label='Correlation Coefficient')
    plt.xticks(range(len(correlation_matrix.columns)), correlation_matrix.columns, rotation=45)
    plt.yticks(range(len(correlation_matrix.columns)), correlation_matrix.columns)
    plt.title('Correlation Heatmap')

    # Add correlation values as text
    for i in range(len(correlation_matrix.columns)):
        for j in range(len(correlation_matrix.columns)):
            plt.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                    ha='center', va='center', color='black')

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '08_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()


def run_all_examples():
    """Run all pandas examples"""
    print("=== Pandas Examples ===\n")
    print(f"Saving plots to: {OUTPUT_DIR}\n")

    print("1. DataFrame Basics")
    dataframe_basics()

    print("\n2. Line Plot")
    pandas_line_plot()
    print(f"   Saved: 01_line_plot.png")

    print("\n3. Bar Plot")
    pandas_bar_plot()
    print(f"   Saved: 02_bar_plot.png")

    print("\n4. Histogram")
    pandas_histogram()
    print(f"   Saved: 03_histogram.png")

    print("\n5. Box Plot")
    pandas_box_plot()
    print(f"   Saved: 04_box_plot.png")

    print("\n6. Scatter Plot")
    pandas_scatter_plot()
    print(f"   Saved: 05_scatter_plot.png")

    print("\n7. Area Plot")
    pandas_area_plot()
    print(f"   Saved: 06_area_plot.png")

    print("\n8. Pivot Table Visualization")
    pandas_pivot_table_visualization()
    print(f"   Saved: 07_pivot_table.png")

    print("\n9. Correlation Heatmap")
    pandas_correlation_heatmap()
    print(f"   Saved: 08_correlation_heatmap.png")

    print(f"\nAll plots saved successfully to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_all_examples()
