#include <iostream>
#include <fstream>
#include <iomanip>
#include <cmath>

#define NE  2000
#define C0  3.E8
#define CFL 0.05
#define DEL 0.01
#define DT  (CFL * DEL / C0)
#define CDT (C0*DT)
#define PI  3.1415926535897932

double z[NE + 3];
double epr[NE + 2];
double mur[NE + 2];

typedef struct _ELEM_ {
    double mat_ep[2][2];
    double mat_mu[2][2];

    double e[2] = {0, 0};
    double h[2] = {0, 0};
}
        ELEM;

ELEM elem[NE + 2];

void BuildMassMatrix() {
    for (int ielem = 1; ielem <= NE; ++ielem) {
        epr[ielem] = 1;
        mur[ielem] = 1;


        double dz = z[ielem + 1] - z[ielem];

        elem[ielem].mat_ep[0][0] = dz * epr[ielem] / 3.0;
        elem[ielem].mat_ep[0][1] = dz * epr[ielem] / 6.0;
        elem[ielem].mat_ep[1][0] = dz * epr[ielem] / 6.0;
        elem[ielem].mat_ep[1][1] = dz * epr[ielem] / 3.0;

        elem[ielem].mat_mu[0][0] = dz * mur[ielem] / 3.0;
        elem[ielem].mat_mu[0][1] = dz * mur[ielem] / 6.0;
        elem[ielem].mat_mu[1][0] = dz * mur[ielem] / 6.0;
        elem[ielem].mat_mu[1][1] = dz * mur[ielem] / 3.0;

        double deno;

        double tpm[2][2];

        deno = elem[ielem].mat_ep[0][0] * elem[ielem].mat_ep[1][1] -
               elem[ielem].mat_ep[0][1] * elem[ielem].mat_ep[1][0];

        tpm[0][0] = +elem[ielem].mat_ep[1][1] / deno;
        tpm[0][1] = -elem[ielem].mat_ep[0][1] / deno;
        tpm[1][0] = -elem[ielem].mat_ep[1][0] / deno;
        tpm[1][1] = +elem[ielem].mat_ep[0][0] / deno;

        for (int i = 0; i < 4; ++i)*(*elem[ielem].mat_ep + i) = *(*tpm + i);

        deno = elem[ielem].mat_mu[0][0] * elem[ielem].mat_mu[1][1] -
               elem[ielem].mat_mu[0][1] * elem[ielem].mat_mu[1][0];

        tpm[0][0] = +elem[ielem].mat_mu[1][1] / deno;
        tpm[0][1] = -elem[ielem].mat_mu[0][1] / deno;
        tpm[1][0] = -elem[ielem].mat_mu[1][0] / deno;
        tpm[1][1] = +elem[ielem].mat_mu[0][0] / deno;

        for (int i = 0; i < 4; ++i)*(*elem[ielem].mat_mu + i) = *(*tpm + i);
    }
}

double Dz[2][2] = {{-0.5, -0.5},
                   {0.5,  0.5}};

void UpdateEx() {
    for (int ielem = 1; ielem <= NE; ++ielem) {
        double rhs[2] = {0};

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; ++j) {
                rhs[i] += CDT * Dz[i][j] * elem[ielem].h[j];
            }
        }

        {
            rhs[0] += 0.5 * CDT * (elem[ielem - 1].h[1] + elem[ielem].h[0]);
            rhs[1] -= 0.5 * CDT * (elem[ielem + 1].h[0] + elem[ielem].h[1]);
        }

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; ++j) {
                elem[ielem].e[i] += elem[ielem].mat_ep[i][j] * rhs[j];
            }
        }
    }

    elem[0000].e[1] = -elem[01].e[0];

    elem[NE + 1].e[0] = -elem[NE].e[1];
}

void UpdateHy() {
    for (int ielem = 1; ielem <= NE; ++ielem) {
        double rhs[2] = {0};

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; ++j) {
                rhs[i] += CDT * Dz[i][j] * elem[ielem].e[j];
            }
        }

        {
            rhs[0] += 0.5 * CDT * (elem[ielem - 1].e[1] + elem[ielem].e[0]);
            rhs[1] -= 0.5 * CDT * (elem[ielem + 1].e[0] + elem[ielem].e[1]);
        }

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; ++j) {
                elem[ielem].h[i] += elem[ielem].mat_mu[i][j] * rhs[j];
            }
        }
    }

    elem[000000].h[1] = elem[01].h[0];
    elem[NE + 1].h[0] = elem[NE].h[1];
}

void Init() {

    for (int k = 0; k < NE + 3 + 1; k++) {
        z[k] = k * DEL;
    }

    {
        double th = -DT / 2.0;
        double te = 0.0000000;

        for (int ielem = 1; ielem <= NE; ++ielem) {
            elem[ielem].h[0] = sin((double) ielem / NE * 2 * PI);
            elem[ielem].h[1] = sin(((double) ielem + 1) / NE * 2 * PI);

            elem[ielem].e[0] = sin((double) ielem / NE * 2 * PI);
            elem[ielem].e[1] = sin(((double) ielem + 1) / NE * 2 * PI);
        }
    }
}

int main(void) {
    Init();
    BuildMassMatrix();

    int nt = 6. / CDT;

    double t = 0.0;

    std::ofstream EvsT("ex_vs_t.dat");

    for (int it = 0; it < nt; ++it) {
        UpdateHy();

        t += 0.5 * DT;

        UpdateEx();

        t = (it + 1) * DT;

        if (it % 1000 == 0)
            /*std::cout
                    << std::setw(25) << std::setprecision(15) << t
                    << std::setw(25) << std::setprecision(15) << 0.5 * (elem[100].e[0] + elem[100].e[1])
                    << std::endl;*/

            EvsT
                    << std::setw(25) << std::setprecision(15) << t
                    << std::setw(25) << std::setprecision(15) << 0.5 * (elem[100].e[0] + elem[100].e[1])
                    << std::endl;


    }

    EvsT.close();
    EvsT.clear();

    std::ofstream EvsZ("ex_vs_z.dat");

    for (int ielem = 1; ielem <= NE; ++ielem) {
        EvsZ
                << std::setw(25) << std::setprecision(15) << 0.5 * (z[ielem] + z[ielem + 1])
                << std::setw(25) << std::setprecision(15) << 0.5 * (elem[ielem].e[0] + elem[ielem].e[1])
                << std::endl;
    }

    EvsZ.close();
    EvsZ.clear();
}