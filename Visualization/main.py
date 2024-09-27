import sys

import matplotlib.pyplot as plt
import numpy as np

def visualize_distribution_of_groups_over_time(filepath):
    with open(filepath, 'r') as f:
        data = []
        T = []
        for line in f:
            numbers = line.split()
            if len(numbers) == 1:
                T.append(float(numbers[0]))
            else:
                numbers = np.array([float(x) for x in numbers])
                data.append(numbers)
        data = np.array(data).T
        plt.plot(T, data[0], color='red', )
        plt.plot(T, data[25], color='green')
        plt.plot(T, data[50], color='blue')
        plt.legend
        # for i in range(len(data)):
        #     plt.plot(T, data[i])
        plt.show()
    return

def main():
    if len(sys.argv) != 2:
        print("Usage ./main.py [filename]")
        return

    visualize_distribution_of_groups_over_time(sys.argv[1])

if __name__ == "__main__":
    main()
