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
                print("mismatch")
                continue
            t.append(float(numbers[0]))
            numbers = np.array([float(x) for x in numbers[1:]])
            data.append(numbers)
        data = np.array(data).T
    return m, n, r, s, lambda_rate, w_i, w_g, data, t

def visualize_distribution_of_groups_over_time(file_paths, model):
    raw_data = None
    raw_time = None
    for file_path in file_paths:
        if model == 0:
            _, _, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        else:
            _, _, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
        if raw_data.shape[0] < 3:
            for i in range(raw_data.shape[0]):
                if i == 0:
                    plt.plot(raw_time, raw_data[i], color="r")
                elif i == raw_data.shape[0]-1:
                    plt.plot(raw_time, raw_data[i], color="b")
                else:
                    plt.plot(raw_time, raw_data[i], color="grey")
        else:
                    plt.plot(raw_time, raw_data[0]*100, color="r", label="0/"+str(raw_data.shape[0]-1)+" type G individuals")
                    plt.plot(raw_time, raw_data[raw_data.shape[0]-1]*100, color="blue", label=str(raw_data.shape[0]-1)+"/"+str(raw_data.shape[0]-1)+" type G individuals")
        plt.title("Percentage of Groups with No Cooperators and Only Cooperators Over Time (m=100, n=100)")
        plt.xlabel("Time")
        plt.ylabel("% of groups")
        plt.legend()
        plt.show()

def visualize_distribution_of_groups_over_time_single_file(file_path, model):
    raw_data = None
    raw_time = None
    if model == 0:
        _, _, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
    else:
        _, _, _, _, _, _, _, raw_data, raw_time = read_data(file_path, model)
    if raw_data.shape[0] < 3:
        for i in range(raw_data.shape[0]):
            if i == 0:
                plt.plot(raw_time, raw_data[i], color="r")
            elif i == raw_data.shape[0]-1:
                plt.plot(raw_time, raw_data[i], color="b")
            else:
                plt.plot(raw_time, raw_data[i], color="grey")
    else:
                plt.plot(raw_time, raw_data[0]*100, color="r", label="0/"+str(raw_data.shape[0]-1)+" type G individuals")
                plt.plot(raw_time, raw_data[raw_data.shape[0]-1]*100, color="blue", label=str(raw_data.shape[0]-1)+"/"+str(raw_data.shape[0]-1)+" type G individuals")
    plt.title("Percentage of Groups with No Cooperators and Only Cooperators Over Time (m=100, n=100)")
    plt.xlabel("Time")
    plt.ylabel("% of groups")
    plt.legend()
    plt.show()

    # # use index range
    # data = []
    # filepath = file_paths[0]
    # for i in range(len(file_paths)):
    #     # filepath = sys.argv[1]+"/"+file_paths[i]
    #     _, _, _, _, raw_data, raw_time = read_data(filepath)
    #     data.append(raw_data)

    # # TODO
    # # use time range
    # # for i in range(1, len(sys.argv)):
    # #     filepath = sys.argv[i]
    # #     raw_data, raw_time = read_data(filepath)
    # #     if min_t_points == -1 or min_t_points > len(raw_time):
    # #         min_t_points = len(raw_time)
    # #     # sim_data = split_by_time_increment(raw_data, raw_time, m, n, start_t, end_t, increment_t)
    # #     # data += sim_data/sim_count
    # #     if len(data) == 0:
    # #         data = raw_data
    # 
    # if sim_count == 1:
    #     plt.plot(data[0][0], color='red')
    #     plt.plot(data[0][25], color='green')
    #     plt.plot(data[0][50], color='blue')
    # else:
    #     max_len = 0
    #     for i in range(sim_count):
    #         if len(data[i][0]) > max_len:
    #             max_len = len(data[i][0])
    #     avg = np.zeros((data[0].shape[0], max_len))
    #     for i in range(sim_count):
    #         avg[:, :data[i].shape[1]] += data[i] / sim_count
    #     # plt.plot(avg[0], color='red')
    #     # plt.plot(avg[25], color='green')
    #     # plt.plot(avg[50], color='blue')
    #     # for i in range(10):
    #     #     plt.bar(x, avg[i,0:10])
    #     df = pd.DataFrame(avg[:,:10000:1000].T)
    #     df.plot(kind="bar", stacked=True)
    # plt.show()
    return
# # TODO
# def split_by_time_increment(raw_data, raw_time, m, n, start_t, end_t, increment_t):
#     data = np.array([np.array([0 for _ in range(start_t, end_t, increment_t)], dtype=np.float64) for _ in range(m+1)])
#     prev_data = raw_data[:,0]
#     prev_t = 0
#     t = 0
#     for i in range(len(raw_data[0])):
#         if raw_time[i] < t and prev_t <= raw_time[i]:
#             print(f"data in interval [{prev_t},{t})")
#             data[:,i] = raw_data[:,i]
#             prev_data = data[:, i]
#             t += increment_t
#         elif raw_time[i] >= t:
#             data[:,i] = prev_data
#             prev_data = data[:, i]
#             t += increment_t
#         # else: raw_time < prev_t
# 
# 
#     return data

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
        plt.title("Probability of Fixation to Type G Individuals")
        plt.xlabel("Number of Individuals per Group (n)")
        plt.ylabel("Number of Groups (m)")
        plt.show()

    # line plot
    for i in range(0, n_group_count, 2):
        plt.plot(m_ticks, data[:, i], marker='o', linestyle='-', label="n="+str(sim_shape[1][0]+i*sim_shape[1][2]))
    plt.title("Probability of Fixation to Type G Individuals")
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
    file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    visualize_distribution_of_groups_over_time(file_paths, model)
    # ----- or -----
    # visualize_distribution_of_groups_over_time_single_file(sys.argv[1], model)
    # -----------------------------------------------------------------

    # fixation probability (python3 ./main.py [data directory])
    # -----------------------------------------------------------------
    # file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # sim_shape = ((20, 200, 20), (20, 200, 20), 100)
    # visualize_fixation_probabilities(file_paths, sim_shape, model)
    # -----------------------------------------------------------------

    # fixation time (python3 ./main.py [data directory])
    # -----------------------------------------------------------------
    # file_paths = [os.path.abspath(sys.argv[1] + "/" + x) for x in os.listdir(sys.argv[1])]
    # sim_shape = ((20, 200, 20), (20, 200, 20), 100)
    # visualize_fixation_times(file_paths, sim_shape, model)
    # -----------------------------------------------------------------

if __name__ == "__main__":
    main()
