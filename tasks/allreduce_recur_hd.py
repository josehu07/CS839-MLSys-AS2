from allreduce import *


class AllReduceRecurHD(AllReduce):
    def bde_allreduce(self, x, left, right):
        """
        This is one implementation as fig. 13 in the paper.
        It sends the entire vector, which is not bandwidth-optimal.
        """
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

    def bde_allgather(self, x, left, right):
        if left == right:
            return
        size = right - left + 1
        mid = (left + right) // 2

        if self.rank <= mid:
            partner = self.rank + (size // 2)
            self.bde_allgather(x, left, mid)
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(left, mid + 1)
            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(mid + 1, right + 1)
        else:
            partner = self.rank - (size // 2)
            self.bde_allgather(x, mid + 1, right)
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(mid + 1, right + 1)
            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(left, mid + 1)

        req_send = dist.isend(x[send_slice_begin: send_slice_end], partner)
        req_recv = dist.irecv(x[recv_slice_begin: recv_slice_end], partner)
        req_recv.wait()
        req_send.wait()

    def bde_reduce_scatter(self, x, left, right):
        if left == right:
            return
        size = right - left + 1
        mid = (left + right) // 2

        if self.rank <= mid:
            partner = self.rank + (size // 2)
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(mid + 1, right + 1)
            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(left, mid + 1)
        else:
            partner = self.rank - (size // 2)
            send_slice_begin, send_slice_end = \
                self.get_slice_idx(left, mid + 1)
            recv_slice_begin, recv_slice_end = \
                self.get_slice_idx(mid + 1, right + 1)

        recv_buf = self.get_zero_buf(recv_slice_end - recv_slice_begin)
        req_send = dist.isend(x[send_slice_begin: send_slice_end], partner)
        req_recv = dist.irecv(recv_buf, partner)
        req_recv.wait()
        req_send.wait()

        x[recv_slice_begin: recv_slice_end] += recv_buf

        if self.rank <= mid:
            self.bde_reduce_scatter(x, left, mid)
        else:
            self.bde_reduce_scatter(x, mid + 1, right)

    def run(self, vec: torch.Tensor) -> torch.Tensor:
        self.bde_reduce_scatter(vec, 0, self.world_size - 1)
        self.bde_allgather(vec, 0, self.world_size - 1)
        return vec
