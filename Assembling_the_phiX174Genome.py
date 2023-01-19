#Python3

'''
Problem Description
Task. Given a list of error-free reads, perform the task of Genome Assembly and
return the circular genome from which they came.
Dataset. Each of 1 618 lines of the input contains a single read, that is, a string over {A, C, G, T}.
The reads are given to you in alphabetical order because their true order is hidden from you.
Each read is 100 nucleotides long and contains no sequencing errors.
Note that you are not given the 100-mer composition of the genome, i.e., some 100-mers may be missing.
Output. Output the assembled genome on a single line.
'''



class GenomeAssembling:
    @staticmethod
    def find_bigger_overlap_size(s1, s2, prev_overlap_size):
        res = None
        for overlap_size in range(GenomeAssembling.len - 1, prev_overlap_size, -1):
            if s2.startswith(s1[(GenomeAssembling.len - overlap_size):]):
                res = overlap_size
                break
        return res

    len = 100

    def __init__(self, dataset):
        self.dataset = dataset
        self.n = len(self.dataset)

    def genome(self):
        next_s = [(0, None) for _ in range(self.n)]

        for i in range(self.n - 1):
            s1 = self.dataset[i]
            for j in range(i + 1, self.n):
                s2 = self.dataset[j]

                prev_overlap_size_i, _ = next_s[i]
                prev_overlap_size_j, _ = next_s[j]

                overlap_size_i = self.find_bigger_overlap_size(s1, s2, prev_overlap_size_i)
                overlap_size_j = self.find_bigger_overlap_size(s2, s1, prev_overlap_size_j)

                if overlap_size_i is not None:
                    next_s[i] = (overlap_size_i, j)
                if overlap_size_j is not None:
                    next_s[j] = (overlap_size_j, i)

        str_parts = [self.dataset[0]]
        overlap_size, cur = next_s[0]
        while cur != 0:
            str_parts.append(self.dataset[cur][overlap_size:])
            overlap_size, cur = next_s[cur]

        s = "".join(str_parts)
        s = s[:-overlap_size]
        return s

def sol():
    n_rows = 1618
    dataset = [input().strip()]
    for _ in range(n_rows - 1):
        s = input().strip()
        if s != dataset[-1]:
            dataset.append(s)

    t = GenomeAssembling(dataset)
    ans = t.genome()
    print(ans)


if __name__ == "__main__":
    sol()
