# python 3
from collections import defaultdict


class GenomeAssembling:
    @staticmethod
    def lessmis(s1, s2, max_mis=2):
        num_mistakes = 0
        res = True
        for i in range(GenomeAssembling.len):
            if s1[i] != s2[i]:
                num_mistakes += 1

            if num_mistakes > max_mis:
                res = False
                break
        return res
    len = 100
    num_of_error = 2

    @staticmethod
    def overlap(s1, s2, prev_overlap_size=0):
        res = None
        for overlap_size in range(GenomeAssembling.len - 1, prev_overlap_size, -1):
            num_errors = 0
            s1_start_pos = GenomeAssembling.len - overlap_size
            for i in range(overlap_size):
                if s1[s1_start_pos + i] != s2[i]:
                    num_errors += 1
                    if num_errors > GenomeAssembling.num_of_error:
                        break
            else:
                res = overlap_size
                break
        return res

    def __init__(self, dataset):
        self.dataset = self.remove_dup(dataset)
        self.n = len(self.dataset)

    def remove_dup(self, dataset):
        n = len(dataset)
        duplicate = [False] * n

        for i in range(n - 1):
            if duplicate[i]:
                continue
            s1 = dataset[i]
            for j in range(i + 1, n):
                if duplicate[j]:
                    continue
                s2 = dataset[j]
                if self.lessmis(s1, s2, max_mis=GenomeAssembling.num_of_error):
                    duplicate[j] = True

        filtered_dataset = []
        for i in range(n):
            if not duplicate[i]:
                filtered_dataset.append(dataset[i])
        return filtered_dataset

    def genome(self):
        processed = [False] * self.n
        overlap = [0] * self.n
        next_id = [0] * self.n

        i = 0
        for _ in range(self.n - 1):
            s1 = self.dataset[i]
            processed[i] = True
            for j in range(1, self.n):
                if processed[j]:
                    continue

                s2 = self.dataset[j]

                new_overlap = self.overlap(s1, s2, overlap[i])

                if new_overlap is not None:
                    next_id[i] = j
                    overlap[i] = new_overlap

            i = next_id[i]

        next_id[i] = 0
        overlap[i] = self.overlap(self.dataset[i], self.dataset[0])
        last_overlap = overlap[i]
        start_pos = 0
        str_with_errors = [(0, start_pos)]
        cur = 0
        for _ in range(self.n - 1):
            start_pos += GenomeAssembling.len - overlap[cur]
            str_with_errors.append((next_id[cur], start_pos))
            cur = next_id[cur]
        str_len = start_pos + GenomeAssembling.len
        for _ in range(self.n - 1, self.n * 2):
            start_pos += GenomeAssembling.len - overlap[cur]
            str_with_errors.append((next_id[cur], start_pos))
            cur = next_id[cur]
        chars = []
        for i in range(str_len):
            counter = defaultdict(int)
            for str_id, start_pos in str_with_errors:
                if start_pos <= i < (start_pos + GenomeAssembling.len):
                    counter[self.dataset[str_id][i - start_pos]] += 1
            max_n = 0
            char = ""
            for c, n in counter.items():
                if n > max_n:
                    char = c
                    max_n = n
            chars.append(char)

        s = "".join(chars)
        s = s[last_overlap:]
        return s


def sol():
    n_rows = 1618
    dataset = [input().strip()]
    for _ in range(n_rows - 1):
        dataset.append(input().strip())

    t = GenomeAssembling(dataset)
    ans = t.genome()
    print(ans)


if __name__ == "__main__":
    sol()
