#
# Task 1 wrapper script.
#

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands, copy_file


"""
Run this command in the top-level directory, i.e. python tasks/task1.py
"""
if __name__ == "__main__":
    copy_file(".", ".", recurse=True)

    for alg in ["ring", "recur_hd"]:
        commands = [
            f"python3 tasks/task_driver.py --alg={alg} --master_ip=10.10.1.1 --rank=%d --vec_size=16 --num_nodes=16 --print"
        ]
        host_args_list = [
            tuple(r for r in range(16))
        ]
        run_commands(commands, host_args_list=host_args_list)
