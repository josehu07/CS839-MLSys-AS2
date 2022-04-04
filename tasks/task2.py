#
# Task 2 wrapper script.
#

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands, copy_file


"""
Run this command in the top-level directory, i.e. python tasks/task2.py
"""
if __name__ == "__main__":
    copy_file(".", ".", recurse=True)

    for sz in ["1KB", "10KB", "100KB", "1MB", "10MB", "100MB"]:
        for alg in ["ring", "recur_hd"]:
            commands = [
                f"python3 tasks/task_driver.py --alg={alg} --master_ip=10.10.1.1 --rank=%d --vec_size={sz} --num_nodes=16"
            ]
            host_args_list = [
                tuple(r for r in range(16))
            ]
            print(f"--- sz={sz}, num_nodes=16, alg={alg} ---")
            run_commands(commands, host_args_list=host_args_list)
