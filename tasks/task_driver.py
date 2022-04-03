import argparse
import sys
import os
import time
import torch
from allreduce_recur_hd import AllReduceRecurHD
from allreduce_ring import AllReduceRing


def get_tensor_size(size_str: str):
    # pytorch use float32 by default, i.e. 4B for each vector element
    # it can directly accept the length of the vector e.g. 16
    # it can also accept size specified by B/KB/MB
    if size_str.endswith("MB"):
        return int(size_str[:-2]) * 1024 * 1024 / 4
    if size_str.endswith("KB"):
        return int(size_str[:-2]) * 1024 / 4
    if size_str.endswith("B"):
        return int(size_str[:-1]) / 4
    return int(size_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--alg", choices=["ring", "recur_hd"], required=True, type=str)
    parser.add_argument("--master_ip", required=True, type=str)
    parser.add_argument("--rank", required=True, type=int)
    parser.add_argument("--vec_size", required=True, type=str)
    parser.add_argument("--num_nodes", required=True, type=int)
    parser.add_argument("--print", required=False, action="store_true")
    args = parser.parse_args()
    vec_size = get_tensor_size(args.vec_size)

    if args.alg == "ring":
        alg_type = AllReduceRing
        print(f"Rank {args.rank}: Use Ring AllReduce algorithm.")
    else:
        alg_type = AllReduceRecurHD
        print(f"Rank {args.rank}: Use Recursive Halving and Doubling algorithm.")

    alg = alg_type(master_ip=args.master_ip,
                   rank=args.rank, world_size=args.num_nodes, vec_size=vec_size)

    vec = torch.rand(vec_size)
    t0 = time.time()
    vec_reduced = alg.run(vec)
    t1 = time.time()

    print(f"Rank {args.rank}: {t1 - t0:.3f} s")

    if args.print:
        print(vec_reduced)
