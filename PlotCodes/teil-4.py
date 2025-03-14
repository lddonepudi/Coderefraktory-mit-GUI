import matplotlib.pyplot as plt
import numpy as np
import json
import os
import pandas as pd

# Define directories
json_dir = "JSONData"
csv_dir = "CSVData"
xlsx_dir = "XLSXData"

# Create directories if they don't exist
os.makedirs(json_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(xlsx_dir, exist_ok=True)

# Define category names
category_names = ['Ja', 'Nein, ich benötige keine Stifterkennung', 'Nein, ich hätte gerne ein Gerät mit Stifterkennung', 
                  'Nein, ich weiß nicht ob ich ein Gerät mit Stifterkennung besitze'][::-1]

# Define results
results = {"results": [5, 12, 3, 2][::-1]}

# Save results to JSONData
json_path = os.path.join(json_dir, "results-teil-4.json")
with open(json_path, "w") as json_file:
    json.dump(results, json_file, indent=4)

# Save results to CSVData
csv_path = os.path.join(csv_dir, "results-teil-4.csv")
df = pd.DataFrame({"Category": category_names, "Values": results["results"]})
df.to_csv(csv_path, index=False)

# Save results to XLSXData
xlsx_path = os.path.join(xlsx_dir, "results-teil-4.xlsx")
df.to_excel(xlsx_path, index=False)

def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    # Extract the results and category names
    data = np.array(list(results.values()))

    category_colors = plt.get_cmap('RdYlGn_r')(
        np.linspace(0.15, 0.85, data.shape[1]))[::-1]
    
    # Calculate the total sum of values to compute percentages
    total = np.sum(data)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(9.4, 5))
    ax.set_title("Gerät mit Stifterkennung in Mechanik", pad=30)  # Add padding for the title

    # Define bar height and y positions for the bars
    bar_height = 0.5
    y_pos = np.arange(len(category_names))

    # Plot horizontal bars with color mapping
    bars = ax.barh(y_pos, data[0], height=bar_height, label='Results', color=category_colors)

    # Set labels and ticks
    ax.set_xlabel('Anzahl')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(category_names)
    ax.set_xticks([0, 2, 4, 6, 8, 10])

    # Display absolute and percentage values inside the bars
    for i, bar in enumerate(bars):
        absolute_value = bar.get_width()
        percentage = (absolute_value / total) * 100 if total > 0 else 0  # Prevent division by zero

        # Adjust x position for the last bar (if value is 0, move it slightly to the right)
        if absolute_value == 0:
            x_position = 0.1  # Small indent to make it visible
            ha_value = 'left'  # Align left so it's readable
        else:
            x_position = absolute_value / 2
            ha_value = 'center'

        # Display the absolute value and percentage
        ax.text(x_position, bar.get_y() + bar.get_height() / 2,
                f'{absolute_value} \n{percentage:.0f}%', va='center', ha=ha_value, fontsize=10, color='black')

    # Apply tight layout to ensure everything fits
    plt.tight_layout(pad=2.0)

    return fig, ax

# Run the function and generate the plot
survey(results, category_names)

# Save and display the plot
plot_path = os.path.join(csv_dir, "plot4.jpg")
plt.savefig(plot_path)
plt.show()
