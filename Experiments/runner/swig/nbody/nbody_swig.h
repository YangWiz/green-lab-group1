// nbody_swig.h
#ifndef NBODY_SWIG_H
#define NBODY_SWIG_H

#include <vector>

// Body structure
struct Body {
    double x;
    double y;
    double vx;
    double vy;
    double m;
    
    Body() : x(0), y(0), vx(0), vy(0), m(0) {}
    Body(double x_, double y_, double vx_, double vy_, double m_) 
        : x(x_), y(y_), vx(vx_), vy(vy_), m(m_) {}
};

typedef std::vector<Body> BodiesVector;

// Initialize N bodies with random positions, velocities, and masses
BodiesVector initialize_bodies(int N, double box_size = 1000.0, double max_mass = 1.0);

// Perform one N-body simulation step
BodiesVector nbody_step_update(const BodiesVector& bodies, double dt, 
                                double G = 6.674e-11, double softening = 1e-9);

#endif // NBODY_SWIG_H