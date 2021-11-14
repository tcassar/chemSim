import argparse
import csv
import matplotlib.pyplot as plt
import sys


def parse_csv(source):
    datareader = csv.reader(source, delimiter=',', quotechar='|')
    headers = next(datareader)
    for data in datareader:
        distance.append(float(data[0]))
        energy.append(float(data[1]))
        force.append(float(data[2]))
        time.append(float(data[3]))
    return headers


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='csv to graph from')
args = parser.parse_args()

distance, force, energy, time = [], [], [], []

if args.file:
    with open(args.file, newline='') as csvfile:
        labels = parse_csv(csvfile)
else:
    csv_stdin = sys.stdin.read().splitlines()
    labels = parse_csv(csv_stdin)

fig, axs = plt.subplots(3)
fig.suptitle("Plots of Distance, Energy and Force against time")

axs[0].plot(time, distance)
axs[0].set(xlabel=labels[3], ylabel=labels[0])

axs[1].plot(time, energy)
axs[1].set(xlabel=labels[3], ylabel=labels[1])

axs[2].plot(time, force)
axs[2].set(xlabel=labels[3], ylabel=labels[2])
plt.show()
