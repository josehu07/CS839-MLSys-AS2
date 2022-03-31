#
# Setup the passwordless sudoer user 'torchuser' on all 16 nodes.
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
            else:
                for line in host_output.stdout:
                    print(line)
            idx += 1


def main():
    print("=== Copying script files to all hosts...")
    client.copy_file('chsh_bash.sh', 'chsh_bash.sh')
    print("Done")

    commands = [
        "sudo chmod a+x chsh_bash.sh",
        "sudo bash ./chsh_bash.sh",
        "sudo userdel -r torchuser",
        "sudo useradd -m -s /bin/bash torchuser",
        "echo 'torchuser:torchuser' | sudo chpasswd",
        "sudo usermod -aG sudo torchuser",
        "sudo runuser -u torchuser mkdir /home/torchuser/.ssh"
    ]
    run_commands(commands)

    print("=== Copying SSH authorized_keys to torchuser...")
    client.copy_file('authorized_keys', 'authorized_keys')
    print("Done")

    commands = [
        "sudo runuser -u torchuser cp /users/josehu/authorized_keys /home/torchuser/.ssh/authorized_keys",
        "sudo runuser -u torchuser chmod 644 /home/torchuser/.ssh/authorized_keys",
        "echo 'torchuser ALL=(ALL) NOPASSWD: ALL' | sudo tee -a /etc/sudoers.d/99-emulab"
    ]
    run_commands(commands)

if __name__ == '__main__':
    main()
