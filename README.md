# CS839 MLSys Collective Communication Assignment

CS839 MLSys @ UW-Madison, SP2022. Assignment 2 on collective communication.

Install `parallel-ssh` tool:

```bash
pip3 install parallel-ssh
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

To run task 1 to 4, execute the command below at the root path of this repository:

```bash
python3 tasks/task<x>.py    # replace <x> with 1~4
```

The core source code for the two AllReduce algorithms are at:

* `tasks/allreduce_ring.py`: "Ring" algorithm
* `tasks/allreduce_recur_hd.py`: Recursive Halving and Doubling algorithm

TODO
