import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure figures directory exists
os.makedirs("figures", exist_ok=True)

# Formatting settings
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.grid'] = True

# Time series data simulation (e.g., 24 hours)
hours = np.arange(1, 25)
heuristic_detections = np.array([45, 48, 52, 60, 55, 50, 42, 40, 38, 41, 45, 52, 85, 90, 88, 70, 62, 58, 55, 52, 48, 46, 44, 43])
llm_detections = np.array([92, 94, 91, 95, 93, 94, 90, 92, 91, 93, 95, 96, 98, 99, 97, 96, 94, 93, 95, 94, 92, 91, 93, 92])

fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)

ax.plot(hours, llm_detections, color='#1a5f7a', linestyle='-', linewidth=2.0, marker='o', label='LLM-Agent Semantic Detection')
ax.plot(hours, heuristic_detections, color='#c84b31', linestyle='--', linewidth=1.5, marker='s', label='Traditional Heuristic Rules')

ax.set_title('Network Anomalies Over Time: LLM vs. Heuristic Detection', fontsize=12, pad=12)
ax.set_xlabel('Time of Day (Hours)', fontsize=10)
ax.set_ylabel('Anomaly Detection Rate (F1-Score %)', fontsize=10)
ax.set_xlim(1, 24)
ax.set_ylim(30, 105)
ax.set_xticks(np.arange(2, 25, 2))
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower left', frameon=True, facecolor='white', edgecolor='#e0e0e0')

plt.tight_layout()

# Save the PDF file
output_path = os.path.join("figures", "anomalies_over_time.pdf")
plt.savefig(output_path, format='pdf', bbox_inches='tight')
plt.close()

print(f"Graph successfully generated and saved to {output_path}")
