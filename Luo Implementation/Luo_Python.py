import random
import numpy as np
import csv


def get_leaving_rates(u, m, n, r, s):
    L = [0.0] * (n + 1)
    total_sum = sum(u[i] * (1 + r * i / n) for i in range(n + 1))

    for i in range(n + 1):
        term_sum = total_sum - u[i] * (1 + r * i / n)

        if i == 0 or i == n:
            L[i] = m * u[i] * term_sum
        else:
            L[i] = m * u[i] * (n - i) * i / n * (2 + s) + m * u[i] * term_sum

    return L


def get_incoming_rates(u, m, n, r, s, I1):
    G = [0.0] * (n + 1)

    for i in range(n + 1):
        if i == I1 - 1 and I1 < n:
            G[i] = (n - I1) * (1 + s) * I1 / n + u[I1 - 1] * (1 + r * (I1 - 1) / n)
        elif i == I1 + 1 and I1 > 0:
            G[i] = I1 * (1 - I1 / n) + u[I1 + 1] * (1 + r * (I1 + 1) / n)
        elif abs(i - I1) > 1:
            G[i] = u[i] * (1 + r * i / n)

    return G


def draw_time_poisson(L):
    lambda_val = sum(L)
    return np.random.poisson(lambda_val)


def draw_random_number(draw_prob, type_):
    # Ensure no negative probabilities
    draw_prob = [max(0.0, p) for p in draw_prob]  # Clamp negative values to 0

    sum_prob = sum(draw_prob)

    if sum_prob == 0:
        raise ValueError(f"All probabilities are zero. Cannot draw a random number. {type_}")

    prob = [p / sum_prob for p in draw_prob]

    # Uncomment to print probabilities
    # print(f"{type_} {prob}")

    return np.random.choice(len(prob), p=prob)



def randomize_initial_distribution(m, n):
    G = [random.randint(0, n) for _ in range(m)]
    u = [0.0] * (n + 1)

    for g in G:
        u[g] += 1.0 / m

    return u


def save_to_csv(output_filename, rows):
    # Write the rows to a CSV file
    with open(output_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Distribution"])  # Header
        for row in rows:
            writer.writerow(row)


def main():
    m = 50  # number of groups
    n = 50  # number of individuals in a group
    r = 0.1  # proportionality constant
    s = 0.05  # proportionality constant

    # Initial distribution of balls in groups
    u = randomize_initial_distribution(m, n)

    T = 0.0  # time
    output_data = []  # To store time and distribution data

    while abs(u[0] - 1.0) > 1e-8 and abs(u[n] - 1.0) > 1e-8:
        print(T)
        print(u)

        # Store current time and distribution in output_data
        output_data.append([T, u.copy()])

        L = get_leaving_rates(u, m, n, r, s)
        tau = draw_time_poisson(L)
        I1 = draw_random_number(L, "(L) = Drawing Group Prob: ")

        G = get_incoming_rates(u, m, n, r, s, I1)
        I2 = draw_random_number(G, "(G) = Placed Group Prob: ")

        u[I1] -= 1.0 / m
        u[I2] += 1.0 / m
        T += tau

    # Append the final time and distribution
    output_data.append([T, u.copy()])

    # Save output to CSV
    save_to_csv("output.csv", output_data)

    print(f"Simulation complete. Output saved to 'output.csv'.")


if __name__ == "__main__":
    main()
