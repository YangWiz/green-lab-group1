// nbody_swig.cpp
#include "nbody_swig.h"
#include <cmath>
#include <cstdlib>
#include <ctime>

BodiesVector initialize_bodies(int N, double box_size, double max_mass) {
    BodiesVector bodies;
    bodies.reserve(N);
    
    // Seed random number generator (only once)
    static bool seeded = false;
    if (!seeded) {
        std::srand(std::time(nullptr));
        seeded = true;
    }
    
    for (int i = 0; i < N; i++) {
        Body body;
        body.x = (static_cast<double>(std::rand()) / RAND_MAX) * box_size;
        body.y = (static_cast<double>(std::rand()) / RAND_MAX) * box_size;
        body.vx = (static_cast<double>(std::rand()) / RAND_MAX) * 2.0 - 1.0;  // [-1, 1]
        body.vy = (static_cast<double>(std::rand()) / RAND_MAX) * 2.0 - 1.0;  // [-1, 1]
        body.m = (static_cast<double>(std::rand()) / RAND_MAX) * (max_mass - 0.1) + 0.1;  // [0.1, max_mass]
        
        bodies.push_back(body);
    }
    
    return bodies;
}

BodiesVector nbody_step_update(const BodiesVector& bodies, double dt, double G, double softening) {
    int N = bodies.size();
    
    // Create a copy of bodies to update
    BodiesVector updated_bodies = bodies;
    
    // Allocate acceleration arrays
    std::vector<double> ax(N, 0.0);
    std::vector<double> ay(N, 0.0);
    
    // 1. Calculate net acceleration (O(N^2) loop)
    for (int i = 0; i < N; i++) {
        const Body& body_i = bodies[i];
        
        for (int j = 0; j < N; j++) {
            if (i == j) continue;
            
            const Body& body_j = bodies[j];
            
            // Calculate displacement vector
            double dx = body_j.x - body_i.x;
            double dy = body_j.y - body_i.y;
            
            // Calculate distance with softening
            double dist_sq = dx * dx + dy * dy;
            double dist_soft = std::sqrt(dist_sq + softening);
            
            // Calculate acceleration
            double inv_dist_cube = 1.0 / (dist_soft * dist_soft * dist_soft);
            double force_factor = G * body_j.m * inv_dist_cube;
            
            ax[i] += dx * force_factor;
            ay[i] += dy * force_factor;
        }
    }
    
    // 2. Update velocity and position (O(N) loop)
    for (int i = 0; i < N; i++) {
        // Update velocity (Euler integration)
        updated_bodies[i].vx += ax[i] * dt;
        updated_bodies[i].vy += ay[i] * dt;
        
        // Update position
        updated_bodies[i].x += updated_bodies[i].vx * dt;
        updated_bodies[i].y += updated_bodies[i].vy * dt;
    }
    
    return updated_bodies;
}