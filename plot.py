#
# Plotting scripts for the report.
#

import matplotlib
matplotlib.use('Agg')

import argparse
import matplotlib.pyplot as plt
import numpy as np


def standard_error(arr):
    arr_np = np.array(arr)
    return np.std(arr_np, ddof=1) / np.sqrt(np.size(arr_np))


def read_task2(csv):
    result = {
        'vsizes': [],
        'ring': {
            'avg': [],
            'err': []
        },
        'recur_hd': {
            'avg': [],
            'err': []
        }
    }

    with open(csv, 'r') as fcsv:
        curr_run = []

        for line in fcsv.readlines():
            line = line.strip()
            segs = line.split(', ')
            assert len(segs) == 6
            assert segs[0] == "task2-tag"

            size = segs[1]
            alg = segs[3]
            time = float(segs[5])

            if len(result['vsizes']) == 0 or size != result['vsizes'][-1]:
                result['vsizes'].append(size)
            curr_run.append(time)

            num_nodes = int(segs[2])
            node_id = int(segs[4])
            if node_id == num_nodes - 1:
                avg = sum(curr_run) / len(curr_run)
                err = standard_error(curr_run)
                result[alg]['avg'].append(avg)
                result[alg]['err'].append(err)
                curr_run = []

    return result

def plot_task2(result, out):
    xticks = result['vsizes']
    xs = range(len(xticks))

    yticks_pos = [0.1, 1, 10]

    markers = {'ring': 'o', 'recur_hd': '^'}
    for alg in ('ring', 'recur_hd'):
        ys = result[alg]['avg']
        # yerrs = result[alg]['err']

        plt.plot(xs, ys, zorder=3, label=alg, marker=markers[alg])

    plt.yscale('log')

    plt.xticks(xs, xticks)
    plt.yticks(yticks_pos, [str(y) for y in yticks_pos])

    plt.xlabel("Vector Size")
    plt.ylabel("Completion Time (s)")

    plt.legend()

    plt.savefig(out, dpi=120)
    plt.close()


def read_task3(csv):
    result = {
        'nodes': [],
        'ring': {
            'avg': [],
            'err': []
        },
        'recur_hd': {
            'avg': [],
            'err': []
        }
    }

    with open(csv, 'r') as fcsv:
        curr_run = []

        for line in fcsv.readlines():
            line = line.strip()
            segs = line.split(', ')
            assert len(segs) == 6
            assert segs[0] == "task3-tag"

            num_nodes = int(segs[2])
            alg = segs[3]
            time = float(segs[5])

            if len(result['nodes']) == 0 or num_nodes != result['nodes'][-1]:
                result['nodes'].append(num_nodes)
            curr_run.append(time)

            node_id = int(segs[4])
            if node_id == num_nodes - 1:
                avg = sum(curr_run) / len(curr_run)
                err = standard_error(curr_run)
                result[alg]['avg'].append(avg)
                result[alg]['err'].append(err)
                curr_run = []

    return result

def plot_task3(result, out):
    xs = result['nodes']

    markers = {'ring': 'o', 'recur_hd': '^'}
    for alg in ('ring', 'recur_hd'):
        ys = result[alg]['avg']
        # yerrs = result[alg]['err']

        plt.plot(xs, ys, zorder=3, label=alg, marker=markers[alg])

    plt.xticks(xs, xs)

    plt.xlabel("Number of Nodes")
    plt.ylabel("Completion Time (s)")

    plt.legend()

    plt.savefig(out, dpi=120)
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task", choices=[2, 3], required=True, type=int)
    parser.add_argument("--csv", required=True, type=str)
    parser.add_argument("--out", required=True, type=str)
    args = parser.parse_args()

    plt.rcParams.update({'font.size': 12})

    if args.task == 2:
        result = read_task2(args.csv)
        plot_task2(result, args.out)
    else:
        result = read_task3(args.csv)
        plot_task3(result, args.out)
