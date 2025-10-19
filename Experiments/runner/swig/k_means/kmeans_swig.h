// kmeans_swig.h
#ifndef KMEANS_SWIG_H
#define KMEANS_SWIG_H

#include <vector>

// Type definitions for clarity
typedef std::vector<double> Point;
typedef std::vector<Point> DataSet;

// Initialize random data points
DataSet initialize_data(int N, int D, double max_val = 100.0);

// Initialize centroids by randomly selecting K points from data
DataSet initialize_centroids(const DataSet& data, int K);

// Perform one K-means iteration (assignment + update)
// Returns new centroids
DataSet kmeans_iteration(const DataSet& data, const DataSet& centroids);

// Helper function to calculate Euclidean distance
double euclidean_distance(const Point& p1, const Point& p2);

#endif // KMEANS_SWIG_H