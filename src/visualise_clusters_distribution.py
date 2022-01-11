from collections import Counter # for specialised data types
import matplotlib.pyplot as plt
import pandas as pd

def visualise_clusters_distribution(labels):
    
    pd.DataFrame(Counter(labels).most_common()).set_index(0).plot.bar(legend=None)
    plt.title('Distribution of Clusters')
    plt.xlabel('Cluster ID')
    plt.ylabel('# of users belonging to the cluster');