import argparse
import csv
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument('file', help='csv to graph from')
args = parser.parse_args()

distance, force, energy, time = [], [], [], []

with open(args.file, newline='') as csvfile:
    datareader = csv.reader(csvfile, delimiter=',', quotechar='|')
    labels = next(datareader)
    for data in datareader:
        distance.append(float(data[0]))
        energy.append(float(data[1]))
        force.append(float(data[2]))
        time.append(float(data[3]))

fig, ax = plt.subplots(3)
# fig.suptitle

ax.plot(time, distance)
ax.set(xlabel=labels[3], ylabel=labels[0])
plt.show()
