// Newton method
#include <stdio.h>
#include "newton.c"

int main() {
    int js, k;
    double x, eps;
    eps = 0.000001;
    js = 60;    // max steps
    x = 1.46;    // initial guess
    k = dnewt(&x, eps, js); // k is used steps
    if (k >= 0)
        printf("k=%d  x=%13.7e\n", k, x);
    printf("\n");
}
