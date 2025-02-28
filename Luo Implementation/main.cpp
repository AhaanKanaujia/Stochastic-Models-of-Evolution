#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <string>

using namespace std;

vector<double> get_leaving_rates(vector<double> u, int m, int n, double r, double s) {
    vector<double> L(n + 1, 0.0);

    double sum = 0.0;
    for(int i = 0; i < n + 1; i++) {
        sum += u[i] * (1 + r * i/n);
    }

    for(int i = 0; i < n + 1; i++) {
        double term_sum = sum - u[i] * (1 + r * i/n);

        if (i == 0 || i == n) {
            // m * u[i] to the term to ensure positive probabilities
            // fixed typo from the paper
            L[i] = m * u[i] * term_sum;
        } else {
            L[i] = m * u[i] * (n - i) * i/n * (2 + s) + m * u[i] * term_sum;
        }
    }

    return L;
}

vector<double> get_incoming_rates(vector<double> u, int m, int n, double r, double s, double I1) {
    vector<double> G(n + 1, 0.0);

    for(int i = 0; i < n + 1; i++) {
        if(i == I1 - 1 && I1 < n) {
            G[i] = (n - I1) * (1 + s) * I1/n + u[I1 - 1] * (1 + r * (I1 - 1)/n);
        } else if(i == I1 + 1 && I1 > 0) {
            G[i] = I1 * (1 - I1/n) + u[I1 + 1] * (1 + r * (I1 + 1)/n);
        } else if(abs(i - I1) > 1) {
            G[i] = u[i] * (1 + r * i/n);
        }
    }

    return G;
}

double draw_time_poisson(vector<double> L) {
    double lambda = 0.0;
    for(int i = 0; i < L.size(); i++) {
        lambda += L[i];
    }
    random_device rd;
    mt19937 gen(rd());
    poisson_distribution<int> pd(lambda);
    return pd(gen);
}

int draw_random_number(vector<double> draw_prob, string type) {
    random_device rd;
    mt19937 gen(rd());

    double sum = 0.0;
    for(int i = 0; i < draw_prob.size(); i++) {
        sum += draw_prob[i];
    }

    vector<double> prob(draw_prob.size(), 0.0);
    for(int i = 0; i < draw_prob.size(); i++) {
        prob[i] = draw_prob[i] / sum;
    }

    // cout << type;
    // for(int t = 0; t < prob.size(); t++) {
    //     cout << prob[t] << " ";
    // }
    // cout << "\n";

    discrete_distribution<int> dd(prob.begin(), prob.end());

    return dd(gen);
}

vector<double> randomize_initial_distribution(int m, int n) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dis(0, n);

    vector<double> G(m, 0.0);
    for(int i = 0; i < G.size(); i++) {
        G[i] = dis(gen);
    }

    vector<double> u(n + 1, 0.0);
    for(int i = 0; i < G.size(); i++) {
        u[G[i]] += 1.0/m;
    }

    return u;
}

// vector<double> uniform_initial_distribution(int m, int n) {
//     vector<double> u(n + 1, 0.0);
//     double sum = 0;
//     for (int i = 0; i < n+1; i += n/m) {
//         u[i] += 1.0/m;
//         sum += u[i];
//     }
//     return u;
// }

int main(int argc, char** argv) {
    if (argc != 1 && argc != 2 && argc != 7) {
        cout << "Usage: ./main [output_path]" << endl;
        cout << "or: ./main [output_path] [m] [n] [r] [s] [full_output=0,1]" << endl;
        return 1;
    }
    bool full_output = 0;

    // default to std::cout
    std::ostream* output_stream = &std::cout;

    // if given output file path change stream to filestream
    std::fstream file;
    if (argc >= 2) {
        file.open(argv[1], std::fstream::out);
        if (!file.is_open()) {
            file = fstream(argv[1], std::fstream::out);
        }
        output_stream = &file;
    }

    int m = 50; // number of groups
    int n = 50; // number of individuals in a group

    double r = 0.1; // proportionality constant
    double s = 0.05; // proportionality constant
    
    if (argc == 7) {
        m = std::stoi(argv[2]);
        n = std::stoi(argv[3]);
        r = std::stod(argv[4]);
        s = std::stod(argv[5]);
        full_output = std::stoi(argv[6]);
    }
    // std::cout << m << " " << n << " " << r << " " << s << endl;

    *output_stream << m << " " << n << " " << r << " " << s << endl;

    // groups[i] is the proportion of groups that have i G type individuals, where i in [0..n]
    vector<double> u = randomize_initial_distribution(m, n); // initial distribution of balls in groups

    // // assume 2 groups with 1 G type individual, 1 group with 2 G type individuals, 1 group with 0 G type individuals
    // u[0] = 0.0/m;
    // u[1] = 2.0/m;
    // u[2] = 1.0/m;
    // u[3] = 1.0/m;

    double T = 0.0; // time

    while(fabs(u[0] - 1.0) > 1e-8 && fabs(u[n] - 1.0) > 1e-8) {
        // cout << "U: ";
        if (full_output) {
            *output_stream << T << " ";
            for (int i = 0; i < u.size(); i++) {
                *output_stream << " " << u[i];
            }
            *output_stream << endl;
        }

        // rate of balls leaving each group
        vector<double> L = get_leaving_rates(u, m, n, r, s);

        // draw time to next event from poisson distribution
        double tau = draw_time_poisson(L);
        // cout << "tau: " << tau << endl;

        // draw random number I1, group that the individual is drawn from
        int I1 = draw_random_number(L, "(L) = Drawing Group Prob: ");
        // cout << "Drawing Group Index: " << I1 << endl;

        // draw random number I2, group that the individual is placed in
        vector<double> G = get_incoming_rates(u, m, n, r, s, I1);
        int I2 = draw_random_number(G, "(G) = Placed Group Prob: ");
        // cout << "Placed Group Index: " << I2 << endl;

        // update u and t
        u[I1] -= 1.0/m;
        u[I2] += 1.0/m;
        T += tau;

        // cout << "Time Taken for Current Event: " << tau << endl;
        // cout << "Total Time: " << T << endl;

        // cout << "\n";
    }

    // cout << "Final U: ";
    *output_stream << T << " ";
    for (int i = 0; i < u.size(); i++) {
        *output_stream << " " << u[i];
    }
    *output_stream << endl;

    // cout << "Total Time Taken: " << T << endl;


    // ------- OUTPUT FORMAT -------
    // First Line: m n r s
    // Other Lines: T u[0] u[1] ...

    return 0;
}
