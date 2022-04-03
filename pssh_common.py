#
# CloudLab machine SSH helpers with parallel-ssh.
#


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
    client = ParallelSSHClient(HOSTS[:num_nodes], host_config=HOST_CONFIG)
    return client


def run_commands(commands, user='torchuser', print_stdout=True):
    client = get_pssh_client(user)

    for cmd in commands:
        print(f"=== Running {cmd} ...")
        output = client.run_command(cmd)

        idx = 0
        for host_output in output:
            print(f">>> Host {idx} result:")
            exit_code = host_output.exit_code
            if exit_code and exit_code != 0:
                print(f"Error! code {host_output.exit_code}")
            elif print_stdout:
                for line in host_output.stdout:
                    print(line)
            idx += 1


def copy_file(src_path, dst_path, user='torchuser'):
    for hc in HOST_CONFIG:
        hc.user = user
    client = ParallelSSHClient(HOSTS, host_config=HOST_CONFIG)

    client.copy_file(src_path, dst_path)
