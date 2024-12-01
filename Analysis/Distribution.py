import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import json

def plotDistribute(scores, label, normal=False):
    # plt.hist(scores, bins=10, density=True, alpha=0.6, color='blue', label='Actual Data Distribution')
    bins = np.linspace(min(scores), max(scores), 10)
    hist, bin_edges = np.histogram(scores, bins=bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    plt.plot(bin_centers, hist, label=label, marker='o')
    if normal:
        # Calculate mean and standard deviation for normal distribution
        mean = np.mean(scores)
        std_dev = np.std(scores)
        # Generate x values for plotting the normal distribution
        x = np.linspace(min(scores) - 0.5, max(scores) + 0.5, 1000)
        normal_dist = norm.pdf(x, mean, std_dev)
        # Plot the normal distribution for comparison
        plt.plot(x, normal_dist, 'r-', label='Normal Distribution')

# 假设 JSON 文件名为 data.json
file_name = '../base_model/data.json'

# 打开并读取 JSON 文件
with open(file_name, 'r') as file:
    data = json.load(file)

# Flattening the data to create a distribution
overall_scores = []
recommendHiring_scores = []
structuredAnswers_scores = []
for key in data:
    overall_scores.append(data[key]['Overall'])
    structuredAnswers_scores.append(data[key]['StructuredAnswers'])
    recommendHiring_scores.append(data[key]['RecommendHiring'])
    
    # scores.extend(data[key].values())

plotDistribute(overall_scores,'Overall')
plotDistribute(structuredAnswers_scores,'StructuredAnswers')
plotDistribute(recommendHiring_scores,'RecommendHiring',True)
# Add labels, title, and legend
plt.xlabel('Scores')
plt.ylabel('Density')
plt.title('Score Distribution vs Normal Distribution')
plt.legend(loc="upper left")

# Show the plot
plt.tight_layout()
plt.savefig("dis.png",dpi=300)
