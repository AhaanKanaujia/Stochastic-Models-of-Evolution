#include <iostream>
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

vector<double> get_leaving_rates(vector<double> u, int m, int n, vector<double> G, vector<double> pi_c, vector<double> pi_d, double lambda, double w_i, double w_g) {
    vector<double> L(n + 1, 0.0);

    double sum = 0.0;
    for (int i = 0; i < n + 1; i++) {
        sum += lambda * u[i] * (1 + w_g * G[i]);
    }

    for (int i = 0; i < n + 1; i++) {
        double term_sum = sum - lambda * u[i] * (1 + w_g * G[i]);

        if (i == 0 || i == n) {
            L[i] = m * u[i] * term_sum;
        } else {
            double coop_def_sum = m * u[i] * (n - i) * i/n * (2 + w_i * pi_d[i] + w_i * pi_c[i]);
            L[i] = coop_def_sum + m * u[i] * term_sum;
        }
    }

    return L;
}

vector<double> get_incoming_rates(vector<double> u, int m, int n, vector<double> G_payoff, vector<double> pi_c, vector<double> pi_d, double lambda, double I1, double w_i, double w_g) {
    vector<double> G(n + 1, 0.0);

    for (int i = 0; i < n + 1; i++) {
        if (i == I1 - 1 && I1 < n) {
            G[i] = (n - I1) * (1 + w_i * pi_d[I1]) * I1/n + u[I1 - 1] * lambda * (1 + w_g * G_payoff[I1 - 1]);
        } else if (i == I1 + 1 && I1 > 0) { 
            G[i] = I1 * (1 - I1/n) * (1 + w_i * pi_c[I1]) + u[I1 + 1] * lambda * (1 + w_g * G_payoff[I1 + 1]);
        } else if (abs(i - I1) > 1) {
            G[i] = u[i] * lambda * (1 + w_g * G_payoff[i]);
        }
    }

    return G;
}   

double draw_time_poisson(vector<double> L) {
    double lambda = 0.0;
    for (int i = 0; i < L.size(); i++) {
        lambda += L[i];
    }
    random_device rd;
    mt19937 gen(rd());

    // continuous time poisson distribution?
    poisson_distribution<int> pd(lambda);
    return pd(gen);
}

int draw_random_number(vector<double> draw_prob, string type) {
    random_device rd;
    mt19937 gen(rd());

    double sum = 0.0;
    for (int i = 0; i < draw_prob.size(); i++) {
        sum += draw_prob[i];
    }

    vector<double> prob(draw_prob.size(), 0.0);
    for (int i = 0; i < draw_prob.size(); i++) {
        prob[i] = draw_prob[i] / sum;
    }

    // print_vector(prob, type);

    discrete_distribution<int> dd(prob.begin(), prob.end());

    return dd(gen);
}

vector<double> randomize_initial_distribution(int m, int n) {
    random_device rd;
    mt19937 gen(rd());
    uniform_int_distribution<int> dis(0, n);

    vector<double> G(m, 0.0);
    for (int i = 0; i < G.size(); i++) {
        G[i] = dis(gen);
    }

    vector<double> u(n + 1, 0.0);
    for (int i = 0; i < G.size(); i++) {
        u[G[i]] += 1.0/m;
    }

    return u;
}

int main() {
    int m = 50; // number of groups
    int n = 50; // number of individuals in a group

    double lambda = 0.1; // group level events rate

    double w_i = 0.01; // individual level events
    double w_g = 0.01; // group level events
    
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

    // groups[i] is the proportion of groups that have i G type individuals, where i in [0..n]
    vector<double> u = randomize_initial_distribution(m, n); // initial distribution of balls in groups

    double T = 0.0; // time

    while(fabs(u[0] - 1.0) > 1e-8 && fabs(u[n] - 1.0) > 1e-8) {
        // print_vector(u, "U: ");

        // rate of balls leaving each group
        vector<double> L = get_leaving_rates(u, m, n, G_payoff, pi_c, pi_d, lambda, w_i, w_g);
        // print_vector(L, "Leaving Rates: ");

        // draw time to next event from poisson distribution
        double tau = draw_time_poisson(L);
        // cout << "tau: " << tau << endl;

        // draw random number I1, group that the individual is drawn from
        int I1 = draw_random_number(L, "(L) = Drawing Group Prob: ");
        // cout << "Drawing Group Index: " << I1 << endl;

        // draw random number I2, group that the individual is placed in
        vector<double> G = get_incoming_rates(u, m, n, G_payoff, pi_c, pi_d, lambda, I1, w_i, w_g);
        // print_vector(G, "Incoming Rates: ");

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

    cout << "Final U: ";
    for (int i = 0; i < u.size(); i++) {
        if (u[i] < 1e-8) cout << 0 << " ";
        else cout << u[i] << " ";
    }
    cout << "\n";

    cout << "Total Time Taken: " << T << endl;

    return 0;
}
