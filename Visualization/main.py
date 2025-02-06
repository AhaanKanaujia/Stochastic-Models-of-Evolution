import sys
import os

import math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def read_data(filepath, model):
    data = []
    t = []
    m = 0
    n = 0
    r = -1
    s = -1
    lambda_rate = -1
    w_i = -1
    w_g = -1
    with open(filepath, 'r') as f:
        first_list = f.readline().split()
        m = int(first_list[0])
        n = int(first_list[1])
        if model == 0:
            r = float(first_list[2])
            s = float(first_list[3])
        else:
            lambda_rate = float(first_list[2])
            w_i = float(first_list[3])
            w_g = float(first_list[4])
        for line in f:
            numbers = line.split()
            if (len(numbers) != n + 2):
                print(f"mismatch: n={n} but line has {len(numbers)} entries (need n+2={n+2})")
                continue
            t.append(float(numbers[0]))
            numbers = np.array([float(x) for x in numbers[1:]])
            data.append(numbers)
        data = np.array(data).T
    return m, n, r, s, lambda_rate, w_i, w_g, data, t

def visualize_distribution_of_groups_over_time(file_paths, model):
    m = 0
    n = 0
    raw_data = None
    raw_time = None
    highlight_groups = [int(4/8 * 100)]
    for i in range(len(file_paths)):
        file_path = file_paths[i]
        if i != 0:
            plt.figure()
        if model == 0:
            m, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        else:
            m, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        if True:
            for i in range(n+1):
                if i == 0:
                    plt.plot(raw_time, raw_data[i], color="r", label=f"0/{n} type G individuals")
                elif i == n:
                    plt.plot(raw_time, raw_data[i], color="b", label=f"{i}/{n} type G individuals")
                elif i in highlight_groups:
                    plt.plot(raw_time, raw_data[i], color="black", label=f"{i}/"+str(raw_data.shape[0]-1)+" type G individuals")
                else:
                    continue
                    plt.plot(raw_time, raw_data[i], color="grey")
        else:
                    plt.plot(raw_time, raw_data[0]*100, color="r", label="0/"+str(raw_data.shape[0]-1)+" type G individuals")
                    plt.plot(raw_time, raw_data[raw_data.shape[0]-1]*100, color="blue", label=str(raw_data.shape[0]-1)+"/"+str(raw_data.shape[0]-1)+" type G individuals")
        plt.title(f"Percentage of Groups with No Cooperators and Only Cooperators Over Time (m={m}, n={n})")
        plt.xlabel("Time")
        plt.ylabel("% of groups")
        plt.legend()
        plt.draw()
    plt.show()

def visualize_distribution_of_groups_over_time_single_file(file_path, model):
    m = 0
    n = 0
    raw_data = None
    raw_time = None
    if model == 0:
        m, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
    else:
        m, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
    if raw_data.shape[0] < 52:
        for i in range(raw_data.shape[0]):
            if i == 0:
                plt.plot(raw_time, raw_data[i], color="r", label="0/"+str(raw_data.shape[0]-1)+" type G individuals")
            elif i == raw_data.shape[0]-1:
                plt.plot(raw_time, raw_data[i], color="b", label=f"{i}/"+str(raw_data.shape[0]-1)+" type G individuals")
            else:
                plt.plot(raw_time, raw_data[i], color="grey")
    else:
                plt.plot(raw_time, raw_data[0]*100, color="r", label="0/"+str(raw_data.shape[0]-1)+" type G individuals")
                plt.plot(raw_time, raw_data[raw_data.shape[0]-1]*100, color="blue", label=str(raw_data.shape[0]-1)+"/"+str(raw_data.shape[0]-1)+" type G individuals")
    plt.title(f"Percentage of Groups with No Cooperators and Only Cooperators Over Time (m={m}, n={n})")
    plt.xlabel("Time")
    plt.ylabel("% of groups")
    plt.legend()
    plt.show()
    return

def visualize_proportion_groups_over_time(file_paths, proportion_group_count, model):
    raw_data = None
    raw_time = None
    n = 0
    for i in range(len(file_paths)):
        if i != 0:
            plt.figure()
        file_path = file_paths[i]
        if model == 0:
            _, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        else:
            _, n, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        increment = math.ceil(n / proportion_group_count)
        result = np.zeros((proportion_group_count, len(raw_time)))
        for i in range(proportion_group_count):
            # if i == 0 or i == 2:
            #     continue
            start = i * increment
            end = start + increment
            if end >= n:
                end = n + 1
            result[i] = np.sum(raw_data[start:end], axis=0)
            plt.plot(raw_time, result[i]*100, label=f"[{start},{end-1}]")
        # plt.plot(raw_time[::100], raw_data[0,::100]*100, label=f"[{0},{0}]")
        # plt.plot(raw_time[::100], raw_data[100,::100]*100, label=f"[{100},{100}]")
        plt.title("Percentage of groups within ranges of proportion of cooperators")
        plt.xlabel("Time")
        plt.ylabel("% of groups (in proportion range)")
        plt.legend()
        plt.draw()
    plt.show()

