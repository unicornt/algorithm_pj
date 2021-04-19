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
    print(n, m)
    while i < n and j < m:
        while s1[i] == s2[j]:
            i += 1
            j += 1
        if i >= n and j >= m:
            break
        print('different', i, j, n, m)
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
            res.append(('REV', i, k))
            print('REV', i, i + k)
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
                    res.append(('DEL', i, k))
                    print('DEL', i, i + k)
                    f = 1
                    i += k
                    break
                w = 0
                while(s1[i + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    if s2[j: j + k] == s1[i - k + 1: i + 1]:
                        res.append(('DUP', i - k + 1, k))
                        print('DUP', i - k + 1, i)
                        j += k
                        f = 1
                        break
                    else:
                        res.append(('ADD', i, k))
                        print('ADD', i, i + k)
                        j += k
                        f = 1
                        break
                w = 0
                while(s1[i + k + w] == s2[j + k + w] and w <= MIN_SAME_LEN):
                    w += 1
                if w > MIN_SAME_LEN:
                    res.append(('TRA', i, k))
                    print('TRA', i, k)
                    i += k
                    j += k
                    f = 1
                    break
        if f == 0:
            res.append(('DEL', i, n - i))
            res.append(('ADD', n, m - j))
            i = n
            j = m
    print(res)
            

def solve():
    for x in dic.keys():
        print(x)
        calc_diff(dic[x], dic_n[x])

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
    print(dic.keys())
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
    print(dic_n.keys())
    solve()

if __name__ == "__main__":
    main()