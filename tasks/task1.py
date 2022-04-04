# This is essentially a tester for two algorithms
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import HOSTS, HOSTS_PORT, get_pssh_client

import gevent

"""
Run this command in the top-level directory, i.e. python tasks/task1.py
"""
if __name__ == "__main__":
    client = get_pssh_client()
    copy_greenlets = client.copy_file(".", ".", recurse=True)
    gevent.joinall(copy_greenlets, raise_error=True)

    for alg in ["ring", "recur_hd"]:
        output = client.run_command(
            f"python3 tasks/task_driver.py --alg={alg} --master_ip=10.10.1.1 --rank=%d --vec_size=16 --num_nodes=16 --print", host_args=tuple(r for r in range(16)))

        idx = 0
        for host_output in output:
            print(f">>> Host {idx} result:")
            exit_code = host_output.exit_code
            if exit_code and exit_code != 0:
                print(f"Error! code {host_output.exit_code}")
                for line in host_output.stdout:
                    print(line)
                for line in host_output.stderr:
                    print(line)
            else:
                for line in host_output.stdout:
                    print(line)
            idx += 1
