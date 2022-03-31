#
# Install pytorch on all 16 nodes.
#

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig

hosts = [
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
host_config = [
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
client = ParallelSSHClient(hosts, host_config=host_config)


def run_commands(commands):
    for cmd in commands:
        print(f"=== Running {cmd} ...")
        output = client.run_command(cmd)

        idx = 0
        for host_output in output:
            print(f">>> Host {idx} result:")
            exit_code = host_output.exit_code
            if exit_code and exit_code != 0:
                print(f"Error! code {host_output.exit_code}")
            # else:
            #     for line in host_output.stdout:
            #         print(line)
            idx += 1


def main():
    commands = [
        "sudo apt-get update --fix-missing",
        "sudo apt-get upgrade -y",
    ]
    run_commands(commands)

if __name__ == '__main__':
    main()