def visualize_fixation_probabilities(file_paths, sim_shape, model):
    # plot probability of fixation to type G for different values of m and n
    # Arguments:
    # - file_paths: 
    # - sim_shape:
    #   - sim_shape[0]: (start, end, increment) for m (end inclusive)
    #   - sim_shape[1]: (start, end, increment) for n (end inclusive)
    #   - sim_shape[2]: number of simulations per (m, n)

    m_group_count = math.ceil((sim_shape[0][1]+1-sim_shape[0][0])/sim_shape[0][2])
    n_group_count = math.ceil((sim_shape[1][1]+1-sim_shape[1][0])/sim_shape[1][2])

    # data: array of (m values) x (n values)
    data = np.zeros((m_group_count, n_group_count))

    m_to_idx = {}
    for i in range(m_group_count):
        m_to_idx[sim_shape[0][0]+i*sim_shape[0][2]] = i
    n_to_idx = {}
    for i in range(n_group_count):
        n_to_idx[sim_shape[1][0]+i*sim_shape[1][2]] = i

    for file_path in file_paths:
        m, n, _, _, _, _, _, raw_data, _ = read_data(file_path, model)
        if (raw_data[-1][-1] == 1.0):
            data[m_to_idx[m]][n_to_idx[n]] += 1/sim_shape[2]
    
    # heatmap
    m_ticks = np.arange(sim_shape[0][0], sim_shape[0][1]+1, sim_shape[0][2])
    n_ticks = np.arange(sim_shape[1][0], sim_shape[1][1]+1, sim_shape[1][2])
    if (m_group_count > 1 and n_group_count > 1):
        # heatmap defaults to same ordering as np.array (y-axis increases as we go down, x-axis increases as we go right)
        # swap ordering of vertical so y-axis increases upwards
        sns.heatmap(data[::-1], xticklabels=n_ticks, yticklabels=m_ticks[::-1], vmin=0, vmax=1, cbar=True)
        plt.title("Probability of Fixation to Type G Individuals (Stag Hunt)")
        plt.xlabel("Number of Individuals per Group (n)")
        plt.ylabel("Number of Groups (m)")
        plt.show()

    # line plot
    for i in range(0, n_group_count, 2):
        plt.plot(m_ticks, data[:, i], marker='o', linestyle='-', label="n="+str(sim_shape[1][0]+i*sim_shape[1][2]))
    plt.title("Probability of Fixation to Type G Individuals (Stag Hunt)")
    plt.xlabel("Number of Groups (m)")
    plt.ylabel("Probability")
    plt.legend()
    plt.show()

def visualize_fixation_times(file_paths, sim_shape, model):
    # plot time to fixation for different values of m and n
    # Arguments:
    # - file_paths: 
    # - sim_shape:
    #   - sim_shape[0]: (start, end, increment) for m (end inclusive)
    #   - sim_shape[1]: (start, end, increment) for n (end inclusive)
    #   - sim_shape[2]: number of simulations per (m, n)

    m_group_count = math.ceil((sim_shape[0][1]+1-sim_shape[0][0])/sim_shape[0][2])
    n_group_count = math.ceil((sim_shape[1][1]+1-sim_shape[1][0])/sim_shape[1][2])

    # data: array of (m values) x (n values)
    data = np.zeros((m_group_count, n_group_count))

    m_to_idx = {}
    for i in range(m_group_count):
        m_to_idx[sim_shape[0][0]+i*sim_shape[0][2]] = i
    n_to_idx = {}
    for i in range(n_group_count):
        n_to_idx[sim_shape[1][0]+i*sim_shape[1][2]] = i

    for file_path in file_paths:
        m, n, _, _, _, _, _, _, raw_time = read_data(file_path, model)
        data[m_to_idx[m]][n_to_idx[n]] += raw_time[-1]/sim_shape[2]
    
    # heatmap
    m_ticks = np.arange(sim_shape[0][0], sim_shape[0][1]+1, sim_shape[0][2])
    n_ticks = np.arange(sim_shape[1][0], sim_shape[1][1]+1, sim_shape[1][2])
    if (m_group_count > 1 and n_group_count > 1):
        # heatmap defaults to same ordering as np.array (y-axis increases as we go down, x-axis increases as we go right)
        # swap ordering of vertical so y-axis increases upwards
        sns.heatmap(np.log(data[::-1]), xticklabels=n_ticks, yticklabels=m_ticks[::-1], cbar=True)
        plt.title("Average Time to Fixation")
        plt.xlabel("Number of Individuals per Group (n)")
        plt.ylabel("Number of Groups (m)")
        plt.show()

    # line plot
    for i in range(0, n_group_count, 2):
        plt.plot(m_ticks, np.log(data[:, i]), marker='o', linestyle='-', label="n="+str(sim_shape[1][0]+i*sim_shape[1][2]))
        plt.xticks(n_ticks)
    plt.title("Average Time to Fixation")
    plt.xlabel("Number of Groups (m)")
    plt.ylabel("Time")
    plt.legend()
    plt.show()

def main():
    if len(sys.argv) < 3 or (int(sys.argv[2]) != 0 and int(sys.argv[2]) != 1):
        print("Usage ./main.py [data directory] [1: Game Theory model, 0: Luo model]")
        return
    model = sys.argv[2]
    # distribution over time (python3 ./main.py [data directory or file path])
    # -----------------------------------------------------------------
    # file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # visualize_distribution_of_groups_over_time(file_paths, model)
    # ----- or -----
    # visualize_distribution_of_groups_over_time_single_file(sys.argv[1], model)
    # -----------------------------------------------------------------

    # distribution of proportion groups (python3 ./main.py [data directory or file path])
    # -----------------------------------------------------------------
    # file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # visualize_proportion_groups_over_time(file_paths, 3, model)


    # fixation probability (python3 ./main.py [data directory])
    # -----------------------------------------------------------------
    file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # ((m start, m end, m increment), (n start, n end, n increment), number of simulations per (m,n))
    sim_shape = ((20, 100, 20), (20, 100, 20), 50)
    visualize_fixation_probabilities(file_paths, sim_shape, model)
    # -----------------------------------------------------------------

    # fixation time (python3 ./main.py [data directory])
    # -----------------------------------------------------------------
    # file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # sim_shape = ((20, 200, 20), (20, 200, 20), 100)
    # visualize_fixation_times(file_paths, sim_shape, model)
    # -----------------------------------------------------------------

if __name__ == "__main__":
    main()
