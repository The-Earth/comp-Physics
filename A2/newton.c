// newton method solving non-linear problem
#include <stdio.h>
#include <math.h>

void dnewtf(double x, double y[2])  // define formula f(x) = 0 (Van de Waals Oxygen)
{
    double a = 0.138, b = 3.18e-5, R = 8.314472;
    y[0] = (1.013e5 + a / pow(x, 2)) * (x - b) / R - 273.15; // f(x)
    y[1] = (2 * a * b - a * x + 1e5 * pow(x, 3)) / (R * pow(x, 3));   // f'(x)
}

int dnewt(double *x, double eps, int max) {
    int remain;
    double y[2], dx, dy, x0, x1;
    remain = max;
    x0 = *x;
    x1 = *x;
    dnewtf(x0, y);
    dx = eps + 1.0;
    while ((dx >= eps) && (remain != 0)) {
        if (fabs(y[1]) < eps) {  // derivative = 0
            x0 += eps;
            dnewtf(x0, y);
            continue;
        }
        x1 = x0 - y[0] / y[1];  // update x
        dnewtf(x1, y);
        dx = fabs(x1 - x0);
        dy = fabs(y[0]);
        if (dy > dx)
            dx = dy;
        x0 = x1;
        remain = remain - 1;  // remaining steps
    }
    *x = x1;    // return x through pointer
    int step = max - remain;
    return step;
}