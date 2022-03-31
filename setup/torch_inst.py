#
# Install pytorch on all 16 nodes.
#


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands


def main():
    commands = [
        "sudo apt-get update --fix-missing",
        "sudo apt-get upgrade -y",
        "sudo apt-get install -y python3-pip",
        "pip3 install numpy matplotlib",
        "pip3 install torch==1.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html"
    ]
    run_commands(commands, print_stdout=True)   # somehow False doesn't work

    commands = [
        "python3 -c 'import torch; x = torch.rand(5, 3); print(x)'"
    ]
    run_commands(commands)

if __name__ == '__main__':
    main()
