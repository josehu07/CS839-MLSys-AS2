from .allreduce import *


class AllReduceRing(AllReduce):
    def run(self, vec: torch.Tensor):
        vec_buf = [self.get_zero_buf() if i != self.rank else vec.clone()
                   for i in range(self.world_size)]
        dst = (self.rank - 1) % self.world_size
        src = (self.rank + 1) % self.world_size
        for i in range(self.world_size - 1):
            send_idx = (self.rank + i) % self.world_size
            recv_idx = (send_idx + 1) % self.world_size

            req_send = dist.isend(vec_buf[send_idx], dst)
            req_recv = dist.irecv(vec_buf[recv_idx], src)

            # it might not be necessary to wait
            req_recv.wait()
            vec += req_recv
            req_send.wait()
        return vec_buf
