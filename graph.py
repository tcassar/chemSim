import argparse
import csv
import matplotlib.pyplot as plt
import sys


def parse_csv(source):
    """
    Puts csv file in memory, 4 different lists; returns headers for labelling graphs, and final values for expecteds
    """
    datareader = csv.reader(source, delimiter=',', quotechar='|')
    headers = next(datareader)
    for data in datareader:
        distance.append(float(data[0]))
        energy.append(float(data[1]))
        force.append(float(data[2]))
        time.append(float(data[3]))

    expected = [distance.pop(), energy.pop(), force.pop(), time.pop()]

    return headers, expected


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='csv to graph from')
args = parser.parse_args()

distance, force, energy, time = [], [], [], []

if args.file:
    with open(args.file, newline='') as csvfile:
        labels, expected = parse_csv(csvfile)
else:
    csv_stdin = sys.stdin.read().splitlines()
    labels, expected = parse_csv(csv_stdin)

assert len(labels) > 1
assert len(expected) > 1
# print(expected)

straight_x = [time[0], time[-1]]
straight_y = lambda y: [y, y]

straight_line = lambda l: axs[l].plot(straight_x, straight_y(expected[l]))

fig, axs = plt.subplots(3)
fig.suptitle("Plots of Distance, Energy and Force against time")

axs[0].plot(time, distance)
straight_line(0)
axs[0].set(xlabel=labels[3], ylabel=labels[0])

axs[1].plot(time, energy)
straight_line(1)
axs[1].set(xlabel=labels[3], ylabel=labels[1])

axs[2].plot(time, force)
straight_line(2)
axs[2].set(xlabel=labels[3], ylabel=labels[2])
plt.show()
