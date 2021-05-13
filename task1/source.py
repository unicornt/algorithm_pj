import functools
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

def calc_diff(s1, s2, sn):
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
            res.append(('INV', sn, i, i + k))
            # print('REV', i, i + k)
            i += k
            j += k
            f = 1
            break
        if f == 0:
            for k in range(1, min(m - j, n - i, 1000)):
                w = 0
                while(s1[i + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    for ki in range(0, 20):
                        if s2[j - k: j - ki] == s2[j - ki: j + k - ki]:
                            res.append(('DUP', sn, i - k + 1, i - ki + 1))
                            # print('DUP', i - k + 1, i)
                            j += k - ki
                            f = 1
                            break
        if f == 0:
            for k in range(1, min(m - j, n - i, 1000)):
                w = 0
                while(s1[i + k + w] == s2[j + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    res.append(('DEL', sn, i, i + k))
                    # print('DEL', i, i + k)
                    f = 1
                    i += k
                    break
                w = 0
                while(s1[i + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    res.append(('INS', sn, i, i + k))
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
            res.append(('INS', n, m))
            i = n
            j = m
    # print(res)
    return res
            
rest = {}
prio = {"DUP": 0, "INS": 1, "DEL": 1, "INV": 2, "TRA": 3}

def cmp(a, b):
    if prio[a[0]] == prio[b[0]]:
        if a[1] == b[1]:
            if a[2] < b[2]:
                return -1
            else:
                return 1
        else:
            if a[1] < b[1]:
                return -1
            else:
                return 1
    else:
        if prio[a[0]] < prio[b[0]]:
            return -1
        else:
            return 1

def solve():
    for x in dic.keys():
        # print(x)
        rest[x] = calc_diff(dic[x], dic_n[x], x)
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
                            rest[x][ui] = ('TRA', x, u[1], u[1] + u[2], y, v[1], v[1] + v[2])
                            rest[y][vi] = ('TRA2222', x, u[1], u[1] + u[2], y, v[1], v[1] + v[2])
    inf = open("./task1-sample/sv_ans.bed", 'w')
    res=[]
    for x in rest:
        for y in rest[x]:
            if y[0] == 'TRA2222':
                continue
            if y[0] == 'TRA0':
                y[0] = 'ADD'
                res.append(y)
                y[0] = 'DEL'
            res.append(y)
    res.sort(key=functools.cmp_to_key(cmp))
    print(res)
    ret = []
    for y in res:
        s = ''
        for i in range(len(y)):
            s += str(y[i]) + ' \n'[i == len(y) - 1]
        ret.append(s)
    for s in ret:
        inf.write(s)

def main():
    inf = open("./task1-sample/ref.fasta")
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
    inf = open("./task1-sample/sv.fasta")
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