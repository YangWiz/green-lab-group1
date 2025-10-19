# kmeans_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.math cimport sqrt
from libc.stdlib cimport malloc, free
from libc.float cimport DBL_MAX
import random

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cdef inline double euclidean_distance_cy(double* p1, double* p2, int D) nogil:
    """Calculates the Euclidean distance between two D-dimensional points."""
    cdef int i
    cdef double distance_sq = 0.0
    
    for i in range(D):
        distance_sq += (p1[i] - p2[i]) * (p1[i] - p2[i])
    
    return sqrt(distance_sq)


def initialize_data_cy(int N, int D, double max_val=100.0):
    """Generates N random D-dimensional data points."""
    data = []
    cdef int i, d
    
    for i in range(N):
        point = tuple(random.uniform(0, max_val) for d in range(D))
        data.append(point)
    return data


def initialize_centroids_cy(list data, int K):
    """Selects K random data points as initial centroids."""
    return random.sample(data, K)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def kmeans_iteration_cy(list data, list centroids):
    """
    Cython-optimized K-means iteration (assignment and centroid update).
    Complexity is O(N * K * D), where N is data points, K is clusters, and D is dimensions.
    
    Returns:
        list: The new list of centroids.
    """
    cdef int N = len(data)
    cdef int K = len(centroids)
    cdef int D
    cdef int i, j, k, d
    cdef double dist, min_dist
    cdef int closest_k
    cdef double** data_arr
    cdef double** centroids_arr
    cdef int* assignments
    cdef int* cluster_counts
    cdef double** cluster_sums
    cdef list new_centroids
    cdef tuple point, centroid
    
    if N == 0 or K == 0:
        return centroids
    
    D = len(data[0])
    
    # Allocate C arrays
    data_arr = <double**>malloc(N * sizeof(double*))
    centroids_arr = <double**>malloc(K * sizeof(double*))
    assignments = <int*>malloc(N * sizeof(int))
    cluster_counts = <int*>malloc(K * sizeof(int))
    cluster_sums = <double**>malloc(K * sizeof(double*))
    
    if data_arr == NULL or centroids_arr == NULL or assignments == NULL or cluster_counts == NULL or cluster_sums == NULL:
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Allocate rows for data
        for i in range(N):
            data_arr[i] = <double*>malloc(D * sizeof(double))
            if data_arr[i] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Allocate rows for centroids
        for k in range(K):
            centroids_arr[k] = <double*>malloc(D * sizeof(double))
            if centroids_arr[k] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Allocate rows for cluster sums
        for k in range(K):
            cluster_sums[k] = <double*>malloc(D * sizeof(double))
            if cluster_sums[k] == NULL:
                raise MemoryError("Failed to allocate memory")
        
        # Copy data to C arrays
        for i in range(N):
            point = data[i]
            for d in range(D):
                data_arr[i][d] = point[d]
        
        # Copy centroids to C arrays
        for k in range(K):
            centroid = centroids[k]
            for d in range(D):
                centroids_arr[k][d] = centroid[d]
        
        # Initialize cluster sums and counts
        for k in range(K):
            cluster_counts[k] = 0
            for d in range(D):
                cluster_sums[k][d] = 0.0
        
        # Assignment Step (O(N * K * D))
        for i in range(N):
            min_dist = DBL_MAX
            closest_k = 0
            
            for k in range(K):
                dist = euclidean_distance_cy(data_arr[i], centroids_arr[k], D)
                if dist < min_dist:
                    min_dist = dist
                    closest_k = k
            
            assignments[i] = closest_k
            cluster_counts[closest_k] += 1
            
            # Add point to cluster sum
            for d in range(D):
                cluster_sums[closest_k][d] += data_arr[i][d]
        
        # Update Step: Calculate new centroids
        new_centroids = []
        for k in range(K):
            if cluster_counts[k] == 0:
                # Keep old centroid if cluster is empty
                new_centroids.append(centroids[k])
            else:
                # Calculate mean
                new_centroid = [0.0] * D
                for d in range(D):
                    new_centroid[d] = cluster_sums[k][d] / cluster_counts[k]
                new_centroids.append(tuple(new_centroid))
        
        return new_centroids
    
    finally:
        # Free all allocated memory
        if data_arr != NULL:
            for i in range(N):
                if data_arr[i] != NULL:
                    free(data_arr[i])
            free(data_arr)
        
        if centroids_arr != NULL:
            for k in range(K):
                if centroids_arr[k] != NULL:
                    free(centroids_arr[k])
            free(centroids_arr)
        
        if cluster_sums != NULL:
            for k in range(K):
                if cluster_sums[k] != NULL:
                    free(cluster_sums[k])
            free(cluster_sums)
        
        if assignments != NULL:
            free(assignments)
        if cluster_counts != NULL:
            free(cluster_counts)