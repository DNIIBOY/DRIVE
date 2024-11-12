import matplotlib.pyplot as plt
# Re-create the plot with adjustments to avoid overlap between "Danish Environment Agency" and "Danish Road Directorate".

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Matrix sections for visual aid
plt.axvline(x=5, color="grey", linestyle="--")
plt.axhline(y=5, color="grey", linestyle="--")

# Set labels for the axis without showing tick numbers
ax.set_xlabel("Influence", fontsize=14)
ax.set_ylabel("Complicity", fontsize=14)
ax.set_xticks([])
ax.set_yticks([])
# ax.set_title("Stakeholder Influence and Complicity Matrix on Highway Traffic", fontsize=16)

# Adjusted positions to avoid overlap
stakeholders = [
    (3, 8, "Private Commuters", "center", "center"),             # High complicity, low influence
    (3, 8.5, "Transportation Businesses", "center", "center"),      # High complicity, high influence
    (2, 6.6, "Danish Industry", "center", "center"),                # Moderate complicity, moderate influence
    (8, 4, "Danish Road Directorate", "center", "center"),        # Low complicity, high influence
    (6, 3, "Danish Environment Agency", "center", "center"),      # Low complicity, moderate influence
    (4, 6, "Emergency Services", "center", "center"),             # Low complicity, low influence
]

# Plot each stakeholder in the matrix
for x, y, label, ha, va in stakeholders:
    ax.text(x, y, label, ha=ha, va=va, fontsize=12,
            bbox=dict(facecolor="lightblue", edgecolor="black", boxstyle="round,pad=0.3"))

# Label the quadrants
ax.text(2.5, 9.5, "High Complicity\nLow Influence", ha="center", va="center", fontsize=12, color="grey")
ax.text(7.5, 9.5, "High Complicity\nHigh Influence", ha="center", va="center", fontsize=12, color="grey")
ax.text(2.5, 0.5, "Low Complicity\nLow Influence", ha="center", va="center", fontsize=12, color="grey")
ax.text(7.5, 0.5, "Low Complicity\nHigh Influence", ha="center", va="center", fontsize=12, color="grey")

# Display the plot
plt.grid(False)
plt.show()
