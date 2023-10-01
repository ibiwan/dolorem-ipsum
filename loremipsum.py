# Download source markov chain db
import urllib.request
u = 'https://ibiwan.com/static/words.json'
f = open ('./markov.txt', 'a');
for line in urllib.request.urlopen(u):
    f.write(line.decode('utf-8'))
f.close()

# 
m, v = open('markov.txt', 'r', encoding='utf-8').read().split("{",1);
k = json.loads('{'+v)
mark = k['mark']
wordlist = k['wordlist']

import os
# recover word database space
os.remove('markov.txt')


w1 = random.choice(list(mark.keys()))
w2 = random.choice(list(mark[w1].keys()))
bites = [bin(ord(b))[2:].rjust(8, '0') for b in m]
bs = ''.join(bites)
gen = [w1, w2]
out = []
sentenceLength = 0
minSentenceLength = 5
minClauseLength = 6
for c in bs:
    branch = int(c)
    [a, b] = gen[-2:]
    cands = []
    outWord = ''
    vecWord = ''
    if a in mark and b in mark[a]:
        cands = list(mark[a][b][branch])
        if len(cands):
            vecWord = random.choice(cands)
            outWord = vecWord
        else:
            vecWord = random.choice(list(mark[a][b][1 - branch]))
            outWord = random.choice(wordlist[branch])
    elif a in mark:
        print(a, b, outWord, vecWord, mark[a][branch].keys(),mark[a][1 - branch].keys(), 'GEN', gen)
        print(mark[a])
        break
    else:
        outWord = random.choice(cands) if len(cands) > 0 else random.choice(wordlist[1-branch])
        vecWord = random.choice(list(mark[a][b][1-branch]))

    endSen = False
    endClause = False
    if sentenceLength > minSentenceLength:
        for j in range(sentenceLength - minSentenceLength):
            br = random.randint(0,5) == 0
            if br:
                endSen = True
                break;
    if sentenceLength == 0:
        outWord = outWord.capitalize()
    if sentenceLength > minClauseLength:
        for k in range(sentenceLength - minClauseLength):
            br = random.randint(0, 1) == 0
            if br:
                endClause = True
                break;
    if endSen:
        out.append(outWord + '.')
        sentenceLength = 0
    elif endClause:
        out.append(outWord + ',')
        sentenceLength = 1
    else:
        out.append(outWord)
        sentenceLength += 1
    gen = [b, vecWord]
lorem = " ".join(out) + '.'

out = open('./lorem.txt', 'w')
out.write(lorem)
out.close()
