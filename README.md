# CS839 MLSys Collective Communication Assignment

CS839 MLSys @ UW-Madison, SP2022. Assignment 2 on collective communication.

Install `parallel-ssh` tool, `matplotlib`, and `sklearn`:

```bash
pip3 install parallel-ssh matplotlib sklearn
```


## Machine Setup

CloudLab connection information is hardcoded in `pssh_common.py`. Setup passwordless sudoer `torchuser` on all nodes:

```bash
cd setup
python3 setup_user.py
```

Install and test CPU-based `pytorch` on all nodes:

```bash
python3 torch_inst.py
cd ..
```

If successful, should see the script outputting a tensor result on all nodes at the end. The above steps have already been completed on the current nodes.


## Running Tasks

The core source code for the two AllReduce algorithms are at:

* `tasks/allreduce_ring.py`: "Ring" algorithm
* `tasks/allreduce_recur_hd.py`: Recursive Halving and Doubling algorithm

To run all 4 tasks, execute the command below at the root path of this repository:

```bash
./run.sh
```

Check out the `task*.csv` and `task*.png` files produced for results.
