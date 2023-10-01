import random;
import json;

n = 2;
usewds = []
start = []
recent = []
rem=''
mark = {}
wordlist = [set(),set()]

with open('./vulgate.txt', mode="rb") as f:
    while True:
        k = f.read(10)
        if len(k) == 0: 
            if len(start) > 0:
                usewds = start[:]
                start.clear()
            else:
                break;
        s = rem + str(k, encoding='utf-8')
        i=s.rindex(' ')
        div = s[:i]
        rem = s[i:]
        wds = usewds or div.split(" ")
        for w in wds:
            if w=='': continue;
            if len(start) < n and len(k) > 0: start.append(w)
            if len(recent) == n:
                a = recent[-2]
                b = recent[-1]
                if not (a in mark): 
                    mark[a] = {}
                if not (b in mark[a]): 
                    fresh = [set(), set()]
                    mark[a][b] = fresh
                try:
                    z = 0 if w[1] in ['a', 'e', 'i', 'o', 'u'] else 1
                    mark[a][b][z].add(w)
                    wordlist[z].add(w)
                except: print(w)
            recent.append(w)
            if len(recent) > n: recent.pop(0)
wordlist[0] = list(wordlist[0])
wordlist[1] = list(wordlist[1])

mark = {a: {c: [list(e) for e in d] for c, d in b.items()} for a, b in mark.items()}

out = open('./words.json', 'w')
json.dump({'mark':mark,'wordlist':wordlist}, out)
out.close()

print("ready")
