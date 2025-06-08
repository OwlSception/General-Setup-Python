# Standard Library

# Third Party Library

# Local Library


# Logger


# PCA

from sklearn.decomposition import PCA

# Function to perform PCA

def perform_pca(data, n_components=2):
    # Initialize PCA
    pca = PCA(n_components=n_components)
    
    # Fit and transform the data
    pca_data = pca.fit_transform(data)
    
    return pca_data
