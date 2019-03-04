// Newton method
#include <stdio.h>
#include "newton.c"

int main() {
    int max_step, steps;
    double init_gue, eps;
    eps = 1e-13;
    max_step = (int) 1e6;    // max steps
    init_gue = -5;    // initial guess
    steps = dnewt(&init_gue, eps, max_step); // steps is used steps
    if (steps == max_step)
        puts("Max steps reached. Check the result!");
    printf("steps=%d  x=%13.7e\n", steps, init_gue);
}
