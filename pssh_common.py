#
# CloudLab machine SSH helpers with parallel-ssh.
#

import gevent
from typing import List

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig


HOSTS = [
    'c220g5-111204.wisc.cloudlab.us',
    'c220g5-111204.wisc.cloudlab.us',
    'c220g5-111204.wisc.cloudlab.us',
    'c220g5-111204.wisc.cloudlab.us',
    'c220g5-111209.wisc.cloudlab.us',
    'c220g5-111209.wisc.cloudlab.us',
    'c220g5-111209.wisc.cloudlab.us',
    'c220g5-111209.wisc.cloudlab.us',
    'c220g5-111215.wisc.cloudlab.us',
    'c220g5-111215.wisc.cloudlab.us',
    'c220g5-111215.wisc.cloudlab.us',
    'c220g5-111215.wisc.cloudlab.us',
    'c220g5-111217.wisc.cloudlab.us',
    'c220g5-111217.wisc.cloudlab.us',
    'c220g5-111217.wisc.cloudlab.us',
    'c220g5-111217.wisc.cloudlab.us'
]

HOSTS_PORT = [
    27610,
    27611,
    27612,
    27613,
    27610,
    27611,
    27612,
    27613,
    27610,
    27611,
    27612,
    27613,
    27610,
    27611,
    27612,
    27613,
]

HOST_CONFIG = [HostConfig(port=p, user='torchuser') for p in HOSTS_PORT]


def get_pssh_client(user='torchuser', num_nodes: int = len(HOSTS)):
    for hc in HOST_CONFIG:
        hc.user = user
    client = ParallelSSHClient(HOSTS[:num_nodes], host_config=HOST_CONFIG[:num_nodes])
    return client


def run_commands(commands, user='torchuser', num_nodes: int = len(HOSTS),
                 host_args_list: List[tuple] = None):
    """
    Run a list of commands on (a subset of) nodes, show the output.
    """
    client = get_pssh_client(user=user, num_nodes=num_nodes)

    for ci, cmd in enumerate(commands):
        print(f"=== Running {cmd} ...")
        if host_args_list is None or ci >= len(host_args_list):
            output = client.run_command(cmd)
        else:
            output = client.run_command(cmd, host_args=host_args_list[ci])

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


def copy_file(src_path, dst_path, user='torchuser', recurse=False):
    """
    Copy file through scp to destination path on all nodes.
    """
    client = get_pssh_client(user=user)

    copy_greenlets = client.copy_file(src_path, dst_path, recurse=recurse)
    gevent.joinall(copy_greenlets, raise_error=True)
