#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <string>

using namespace std;

void print_vector(vector<double> v, string title) {
    cout << title;
    for (int i = 0; i < v.size(); i++) {
        cout << v[i] << " ";
    }
    cout << "\n";
}

vector<double> get_coop_payoff(vector< vector<double> > payoff, int n) {
    double R = payoff[0][0];
    double S = payoff[0][1];
    double T = payoff[1][0];
    double P = payoff[1][1];

    // cooperator payoffs for every group
    vector<double> pi_c(n + 1, 0.0);
    for (int i = 0; i < n + 1; i++) {
        pi_c[i] = R * i / n + S * (n - i) / n;
    }

    return pi_c;
}

vector<double> get_def_payoff(vector< vector<double> > payoff, int n) {
    double R = payoff[0][0];
    double S = payoff[0][1];
    double T = payoff[1][0];
    double P = payoff[1][1];

    // defector payoffs for every group
    vector<double> pi_d(n + 1, 0.0);
    for (int i = 0; i < n + 1; i++) {
        pi_d[i] = T * i / n + P * (n - i) / n;
    }

    return pi_d;
}

vector<double> get_group_payoff(vector< vector<double> > payoff, int n) {
    double R = payoff[0][0];
    double S = payoff[0][1];
    double T = payoff[1][0];
    double P = payoff[1][1];

    // cooperator payoffs for every group
    vector<double> pi_c(n + 1, 0.0);
    for (int i = 0; i < n + 1; i++) {
        pi_c[i] = R * i / n + S * (n - i) / n;
    }

    // defector payoffs for every group
    vector<double> pi_d(n + 1, 0.0);
    for (int i = 0; i < n + 1; i++) {
        pi_d[i] = T * i / n + P * (n - i) / n;
    }

    // average payoff values of groups with different number of cooperators
    vector<double> G(n + 1, 0.0);
    for (int i = 0; i < n + 1; i++) {
        G[i] = (i * pi_c[i] + (n - i) * pi_d[i]) / n;
    }

    return G;
}

vector<double> get_leaving_rates(const vector<double>& u, int m, int n, const vector<double>& G, const vector<double>& pi_c, const vector<double>& pi_d, double lambda, double w_i, double w_g) {
    vector<double> L;
    L.reserve(n + 1);
    
    double group_level_sum = 0.0;
    for (int i = 0; i < n + 1; i++) {
        group_level_sum += u[i] * exp(w_g * G[i]);
    }

    for (int i = 0; i < n + 1; i++) {
        double coop_def_sum = i * exp(w_i * pi_c[i]) + (n - i) * exp(w_i * pi_d[i]);
        double coop_def = (m * u[i] * (n - i) * i * exp(w_i * pi_c[i]) + m * u[i] * (n - i) * i * exp(w_i * pi_d[i])) / coop_def_sum;
        double group = m * u[i] * lambda * (group_level_sum - u[i] * exp(w_g * G[i])) / group_level_sum;
        L.push_back(coop_def + group);
    }

    return L;
}

vector<double> get_incoming_rates(const vector<double>& u, int m, int n, const vector<double>& G_payoff, const vector<double>& pi_c, const vector<double>& pi_d, double lambda, double I1, double w_i, double w_g) {
    vector<double> G(n + 1, 0.0);

    double group_pair_denom = I1 * exp(w_i * pi_c[I1]) + (n - I1) * exp(w_i * pi_d[I1]);
    double group_sum_denom = 0.0;
    for (int i = 0; i < n + 1; i++) {
        group_sum_denom += u[i] * exp(w_g * G_payoff[i]);
    }

    if (I1 > 0) {
        double term = (n - I1) * exp(w_i * pi_d[I1]) / group_pair_denom;
        G[I1 - 1] = (n - I1) * term * I1 + lambda * u[I1 - 1] * exp(w_g * G_payoff[I1 - 1]) / group_sum_denom; 
    }

    if (I1 < n) {
        double term = I1 * exp(w_i * pi_c[I1]) / group_pair_denom;
        G[I1 + 1] = I1 * term * (n - I1) + lambda * u[I1 + 1] * exp(w_g * G_payoff[I1 + 1]) / group_sum_denom;
    }

    for (int i = 0; i < n + 1; i++) {
        if (abs(i - I1) > 1) {
            G[i] = lambda * u[i] * exp(w_g * G_payoff[i]) / group_sum_denom;
        }
    }

    return G;
}

mt19937& get_random_generator() {
    static random_device rd;
    static mt19937 gen(rd());
    return gen;
}

double draw_time_poisson(const vector<double>& L) {
    double lambda = accumulate(L.begin(), L.end(), 0.0);

    poisson_distribution<int> pd(lambda);
    return pd(get_random_generator());
}

