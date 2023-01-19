#Python3

def Uni_string(k, n):
    try:
        _ = int(k)
        collection = list(map(str, range(k)))
    except (ValueError, TypeError):
        collection = k
        k = len(k)

    a = [0] * k * n
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                sequence.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, k):
                a[t] = j
                db(t + 1, t)
    db(1, 1)
    return "".join(collection[i] for i in sequence)

if __name__ == "__main__":
    print(Uni_string(2, int(input())))