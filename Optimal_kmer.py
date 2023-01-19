#Python3

class KmerSize:
    def __init__(self, read):
        self.read = read

    @staticmethod
    def cycle_exists(n, edges):
        in_degree = [0] * n
        out_degree = [0] * n

        for v1, v2 in edges:
            out_degree[v1] += 1
            in_degree[v2] += 1

        cycle = True
        for d1, d2 in zip(in_degree, out_degree):
            if d1 != d2:
                cycle = False
                break
        return cycle

    @staticmethod
    def de_bruijn_graph(k_mers, min_k):
        min_id = dict()
        for i, k_mer in enumerate(min_k):
            min_id[k_mer] = i

        edges = []
        for k_mer in k_mers:
            v1 = min_id[k_mer[:-1]]
            v2 = min_id[k_mer[1:]]
            edges.append((v1, v2))
        edges = tuple(edges)
        return edges

    def res(self):
        k_min = 3
        k_max = len(self.read[0])

        while k_min <= k_max:
            k = (k_min + k_max) // 2

            k_mers = set()
            for read in self.read:
                for i in range(len(read) - k + 1):
                    k_mers.add("".join(read)[i:(i + k)])
            k_mers = tuple(k_mers)

            k_min_1_mers = set()
            for k_mer in k_mers:
                k_min_1_mers.add(k_mer[:-1])
                k_min_1_mers.add(k_mer[1:])
            k_min_1_mers = tuple(k_min_1_mers)

            edges = self.de_bruijn_graph(k_mers, k_min_1_mers)

            if not self.cycle_exists(len(k_min_1_mers), edges):
                k_max = k - 1
            else:
                k_min = k + 1
        return k_max


if __name__ == "__main__":
    def ans():
        n_reads = 400
        reads = []
        for _ in range(n_reads):
            reads.append(input().strip())
        reads = tuple(reads)

        k = KmerSize(reads).res()
        print(k)
    ans()
