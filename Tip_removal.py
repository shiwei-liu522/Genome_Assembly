#Python3


class TipRemoval:
    def __init__(self, reads, k):
        self.reads = reads
        self.k = k

    @staticmethod
    def k_min_mers(k_mers):
        k_min_mers = set()
        for k_mer in k_mers:
            k_min_mers.add(k_mer[:-1])
            k_min_mers.add(k_mer[1:])
        k_min_mers = tuple(k_min_mers)
        return k_min_mers

    @staticmethod
    def de_bruijn(k_mers, k_min_mers):
        to_id = dict()
        for i, k_mer in enumerate(k_min_mers):
            to_id[k_mer] = i

        edges = []
        for k_mer in k_mers:
            v1 = to_id[k_mer[:-1]]
            v2 = to_id[k_mer[1:]]
            edges.append((v1, v2))
        edges = tuple(edges)
        return edges

    @staticmethod
    def to_adj(n, edges):
        adj_list = [[] for _ in range(n)]
        adj_list_r = [[] for _ in range(n)]
        for v1, v2 in edges:
            adj_list[v1].append(v2)
            adj_list_r[v2].append(v1)
        return adj_list, adj_list_r

    def remove_tips(self):
        k_mers = self.k_mers()
        k_min_mers = self.k_min_mers(k_mers)

        n = len(k_min_mers)
        edges = self.de_bruijn(k_mers, k_min_mers)
        adj_list, adj_list_r = self.to_adj(n, edges)

        n_tips = 0
        while True:
            edges_to_del = set()
            for i, edge in enumerate(edges):
                v1, v2 = edge
                if (len(adj_list[v2]) == 0) or (len(adj_list_r[v1]) == 0):
                    edges_to_del.add(i)

            if len(edges_to_del) == 0:
                break
            else:
                n_tips += len(edges_to_del)
                edges = [edge for i, edge in enumerate(edges) if i not in edges_to_del]
                adj_list, adj_list_r = self.to_adj(n, edges)
        return n_tips

    def k_mers(self):
        k_mers = set()
        for read in self.reads:
            for i in range(len(read) - self.k + 1):
                k_mers.add("".join(read)[i:(i + self.k)])
        k_mers = tuple(k_mers)
        return k_mers


if __name__ == "__main__":
    def sol():
        reads = []
        for _ in range(1618):
            reads.append(input().strip())
        reads = tuple(reads)
        k = 15
        tr = TipRemoval(reads, k)
        n_tips = tr.remove_tips()
        print(n_tips)
    sol()
