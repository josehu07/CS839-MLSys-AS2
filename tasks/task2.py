import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import HOSTS, HOSTS_PORT, get_pssh_client

import gevent

"""
Run this command in the top-level directory, i.e. python tasks/task2.py
"""
if __name__ == "__main__":
    client = get_pssh_client()
    copy_greenlets = client.copy_file(".", ".", recurse=True)
    gevent.joinall(copy_greenlets, raise_error=True)

    for sz in ["1KB", "10KB", "100KB", "1MB", "10MB", "100MB"]:
        for alg in ["ring", "recur_hd"]:
            print(f"--- sz={sz}, num_nodes=16, alg={alg} ---")
            output = client.run_command(
                f"python3 tasks/task_driver.py --alg={alg} --master_ip=10.10.1.1 --rank=%d --vec_size={sz} --num_nodes=16", host_args=tuple(r for r in range(16)))

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
