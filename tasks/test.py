#
# TODO
#


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pssh_common import run_commands


def main():
    commands = [
        "python3 -c 'import torch; x = torch.rand(5, 3); print(x)'"
    ]
    run_commands(commands)

if __name__ == '__main__':
    main()
