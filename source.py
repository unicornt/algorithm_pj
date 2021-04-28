def Ins(s, si, k):
    return s[0:k] + si + s[k:]

def Del(s, k, l):
    return s[0:k] + s[k + l:]

def Dup(s, k, l):
    return s[0:k] + s[k: k + l] + s[k: k + l] + s[k + l:]

def Inv(s, k, l):
    return s[0:k] + s[k + l - 1: k - 1: -1] + s[k + l:]

dic = {}
dic_n = {}
l = {}
MIN_SAME_LEN = 20

def rev(c):
    if c == 'A':
        return 'T'
    elif c == 'T':
        return 'A'
    elif c == 'C':
        return 'G'
    else:
        return 'C'

def calc_diff(s1, s2):
    l.clear()
    l['A'] = []
    l['C'] = []
    l['T'] = []
    l['G'] = []
    n = len(s1)
    m = len(s2)
    i = 0
    j = 0
    s1 += '$'
    s2 += '@'
    res = []
    # print(n, m)
    while i < n and j < m:
        while s1[i] == s2[j]:
            i += 1
            j += 1
        if i >= n and j >= m:
            break
        # print('different', i, j, n, m)
        f = 0
        for k in range(2, min(m - j, n - i, 1000)):
            # print('k', k)
            ln = 0
            while(ln < k and s1[i + ln] == rev(s2[j + k - 1 - ln])):
                ln += 1
            if ln < k:
                continue
            w = 0
            while s1[i + k + w] == s2[j + k + w] and w < MIN_SAME_LEN:
                w += 1
            if w < MIN_SAME_LEN:
                continue
            res.append(('REV', i, i + k))
            # print('REV', i, i + k)
            i += k
            j += k
            f = 1
            break
        if f == 0:
            for k in range(1, min(m - j, n - i, 1000)):
                w = 0
                while(s1[i + k + w] == s2[j + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    res.append(('DEL', i, i + k))
                    # print('DEL', i, i + k)
                    f = 1
                    i += k
                    break
                w = 0
                while(s1[i + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    if s2[j: j + k] == s1[i - k + 1: i + 1]:
                        res.append(('DUP', i - k + 1, i + 1))
                        # print('DUP', i - k + 1, i)
                        j += k
                        f = 1
                        break
                    else:
                        res.append(('ADD', i, i + k))
                        # print('ADD', i, i + k)
                        j += k
                        f = 1
                        break
                w = 0
                while(s1[i + k + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    # print(s1[i:i+k], s2[j:j+k])
                    res.append(('TRA0', i, k, s1[i:i+k], s2[j:j+k]))
                    # print('TRA0', i, k)
                    i += k
                    j += k
                    f = 1
                    break
        if f == 0:
            res.append(('DEL', i, n))
            res.append(('ADD', n, m))
            i = n
            j = m
    # print(res)
    return res
            
rest = {}

def solve():
    for x in dic.keys():
        # print(x)
        rest[x] = calc_diff(dic[x], dic_n[x])
    for x in rest:
        for y in rest:
            if x != y:
                for ui in range(len(rest[x])):
                    for vi in range(len(rest[y])):
                        u = rest[x][ui]
                        v = rest[y][vi]
                        if u[2] != v[2]:
                            continue
                        if u[0] == 'TRA0' and v[0] == 'TRA0' and \
                            u[3] == v[4] and u[4] == v[3]:
                            rest[x][ui] = ('TRA', u[1], u[1] + u[2], v[1], v[1] + v[2])
                            rest[y][vi] = ('TRA', u[1], u[1] + u[2], v[1], v[1] + v[2])
    for x in rest:
        print(rest[x])

def main():
    inf = open("./task1/ref.fasta")
    for s in inf.readlines():
        if s[0] == '>':
            # name of sequence
            sname = s[1:-1]
        else:
            if sname == '':
                print('error')
            else:
                dic[sname] = s[:-1]
    # print(dic.keys())
    inf = open("./task1/sv.fasta")
    for s in inf.readlines():
        if s[0] == '>':
            # name of sequence
            sname = s[1:-1]
        else:
            if sname == '':
                print('error')
            else:
                dic_n[sname] = s[:-1]
    # print(dic_n.keys())
    solve()

if __name__ == "__main__":
    main()