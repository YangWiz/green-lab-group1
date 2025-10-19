# nbody_cy.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.math cimport sqrt
from libc.stdlib cimport malloc, free
import random

# --- Body Structure ---
cdef struct Body:
    double x
    double y
    double vx
    double vy
    double m

def initialize_bodies_cy(int N, double box_size=100.0, double max_mass=1.0):
    """Generates N bodies with random positions, velocities, and masses."""
    bodies = []
    cdef int i
    
    for i in range(N):
        bodies.append({
            'x': random.uniform(0, box_size),
            'y': random.uniform(0, box_size),
            'vx': random.uniform(-1, 1),
            'vy': random.uniform(-1, 1),
            'm': random.uniform(0.1, max_mass),
        })
    return bodies


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def nbody_step_update_cy(list bodies, double dt, double G=6.674e-11, double softening=1e-9):
    """
    Cython-optimized N-body simulation step using pairwise interactions.
    Complexity is O(N^2).
    
    Args:
        bodies: List of body dictionaries
        dt: Time step
        G: Gravitational constant
        softening: Softening parameter to prevent singularities
    
    Returns:
        Updated bodies list
    """
    cdef int N = len(bodies)
    cdef int i, j
    cdef double ax, ay
    cdef double dx, dy, dist_sq, dist_soft, inv_dist_cube, force_factor
    cdef Body* body_array
    cdef double* accel_x
    cdef double* accel_y
    
    # Allocate C arrays for bodies and accelerations
    body_array = <Body*>malloc(N * sizeof(Body))
    accel_x = <double*>malloc(N * sizeof(double))
    accel_y = <double*>malloc(N * sizeof(double))
    
    if body_array == NULL or accel_x == NULL or accel_y == NULL:
        if body_array != NULL:
            free(body_array)
        if accel_x != NULL:
            free(accel_x)
        if accel_y != NULL:
            free(accel_y)
        raise MemoryError("Failed to allocate memory")
    
    try:
        # Copy bodies from Python list to C array
        for i in range(N):
            body = bodies[i]
            body_array[i].x = body['x']
            body_array[i].y = body['y']
            body_array[i].vx = body['vx']
            body_array[i].vy = body['vy']
            body_array[i].m = body['m']
        
        # Calculate accelerations (O(N^2) loop)
        for i in range(N):
            ax = 0.0
            ay = 0.0
            
            for j in range(N):
                if i == j:
                    continue
                
                # Calculate displacement
                dx = body_array[j].x - body_array[i].x
                dy = body_array[j].y - body_array[i].y
                
                # Calculate distance with softening
                dist_sq = dx*dx + dy*dy
                dist_soft = sqrt(dist_sq + softening)
                
                # Calculate acceleration
                inv_dist_cube = 1.0 / (dist_soft * dist_soft * dist_soft)
                force_factor = G * body_array[j].m * inv_dist_cube
                
                ax += dx * force_factor
                ay += dy * force_factor
            
            accel_x[i] = ax
            accel_y[i] = ay
        
        # Update velocities and positions (O(N) loop)
        for i in range(N):
            body_array[i].vx += accel_x[i] * dt
            body_array[i].vy += accel_y[i] * dt
            body_array[i].x += body_array[i].vx * dt
            body_array[i].y += body_array[i].vy * dt
        
        # Copy back to Python list
        for i in range(N):
            bodies[i]['x'] = body_array[i].x
            bodies[i]['y'] = body_array[i].y
            bodies[i]['vx'] = body_array[i].vx
            bodies[i]['vy'] = body_array[i].vy
        
        return bodies
    
    finally:
        free(body_array)
        free(accel_x)
        free(accel_y)