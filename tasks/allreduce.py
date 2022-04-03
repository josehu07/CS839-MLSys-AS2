import sys
import os
import argparse
import logging
import time
import torch
from typing import List
from torch import distributed as dist


class AllReduce:
    def __init__(self, matser_ip, master_port, rank: int, world_size: int, vec_size: int) -> None:
        self.rank = rank
        self.world_size = world_size
        self.vec_size = vec_size
        dist.init_process_group(
            backend="gloo",
            init_method=f"tcp://{matser_ip}:{master_port}",
            rank=rank,
            world_size=world_size)
    
    def get_zero_buf(self):
        return torch.zeros(self.vec_size)
