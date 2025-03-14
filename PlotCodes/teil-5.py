import matplotlib.pyplot as plt
import numpy as np

# Data
label = ["Ja", "Nein"][::-1]
val = [21, 9][::-1]
val_sum = sum(val)

colors = plt.colormaps['RdYlGn_r'](
        np.linspace(0.15, 0.85, 2))[::-1]

# Append data and assign color
label.append("")  # Empty label for blank space
val.append(sum(val))  # Blank space for half-ring effect (50% blank)
colors = np.vstack([colors, [1, 1, 1, 1]])

# Plot
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(1, 1, 1)

# Create the pie chart with percentage display for only the non-white segments
wedges, texts, autotexts = ax.pie(val, labels=None, colors=colors, 
                                  wedgeprops={'width': 0.3, 'edgecolor': 'white'},autopct= '%1.1f%%',
                                  startangle=0, pctdistance=0.85)  # Move text inside the ring

# Hide the text for the white part
for id, text in enumerate(autotexts):
    if text.get_text() == '50.0%':  # Blank space for half-ring effect
        text.set_text('')  # Remove text for the white part
    else:
        # Format the text to show both absolute value and percentage
        text.set_text(f"{val[id]} \n{int(round(val[id] / val_sum * 100, 1))}%")
        text.set_color('black')
        # Rotate the text to align with the wedge
        #angle = wedges[id].theta1  # Adjust angle for text rotation (shift by 90 degrees for proper alignment)
        #text.set_rotation(angle)

# Add a circle in the center to create a doughnut effect
ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))

# Set the aspect ratio to ensure the chart is circular
ax.set_aspect('equal')

# Set the y-axis limits to crop the pie chart to the top half (for half-ring effect)
ax.set_ylim(0, 1)

# Title for the plot with additional space between title and plot
ax.set_title("Digitale Tools in Fach 1", pad=20)

ax.legend(wedges[::-1][1:], label[::-1][1:], loc="center") #, title="Categories", loc="center left", fontsize=10)

plt.tight_layout()

# Display the plot
plt.savefig("plot5.jpg")
plt.show()
