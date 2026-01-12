"""
Matplotlib Examples - Basic plotting and visualization
Demonstrates fundamental plotting capabilities with matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Use non-interactive backend for saving plots
plt.switch_backend('Agg')

# Create output directory for plots
OUTPUT_DIR = Path(__file__).parent / "output" / "matplotlib"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def basic_line_plot():
    """Create a simple line plot"""
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='sin(x)', color='blue', linewidth=2)
    plt.title('Basic Line Plot - Sine Wave')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig(OUTPUT_DIR / '01_basic_line_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def multiple_plots():
    """Create multiple plots in the same figure"""
    x = np.linspace(0, 10, 100)

    plt.figure(figsize=(12, 6))
    plt.plot(x, np.sin(x), label='sin(x)', linewidth=2)
    plt.plot(x, np.cos(x), label='cos(x)', linewidth=2)
    plt.plot(x, np.sin(x) * np.cos(x), label='sin(x) * cos(x)',
             linewidth=2, linestyle='--')

    plt.title('Multiple Functions on Same Plot')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / '02_multiple_plots.png', dpi=300, bbox_inches='tight')
    plt.close()


def scatter_plot():
    """Create a scatter plot with random data"""
    np.random.seed(42)
    x = np.random.randn(100)
    y = 2 * x + np.random.randn(100) * 0.5
    colors = np.random.rand(100)
    sizes = np.random.randint(20, 200, 100)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
    plt.colorbar(scatter, label='Color value')
    plt.title('Scatter Plot with Color and Size Variation')
    plt.xlabel('X values')
    plt.ylabel('Y values')
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / '03_scatter_plot.png', dpi=300, bbox_inches='tight')
    plt.close()


def bar_chart():
    """Create a bar chart"""
    categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    values = [23, 45, 56, 78, 32]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom', fontsize=10)

    plt.title('Bar Chart Example')
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.grid(True, alpha=0.3, axis='y')
    plt.savefig(OUTPUT_DIR / '04_bar_chart.png', dpi=300, bbox_inches='tight')
    plt.close()


def histogram():
    """Create a histogram"""
    np.random.seed(42)
    data = np.random.normal(100, 15, 1000)

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.axvline(data.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {data.mean():.2f}')
    plt.title('Histogram - Normal Distribution')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / '05_histogram.png', dpi=300, bbox_inches='tight')
    plt.close()


def subplots_example():
    """Create multiple subplots in a grid"""
    x = np.linspace(0, 10, 100)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Multiple Subplots Example', fontsize=16)

    # Subplot 1: Line plot
    axes[0, 0].plot(x, np.sin(x), 'b-')
    axes[0, 0].set_title('Sine Wave')
    axes[0, 0].grid(True, alpha=0.3)

    # Subplot 2: Cosine plot
    axes[0, 1].plot(x, np.cos(x), 'r-')
    axes[0, 1].set_title('Cosine Wave')
    axes[0, 1].grid(True, alpha=0.3)

    # Subplot 3: Exponential
    axes[1, 0].plot(x, np.exp(x/5), 'g-')
    axes[1, 0].set_title('Exponential Growth')
    axes[1, 0].grid(True, alpha=0.3)

    # Subplot 4: Scatter
    axes[1, 1].scatter(np.random.randn(50), np.random.randn(50), alpha=0.6)
    axes[1, 1].set_title('Random Scatter')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / '06_subplots.png', dpi=300, bbox_inches='tight')
    plt.close()


def pie_chart():
    """Create a pie chart"""
    labels = ['Python', 'JavaScript', 'Java', 'C++', 'Go']
    sizes = [35, 25, 20, 15, 5]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    explode = (0.1, 0, 0, 0, 0)  # Explode the first slice

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Programming Languages Usage')
    plt.axis('equal')
    plt.savefig(OUTPUT_DIR / '07_pie_chart.png', dpi=300, bbox_inches='tight')
    plt.close()


def run_all_examples():
    """Run all matplotlib examples"""
    print("=== Matplotlib Examples ===\n")
    print(f"Saving plots to: {OUTPUT_DIR}\n")

    print("1. Basic Line Plot")
    basic_line_plot()
    print(f"   Saved: 01_basic_line_plot.png")

    print("\n2. Multiple Plots")
    multiple_plots()
    print(f"   Saved: 02_multiple_plots.png")

    print("\n3. Scatter Plot")
    scatter_plot()
    print(f"   Saved: 03_scatter_plot.png")

    print("\n4. Bar Chart")
    bar_chart()
    print(f"   Saved: 04_bar_chart.png")

    print("\n5. Histogram")
    histogram()
    print(f"   Saved: 05_histogram.png")

    print("\n6. Subplots Example")
    subplots_example()
    print(f"   Saved: 06_subplots.png")

    print("\n7. Pie Chart")
    pie_chart()
    print(f"   Saved: 07_pie_chart.png")

    print(f"\nAll plots saved successfully to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_all_examples()
