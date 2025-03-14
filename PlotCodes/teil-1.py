import matplotlib.pyplot as plt
import numpy as np
import json
import os
import pandas as pd

# Define directories
json_dir = "JSONData"
csv_dir = "CSVData"

# Create directories if they don't exist
os.makedirs(json_dir, exist_ok=True)
os.makedirs(csv_dir, exist_ok=True)

# Define category names
category_names = ["F1 und F2", "Fach 1", "Fach 2"]

# Define results
results = {"results": [24, 9, 4]}

# Save results to JSON file
json_path = os.path.join(json_dir, "results.json")
with open(json_path, "w") as json_file:
    json.dump(results, json_file, indent=4)

# Save results to another JSON file named results-teil-1.json
json_path_teil = os.path.join(json_dir, "results-teil-1.json")
with open(json_path_teil, "w") as json_file:
    json.dump(results, json_file, indent=4)

# Save results to CSV
csv_path = os.path.join(csv_dir, "results.csv")
df = pd.DataFrame({"Category": category_names, "Values": results["results"]})
df.to_csv(csv_path, index=False)

# Function to load results from JSON
def load_results_from_json(filename):
    with open(filename, "r") as json_file:
        return json.load(json_file)

# Load results
loaded_results = load_results_from_json(json_path)

def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
    category_names : list of str
        The category labels.
    """
    # Extract the results and category names
    data = np.array(list(results.values()))
    category_colors = plt.get_cmap('RdYlGn_r')(
        np.linspace(0.15, 0.85, data.shape[1]))[::-1]  # Get correct color list
    
    # Calculate the total sum of values to compute percentages
    total = np.sum(data)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(9.4, 5))
    ax.set_title("Fächer", pad=30)  # Add padding for the title

    # Define bar height and y positions for the bars
    bar_height = 0.5
    y_pos = np.arange(len(category_names))

    # Plot horizontal bars with properly assigned colors
    bars = ax.barh(y_pos, data[0], height=bar_height, label='Results', color=category_colors)

    # Set labels and ticks
    ax.set_xlabel('Anzahl')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(category_names)
    ax.set_xticks([0, 5, 10, 15, 20, 25])

    # Display absolute and percentage values inside the bars
    for i, bar in enumerate(bars):
        absolute_value = bar.get_width()
        percentage = (absolute_value / total) * 100 if total > 0 else 0  # Prevent division by zero

        # Adjust x position dynamically based on the bar width
        x_position = absolute_value / 2
        ha_value = 'center'

        # If the value is too small, adjust placement
        if absolute_value < 2:
            x_position = absolute_value + 0.5  # Move slightly right
            ha_value = 'left'

        # Display the absolute value and percentage
        ax.text(x_position, bar.get_y() + bar.get_height() / 2,
                f'{absolute_value} \n{percentage:.0f}%', va='center', ha=ha_value, fontsize=10, color='black')

    # Apply tight layout to ensure everything fits
    plt.tight_layout(pad=2.0)

    return fig, ax

# Run the function with loaded results
survey(loaded_results, category_names)

# Save and display the plot
plot_path = os.path.join(csv_dir, "plot1.jpg")
plt.savefig(plot_path)
plt.show()
