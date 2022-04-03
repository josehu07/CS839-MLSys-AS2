from allreduce import *


class AllReduceRing(AllReduce):
    def bkt_allreduce(self, vec: torch.Tensor):
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

    def bkt_allgather(self, x):
        rank_prev = (self.rank - 1) % self.world_size
        rank_next = (self.rank + 1) % self.world_size

        curr = self.rank
        for i in range(self.world_size - 1):
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(curr, curr + 1)
            req_send = dist.isend(
                x[send_slice_begin, send_slice_end], rank_next)

            curr = (curr - 1) % self.world_size
            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(curr, curr + 1)
            req_recv = dist.irecv(
                x[recv_slice_begin: recv_slice_end], rank_prev)

            req_send.wait()
            req_recv.wait()

    def bkt_reduce_scatter(self, x):
        rank_prev = (self.rank - 1) % self.world_size
        rank_next = (self.rank + 1) % self.world_size

        curr = rank_next
        for i in range(self.world_size - 2, -1, -1):
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(curr, curr + 1)
            req_send = dist.isend(
                x[send_slice_begin, send_slice_end], rank_prev)
            curr = (curr + 1) % self.world_size

            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(curr, curr + 1)
            recv_buf = self.get_zero_buf(recv_slice_end - recv_slice_begin)
            req_recv = dist.irecv(recv_buf, rank_next)
            x[recv_slice_begin: recv_slice_end] += recv_buf

            req_send.wait()
            req_recv.wait()

    def run(self, vec: torch.Tensor) -> torch.Tensor:
        self.bkt_reduce_scatter(vec)
        self.bkt_allgather(vec)
        return vec
