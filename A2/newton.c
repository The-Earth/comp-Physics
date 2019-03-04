// newton method solving non-linear problem
#include <stdio.h>
#include <math.h>

void dnewtf(x, y)
        double x, y[2];
{
    y[0] = x * x - 1; // f(x)
    y[1] = 2 * x;   // f'(x)
}

int dnewt(x, eps, js)
        int js;
        double *x, eps;
{
    int k, l;
    double y[2], d, p, x0, x1;
    l = js;
    x0 = *x;
    x1 = *x;
    dnewtf(x0, y);
    d = eps + 1.0;
    while ((d >= eps) && (l != 0)) {
        if (fabs(y[1]) + 1.0 == 1.0) {  // derivative = 0
            x0 += eps;
            dnewtf(x0, y);
            continue;
        }
        x1 = x0 - y[0] / y[1];  // update x
        dnewtf(x1, y);
        d = fabs(x1 - x0);
        p = fabs(y[0]);
        if (p > d)
            d = p;
        x0 = x1;
        l = l - 1;  // remaining steps
    }
    *x = x1;
    k = js - l; // used steps
    return (k);
}