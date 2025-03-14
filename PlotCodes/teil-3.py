import matplotlib.pyplot as plt
import numpy as np

# Define category names
category_names = ["Laptop", "Handy", "Smartboard", "Tablet", "Thin Clients oder schuleigene Rechner"]

# Define results
results = {"results": [14, 9, 4, 4, 7]}

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

    category_colors = plt.colormaps['RdYlGn_r'](
        np.linspace(0.15, 0.85, data.shape[1]))[::-1][-1]
    
    # Calculate the total sum of values to compute percentages
    total = np.sum(data)

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(9.4, 5))
    ax.set_title("Nutzung digitaler Geräte in Fach 1", pad=30)  # Add padding for the title

    # Define bar height and y positions for the bars
    bar_height = 0.5
    y_pos = np.arange(len(category_names))

    # Plot horizontal bars with green color
    bars = ax.barh(y_pos, data[0], height=bar_height, label='Results', color=category_colors)

    # Set labels and ticks
    ax.set_xlabel('Anzahl')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(category_names)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])

    # Display absolute and percentage values inside the bars
    for i, bar in enumerate(bars):
        absolute_value = bar.get_width()
        percentage = (absolute_value / total) * 100 if total > 0 else 0  # Prevent division by zero

        # Adjust x position for the last bar (if value is 0, move it slightly to the right)
        if absolute_value == 0:
            x_position = 0.1  # Small indent to make it visible
            ha_value = 'left'  # Align left so it's readable
        else:
            # x_position = absolute_value / 2
            # ha_value = 'center'
            x_position = 0.1  # Small indent to make it visible
            ha_value = 'left'  # Align left so it's readable

        # Display the absolute value and percentage
        ax.text(x_position, bar.get_y() + bar.get_height() / 2,
                f'{absolute_value} \n{percentage:.0f}%', va='center', ha=ha_value, fontsize=10, color='black')


    # Apply tight layout to ensure everything fits
    plt.tight_layout(pad=2.0)

    return fig, ax

survey(results, category_names)
plt.savefig("plot3.jpg")
plt.show()
