#
# Task 4: estimate alpha & beta values.
#

import argparse
import math
import numpy as np
from sklearn.linear_model import LinearRegression


def get_tensor_size(size_str):
    if size_str.endswith("MB"):
        return float(size_str[:-2])
    if size_str.endswith("KB"):
        return float(size_str[:-2]) / 1024
    if size_str.endswith("B"):
        return float(size_str[:-1]) / (1024 * 1024)
    return float(size_str)

def read_task2(csv):
    result = {
        'vsizes': [],
        'ring': [],
        'recur_hd': []
    }

    with open(csv, 'r') as fcsv:
        curr_run = []

        for line in fcsv.readlines():
            line = line.strip()
            segs = line.split(', ')
            assert len(segs) == 6
            assert segs[0] == "task2-tag"

            size = get_tensor_size(segs[1])
            alg = segs[3]
            time = float(segs[5])

            if len(result['vsizes']) == 0 or size != result['vsizes'][-1]:
                result['vsizes'].append(size)
            curr_run.append(time)

            num_nodes = int(segs[2])
            node_id = int(segs[4])
            if node_id == num_nodes - 1:
                avg = sum(curr_run) / len(curr_run)
                result[alg].append(avg)
                curr_run = []

    return result


def solve_linear_regression(xs, ys):
    xs, ys = np.array(xs), np.array(ys)
    xs = xs.reshape((-1, 1))    # requires 2D X column vector
    model = LinearRegression().fit(xs, ys)
    assert len(model.coef_) == 1

    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(xs, ys)
    return slope, intercept, r_squared

def calculate_params_for_alg(alg, num_nodes, slope, intercept):
    if alg == 'ring':
        alpha = intercept / (num_nodes - 1)
        beta = slope / ((num_nodes - 1) / num_nodes)
        return alpha, beta
    else:
        alpha = intercept / math.log(num_nodes, 2)
        beta = slope / math.log(num_nodes, 2)
        return alpha, beta

def estimate_params(result):
    """
    Use linear regression to get estimated values for alpha & beta.

      ring:     T = (p-1) * alpha + ((p-1)/p) * n * beta
                  = ((p-1)/p) * beta * n + (p-1) * alpha
                    ------ a ------- * x + ----- b -----

      recur_hd: T = log(p) * (alpha + n * beta)
                  = log(p) * beta * n + log(p) * alpha
                    ----- a ----- * x + ----- b ------

    number of nodes p = 16 in task2, vector size n measured in MB

    We assume that doing the reduction operation (vector add) is cheap
    enough to be negligible.
    """
    print("alg, alpha, beta_in_MB, r_squared")
    for alg in ('ring', 'recur_hd'):
        xs = result['vsizes']
        ys = result[alg]
        
        slope, intercept, r_squared = solve_linear_regression(xs, ys)
        alpha, beta = calculate_params_for_alg(alg, 16, slope, intercept)
        print(f"{alg}, {alpha:.6f}, {beta:.6f}, {r_squared:.6f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task2_csv", required=True, type=str)
    args = parser.parse_args()

    result = read_task2(args.task2_csv)
    estimate_params(result)
