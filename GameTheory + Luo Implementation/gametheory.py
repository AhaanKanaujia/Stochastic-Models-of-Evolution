import numpy as np
import random

def print_vector(v, title):
    print(title, " ".join(map(str, v)))

def get_coop_payoff(payoff, n):
    R, S = payoff[0][0], payoff[0][1]
    pi_c = [R * i / n + S * (n - i) / n for i in range(n + 1)]
    return pi_c

def get_def_payoff(payoff, n):
    T, P = payoff[1][0], payoff[1][1]
    pi_d = [T * i / n + P * (n - i) / n for i in range(n + 1)]
    return pi_d

def get_group_payoff(payoff, n):
    R, S = payoff[0][0], payoff[0][1]
    T, P = payoff[1][0], payoff[1][1]

    pi_c = [R * i / n + S * (n - i) / n for i in range(n + 1)]
    pi_d = [T * i / n + P * (n - i) / n for i in range(n + 1)]
    G = [(i * pi_c[i] + (n - i) * pi_d[i]) / n for i in range(n + 1)]

    return G

def get_leaving_rates(u, m, n, G, pi_c, pi_d, lambd, w_i, w_g):
    lambda_u = [lambd * u[i] * (1 + w_g * G[i]) for i in range(n + 1)]
    sum_lambda_u = sum(lambda_u)
    inv_n = 1.0 / n

    L = [m * u[0] * (sum_lambda_u - lambda_u[0])]
    for i in range(1, n):
        term_sum = sum_lambda_u - lambda_u[i]
        coop_def_sum = m * u[i] * (n - i) * i * inv_n * (2 + w_i * (pi_d[i] + pi_c[i]))
        L.append(coop_def_sum + m * u[i] * term_sum)
    L.append(m * u[n] * (sum_lambda_u - lambda_u[n]))

    return L

def get_incoming_rates(u, m, n, G_payoff, pi_c, pi_d, lambd, I1, w_i, w_g):
    G = [0.0] * (n + 1)
    inv_n = 1.0 / n
    I1_inv_n = I1 * inv_n
    one_minus_I1_inv_n = 1 - I1_inv_n

    if I1 < n:
        G[I1 - 1] = (n - I1) * (1 + w_i * pi_d[I1]) * I1_inv_n + u[I1 - 1] * lambd * (1 + w_g * G_payoff[I1 - 1])
    if I1 > 0:
        G[I1 + 1] = I1 * one_minus_I1_inv_n * (1 + w_i * pi_c[I1]) + u[I1 + 1] * lambd * (1 + w_g * G_payoff[I1 + 1])

    for i in range(n + 1):
        if abs(i - I1) > 1:
            G[i] = u[i] * lambd * (1 + w_g * G_payoff[i])

    return G

def draw_time_poisson(L):
    lambd = sum(L)
    return np.random.poisson(lambd)

def draw_random_number(draw_prob):
    prob = np.array(draw_prob)
    if np.any(prob < 0):
        raise ValueError(f"Negative probabilities in draw_prob: {prob}")
    prob /= sum(prob)
    return np.random.choice(len(draw_prob), p=prob)

def randomize_initial_distribution(m, n):
    G = [random.randint(0, n) for _ in range(m)]
    u = [0.0] * (n + 1)
    inv_m = 1.0 / m

    for g in G:
        u[g] += inv_m

    return u

def main():
    # Parameters
    m = 100  # number of groups
    n = 100  # number of individuals in a group
    lambd = 0.1  # group-level events rate
    w_i = 0.01  # individual-level events weight
    w_g = 0.01  # group-level events weight

    reward, sucker, temptation, punishment = 2, -1, 1, 0
    payoff = [[reward, sucker], [temptation, punishment]]

    # Calculate payoff values
    pi_c = get_coop_payoff(payoff, n)
    pi_d = get_def_payoff(payoff, n)
    G_payoff = get_group_payoff(payoff, n)

    # Initialize distribution
    u = randomize_initial_distribution(m, n)
    T = 0.0
    inv_m = 1.0 / m

    print("Initial distribution (u):", u)

    while abs(u[0] - 1.0) > 1e-8 and abs(u[n] - 1.0) > 1e-8:
        # Get leaving rates and validate
        L = get_leaving_rates(u, m, n, G_payoff, pi_c, pi_d, lambd, w_i, w_g)
        print("Leaving Rates (L):", L)  # Debugging log
        
        if any(l < 0 for l in L):
            raise ValueError(f"Negative values in leaving rates (L): {L}")

        if sum(L) == 0:
            raise ValueError("Sum of leaving rates (L) is zero, unable to draw random numbers.")

        # Draw time and group indices
        tau = draw_time_poisson(L)
        I1 = draw_random_number(L)

        # Get incoming rates and validate
        G = get_incoming_rates(u, m, n, G_payoff, pi_c, pi_d, lambd, I1, w_i, w_g)
        print("Incoming Rates (G):", G)  # Debugging log

        if any(g < 0 for g in G):
            raise ValueError(f"Negative values in incoming rates (G): {G}")

        if sum(G) == 0:
            raise ValueError("Sum of incoming rates (G) is zero, unable to draw random numbers.")

        I2 = draw_random_number(G)

        # Update distribution
        u[I1] -= inv_m
        u[I2] += inv_m
        T += tau

        # Debugging log for each iteration
        print(f"Iteration Time: {T}, Updated Distribution (u): {u}")

    # Final output
    print("Final Distribution (u):", u)
    print("Total Time Taken:", T)


if __name__ == "__main__":
    main()