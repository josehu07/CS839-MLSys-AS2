#
# Setup the passwordless sudoer user 'torchuser' on all 16 nodes.
#


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands, copy_file


def main():
    print("=== Copying script files to all hosts...")
    copy_file('chsh_bash.sh', 'chsh_bash.sh')
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
    run_commands(commands, True)

    print("=== Copying SSH authorized_keys to torchuser...")
    copy_file('authorized_keys', 'authorized_keys')
    print("Done")

    commands = [
        "sudo runuser -u torchuser cp /users/josehu/authorized_keys /home/torchuser/.ssh/authorized_keys",
        "sudo runuser -u torchuser chmod 644 /home/torchuser/.ssh/authorized_keys",
        "echo 'torchuser ALL=(ALL) NOPASSWD: ALL' | sudo tee -a /etc/sudoers.d/99-emulab"
    ]
    run_commands(commands, True)

if __name__ == '__main__':
    main()
