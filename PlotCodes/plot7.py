import matplotlib.pyplot as plt
import numpy as np

# Define category names
category_names = ['Vollständig digital', 'Überwiegend digital', 'Überwiegend analog', 'Vollständig analog']

# Define results
results = {
    'Unterrichtsmaterialien': [4,7,3,2],
    'Durchführung des Unterrichts': [1, 2, 10, 3],
    'Leistungsfeststellung': [1, 5, 1, 15],
    'Korrektur und Beurteilung': [5, 1, 3, 10],
    'Leistungsdokumentation': [3, 10, 4, 5]
}

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
    labels = list(results.keys())
    data = np.array(list(results.values()))

    # Convert counts to percentages
    data_percent = data / data.sum(axis=1, keepdims=True) * 100
    data_cum = data_percent.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn_r'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.4, 5))
    ax.set_title("Derzeitiger Stand der Digitalisierung in Fach 1", pad=30)  # Increase padding for the title
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, 100)

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data_percent[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.7,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'black' if r * g * b < 0.5 else 'darkgrey'
        
        # Labeling with percentages
        ax.bar_label(rects, label_type='center', color=text_color,
                     labels=[f'{y} \n{x:.0f}%' for x, y in zip(widths, data[:,i])])

    # Adjust the legend to be lower and make space for the title
    ax.legend(ncols=len(category_names), bbox_to_anchor=(0, 1.005),
              loc='lower left', fontsize='small')

    # Apply tight_layout to ensure everything fits
    plt.tight_layout(pad=2.0)  # Adjust overall layout padding

    return fig, ax

survey(results, category_names)
plt.savefig("plot7.jpg")
plt.show()
