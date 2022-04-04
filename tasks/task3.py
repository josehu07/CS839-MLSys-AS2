#
# Task 3 wrapper script.
#

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands, copy_file


"""
Run this command in the top-level directory, i.e. python tasks/task3.py
"""
if __name__ == "__main__":
    copy_file(".", ".", recurse=True)

    for num_nodes in [2, 4, 8, 16]:
        for alg in ["ring", "recur_hd"]:
            commands = [
                f"python3 tasks/task_driver.py --alg={alg} --master_ip=10.10.1.1 "
                f"--rank=%d --vec_size=10MB --num_nodes={num_nodes} --tag=task3-tag"
            ]
            host_args_list = [
                tuple(r for r in range(num_nodes))
            ]
            print(f"--- sz=10MB, num_nodes={num_nodes}, alg={alg} ---")
            run_commands(commands, num_nodes=num_nodes, host_args_list=host_args_list)
