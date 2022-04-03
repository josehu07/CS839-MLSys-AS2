import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import HOSTS, HOSTS_PORT, get_pssh_client

import gevent

"""
Run this command in the top-level directory, i.e. python tasks/task3.py
"""
if __name__ == "__main__":
    client = get_pssh_client()
    copy_greenlets = client.copy_file(".", ".", recurse=True)
    gevent.joinall(copy_greenlets, raise_error=True)

    for num_nodes in [2, 4, 8, 16]:
        for alg in ["ring", "recur_hd"]:
            print(f"--- sz=10MB, num_nodes={num_nodes}, alg={alg} ---")
            output = client.run_command(
                f"python3 tasks/task_driver.py --alg={alg} --master_ip=172.16.206.1 --rank=%d --vec_size=10MB --num_nodes={num_nodes} --print", host_args=tuple(r for r in range(num_nodes)))

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
