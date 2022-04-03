from .allreduce import *


class AllReduceRecurHD(AllReduce):
    def bde_allreduce(self, x, left, right):
        if left == right:
            return
        size = right - left + 1
        mid = (left + right) // 2
        if self.rank <= mid:
            partner = self.rank + (size // 2)
        else:
            partner = self.rank - (size // 2)

        req_send = dist.isend(x, partner)
        tmp = self.get_zero_buf()
        req_recv = dist.irecv(tmp, partner)

        req_recv.wait()
        x += tmp
        req_send.wait()

        if self.rank <= mid:
            self.bde_allreduce(x, left, mid)
        else:
            self.bde_allreduce(x, mid + 1, right)

    def run(self, vec: torch.Tensor):
        self.bde_allreduce(vec, 0, self.world_size - 1)
