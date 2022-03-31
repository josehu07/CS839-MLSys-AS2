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

HOST_CONFIG = [
    HostConfig(port=27610, user='josehu'),
    HostConfig(port=27611, user='josehu'),
    HostConfig(port=27612, user='josehu'),
    HostConfig(port=27613, user='josehu'),
    HostConfig(port=27610, user='josehu'),
    HostConfig(port=27611, user='josehu'),
    HostConfig(port=27612, user='josehu'),
    HostConfig(port=27613, user='josehu'),
    HostConfig(port=27610, user='josehu'),
    HostConfig(port=27611, user='josehu'),
    HostConfig(port=27612, user='josehu'),
    HostConfig(port=27613, user='josehu'),
    HostConfig(port=27610, user='josehu'),
    HostConfig(port=27611, user='josehu'),
    HostConfig(port=27612, user='josehu'),
    HostConfig(port=27613, user='josehu')
]

CLIENT = ParallelSSHClient(HOSTS, host_config=HOST_CONFIG)


def run_commands(commands, print_stdout=False):
    for cmd in commands:
        print(f"=== Running {cmd} ...")
        output = CLIENT.run_command(cmd)

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

def copy_file(src_path, dst_path):
    CLIENT.copy_file(src_path, dst_path)
