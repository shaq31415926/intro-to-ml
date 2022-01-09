from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 


def optimal_number_clusters(df):
    """
    Calculates optimal number of clusted based on Elbow Method
    
    parameters df
    """
    
    Sum_of_squared_distances = []
    K = range(1, 30) # define the range of clusters we would like to cluster the data into

    for k in K:
        km = KMeans(n_clusters = k)
        km = km.fit(df)
        Sum_of_squared_distances.append(km.inertia_)

    plt.figure(figsize=(20,6))

    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()