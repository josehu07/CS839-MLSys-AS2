import sys
import os
import gevent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import get_pssh_client

"""
Run this command in the top-level directory, i.e. python tasks/task3.py
"""
if __name__ == "__main__":
    client = get_pssh_client()
    copy_greenlets = client.copy_file(".", ".", recurse=True)
    gevent.joinall(copy_greenlets, raise_error=True)

    for num_nodes in [2, 4, 8, 16]:
        client = get_pssh_client(num_nodes=num_nodes)
        for alg in ["ring", "recur_hd"]:
            print(f"--- sz=10MB, num_nodes={num_nodes}, alg={alg} ---")
            output = client.run_command(
                "python3 tasks/task_driver.py --master_ip=10.10.1.1 "
                f"--alg={alg} --rank=%d --vec_size=10MB "
                f"--num_nodes={num_nodes} --tag=task3",
                host_args=tuple(r for r in range(num_nodes)))

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