int draw_random_number(const vector<double>& draw_prob) {
    double sum = accumulate(draw_prob.begin(), draw_prob.end(), 0.0);

    vector<double> prob(draw_prob.size());
    for (size_t i = 0; i < draw_prob.size(); i++) {
        prob[i] = draw_prob[i] / sum;
    }

    discrete_distribution<int> dd(prob.begin(), prob.end());
    return dd(get_random_generator());
}

vector<double> randomize_initial_distribution(int m, int n) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dis(0, n);

    vector<double> G(m, 0.0);
    for (int i = 0; i < G.size(); i++) {
        G[i] = dis(gen);
    }

    // double inv_m = 1.0 / m;
    vector<double> u(n + 1, 0.0);
    for (int i = 0; i < G.size(); i++) {
        u[G[i]] += 1;
    }

    return u;
}

int main(int argc, char** argv) {
    if (argc != 1 && argc != 2 && argc != 8) {
        cout << "Usage: ./main [output_path]" << endl;
        cout << "or: ./main [output_path] [m] [n] [lambda] [w_i] [w_g] [full_output=0,1]" << endl;
        return 1;
    }

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
    bool full_output = 1;

    int m = 20; // number of groups
    int n = 20; // number of individuals in a group

    double lambda = 0.1; // group level events rate

    double w_i = 0.01; // individual level events
    double w_g = 0.01; // group level events
    
    if (argc == 8) {
        m = std::stoi(argv[2]);
        n = std::stoi(argv[3]);
        lambda = std::stod(argv[4]);
        w_i = std::stod(argv[5]);
        w_g = std::stod(argv[6]);
        full_output = std::stoi(argv[7]);
    }
    
    // payoff matrix
    double reward = 2;
    double sucker = -1;
    double temptation = 1;
    double punishment = 0;
    vector< vector<double> > payoff(2, vector<double>(2, 0.0));

    payoff[0][0] = reward;
    payoff[0][1] = sucker;
    payoff[1][0] = temptation;
    payoff[1][1] = punishment;

    // get cooperator payoff values
    vector<double> pi_c = get_coop_payoff(payoff, n);
    // print_vector(pi_c, "Cooperator Payoff: ");

    // get defector payoff values
    vector<double> pi_d = get_def_payoff(payoff, n);
    // print_vector(pi_d, "Defector Payoff: ");

    // get group payoff values
    vector<double> G_payoff = get_group_payoff(payoff, n);
    // print_vector(G_payoff, "Group Payoff: ");

    // cout << "\nStarting Simulation\n" << endl;

    *output_stream << m << " " << n << " " << lambda << " " << w_i << " " << w_g << endl;
    

    // groups[i] is the proportion of groups that have i G type individuals, where i in [0..n]
    vector<double> u = randomize_initial_distribution(m, n); // initial distribution of balls in groups

    double T = 0.0; // time
    
    // double inv_m = 1.0 / m;

    while(fabs(u[0] - m) > 1e-8 && fabs(u[n] - m) > 1e-8) {
        // print_vector(u, "U: ");
        if (full_output) {
            *output_stream << T << " ";
            for (int i = 0; i < u.size(); i++) {
                *output_stream << " " << u[i];
            }
            *output_stream << endl;
        }

        // rate of balls leaving each group
        vector<double> L = get_leaving_rates(u, m, n, G_payoff, pi_c, pi_d, lambda, w_i, w_g);
        // print_vector(L, "Leaving Rates: ");

        // draw time to next event from poisson distribution
        double tau = draw_time_poisson(L);
        // cout << "tau: " << tau << endl;

        // draw random number I1, group that the individual is drawn from
        // int I1 = draw_random_number(L, "(L) = Drawing Group Prob: ");
        int I1 = draw_random_number(L);
        // cout << "Drawing Group Index: " << I1 << endl;

        // draw random number I2, group that the individual is placed in
        vector<double> G = get_incoming_rates(u, m, n, G_payoff, pi_c, pi_d, lambda, I1, w_i, w_g);
        // print_vector(G, "Incoming Rates: ");

        int I2 = draw_random_number(G);
        // cout << "Placed Group Index: " << I2 << endl;

        // update u and t
        u[I1] -= 1;
        u[I2] += 1;
        T += tau;

        // cout << "Time Taken for Current Event: " << tau << endl;
        // cout << "Total Time: " << T << endl;

        // cout << "\n";
    }

    // cout << "Final U: ";
    *output_stream << T << " " << endl;
    for (int i = 0; i < u.size(); i++) {
        *output_stream << " " << u[i];
    }
    *output_stream << endl;
    // cout << "Total Time Taken: " << T << endl;

    return 0;
}
