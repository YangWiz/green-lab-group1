// kmeans_swig.cpp
#include "kmeans_swig.h"
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <limits>
#include <algorithm>

double euclidean_distance(const Point& p1, const Point& p2) {
    double distance_sq = 0.0;
    size_t D = p1.size();
    
    for (size_t i = 0; i < D; i++) {
        double diff = p1[i] - p2[i];
        distance_sq += diff * diff;
    }
    
    return std::sqrt(distance_sq);
}

DataSet initialize_data(int N, int D, double max_val) {
    DataSet data;
    data.reserve(N);
    
    // Seed random number generator (only once)
    static bool seeded = false;
    if (!seeded) {
        std::srand(std::time(nullptr));
        seeded = true;
    }
    
    for (int i = 0; i < N; i++) {
        Point point;
        point.reserve(D);
        
        for (int d = 0; d < D; d++) {
            double val = (static_cast<double>(std::rand()) / RAND_MAX) * max_val;
            point.push_back(val);
        }
        
        data.push_back(point);
    }
    
    return data;
}

DataSet initialize_centroids(const DataSet& data, int K) {
    DataSet centroids;
    
    if (data.empty() || K <= 0 || K > static_cast<int>(data.size())) {
        return centroids;
    }
    
    // Create a copy of indices
    std::vector<int> indices;
    for (size_t i = 0; i < data.size(); i++) {
        indices.push_back(i);
    }
    
    // Shuffle indices
    for (int i = indices.size() - 1; i > 0; i--) {
        int j = std::rand() % (i + 1);
        std::swap(indices[i], indices[j]);
    }
    
    // Select first K points
    for (int k = 0; k < K; k++) {
        centroids.push_back(data[indices[k]]);
    }
    
    return centroids;
}

DataSet kmeans_iteration(const DataSet& data, const DataSet& centroids) {
    int N = data.size();
    int K = centroids.size();
    
    if (N == 0 || K == 0) {
        return centroids;
    }
    
    int D = data[0].size();
    
    // Assignment Step: assign each point to nearest centroid
    std::vector<int> assignments(N);
    std::vector<int> cluster_counts(K, 0);
    std::vector<Point> cluster_sums(K, Point(D, 0.0));
    
    for (int i = 0; i < N; i++) {
        double min_dist = std::numeric_limits<double>::max();
        int closest_k = 0;
        
        for (int k = 0; k < K; k++) {
            double dist = euclidean_distance(data[i], centroids[k]);
            if (dist < min_dist) {
                min_dist = dist;
                closest_k = k;
            }
        }
        
        assignments[i] = closest_k;
        cluster_counts[closest_k]++;
        
        // Accumulate sums for centroid update
        for (int d = 0; d < D; d++) {
            cluster_sums[closest_k][d] += data[i][d];
        }
    }
    
    // Update Step: calculate new centroids
    DataSet new_centroids;
    new_centroids.reserve(K);
    
    for (int k = 0; k < K; k++) {
        if (cluster_counts[k] == 0) {
            // Keep old centroid if cluster is empty
            new_centroids.push_back(centroids[k]);
        } else {
            // Calculate mean
            Point new_centroid;
            new_centroid.reserve(D);
            
            for (int d = 0; d < D; d++) {
                new_centroid.push_back(cluster_sums[k][d] / cluster_counts[k]);
            }
            
            new_centroids.push_back(new_centroid);
        }
    }
    
    return new_centroids;
}