import torch
from torch import distributed as dist


class AllReduce:
    def __init__(self, master_ip: str, rank: int, world_size: int, vec_size: int) -> None:
        self.rank = rank
        self.world_size = world_size
        self.vec_size = vec_size
        dist.init_process_group(
            backend="gloo",
            init_method=f"tcp://{master_ip}:6585",
            rank=rank,
            world_size=world_size)

    def get_zero_buf(self, size=None):
        return torch.zeros(size if size is not None else self.vec_size)

    def get_slice_idx(self, slice_idx_begin: int, slice_idx_end: int):
        slice_size = self.vec_size // self.world_size
        return slice_idx_begin * slice_size, slice_idx_end * slice_size

    def run(self):
        raise NotImplementedError()
