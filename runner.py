import numpy as np
import re
from copy import deepcopy
from time import sleep
from conceptnet5.query import query
from nltk.corpus import wordnet as wn
import inflect

f = '/home/masteradamo/academy/QueenMerrily/metamatic/corpora/Wikipedia/space2w2NUM/tallus.txt'
g = '/home/masteradamo/academy/QueenMerrily/metamatic/corpora/Wikipedia/numbus.txt'
h = '/home/masteradamo/academy/QueenMerrily/metamatic/corpora/DBpedia/DBstract'

peng = inflect.engine()

def translater(y):
    tr = {}
    z = open(y,'r')
    for line in z:
        line = line.split(",")
        tr[line[1]] = line[0]
    return tr

def numberer(y,l):
    rt = [0]*l
    z = open(y,'r')
    for line in z:
        line = line.split(",")
        rt[int(line[0])] = line[1]
    return rt

def vecter(y,x):
    words = []
    for thing in x:
        words.append(tr[thing])
    vecs = []
    z = open(y,'r')
    n = 0
    for line in z:
        if len(vecs) < len(words):
            if str(n+1) in words:
                print rt[n+1],"FOUND"
                line = line[:-2].split("::",1)
                vecs.append(line[1])
            n += 1
        else:
            break
    z.close()
    return vecs

def grouper(vecs):
    tal = {}
    for vec in vecs:
        vec = vec.split(",")
        for item in vec:
            item = item.split(":")
            if item[0] in tal:
                tal[item[0]].append(float(item[1]))
            else:
                tal[item[0]] = [float(item[1])]
    print "VECS GROUPED"
    return tal

def cutter(tal,l):
    print str(len(tal)) + " DIMENSIONS CONSIDERED IN TOTAL"
    cuts = []
    for thing in tal:
        if len(tal[thing]) < l:
            cuts.append(thing)
    for thing in cuts:
        del tal[thing]
    print "DIMENSIONS CUT"
    return tal

def subnormer(tal,l):
    tots = [0.0]*l
    for thing in tal:
        n = 0
        while n < l:
            tots[n] += (tal[thing][n])**2
            n += 1
    m = 0
    while m < l:
        tots[m] = np.sqrt(tots[m])
        m += 1
    for thing in tal:
        p = 0
        while p < l:
            tal[thing][p] = tal[thing][p]/tots[p]
            p += 1
    print "TALLIES NORMED"
    return tal

def varier(tal,l,dlen):
    tups = []
    ttups = []
    for thing in tal:
        if len(tal[thing]) >= l:
            val = float("%.5f" % np.mean(tal[thing]))
            tups.append((val,thing))
            ttups.append((val,rt[int(thing)]))
    ranks = sorted(tups,reverse=True)
    tranks = sorted(ttups,reverse=True)
    outs = []
    print tranks[0:dlen]
    for item in ranks[0:dlen]:
        outs.append(item[1])
    return outs,tranks[0:dlen]

def textspacer(dims,wd,cent):
    for dim in dims:
        y = "/home/masteradamo/academy/QueenMerrily/metamatic/corpora/Wikipedia/space2w2NUM/contexts/" + dim + ".txt"
        z = open(y,'r')
        n = 0
        for line in z:
            n += 1
            line = line.split("::")
            val = float(line[1])
            wd[int(line[0])][0] += ((cent-val)**2)-cent**2
            wd[int(line[0])][1] += val**2
            wd[int(line[0])][2] += val*cent
#            wd[int(line[0])][3].append(uncler(val,y))
    n = 0
    return wd

def uncler5(dims,wd,l):
    hits = {}
    rits = []
    tops = sorter(wd,1,1)[:l]
    for n in range(0,l):
        word = tops[n]
        ind = wd.index(word)
        hits[ind] = n
        rits.append(ind)
    print "SPARSITY DICTIONARITIES CONSTRUCTED"
    M = matter(dims,l,hits)
    print "SPARSITY MATRIX BUILT"
#    x = 0
    for n in range(0,len(M)):
#        if x%100==0:
#            print x/100
#        x += 1
        vals = np.array([100.0]*len(M))
        for m in range(0,len(M)):
            if n != m:
                vals[m] = np.linalg.norm(M[n]-M[m])
#        wd[rits[n]][3] = (min(vals),rt[rits[np.argmin(vals)]])
        wd[rits[n]][3] = min(vals)
    print "SPARSITY STATS COMPUTED"
    return wd

def matter(dims,l,hits):
    M = np.array([[0.0]*(len(dims))]*l)
    for n in range (0,len(dims)):
        y = "/home/masteradamo/academy/QueenMerrily/metamatic/corpora/Wikipedia/space2w2NUM/contexts/" + dims[n] + ".txt"
    	z = open(y,'r')
        for line in z:
            line = line.split("::")
            if int(line[0]) in hits:
                M[hits[int(line[0])]][n] = float(line[1])
    return M

def resulter(wd,l,cent):
    norm = np.sqrt((cent**2)*l)
    print "ANCHOR NORM: " + str(norm)
    for item in wd:
        item[0] = np.sqrt(item[0]+((cent**2)*l))
        if item[1] > 0:
#            print item[1],item[2]
            item[1] = np.sqrt(item[1])
            item[2] = np.arccos((item[2])/(item[1]*norm))*180/np.pi
        else:
            item[2] = 90.0
    return wd

def sorter(l,n,rev):
    if rev == 0:
        return sorted(l,key=lambda bunch: bunch[n])
    else:
        return sorted(l,key=lambda bunch: bunch[n],reverse=True)

def inster(words,comp,ds,vs,dbase,wd):
    title = str(comp) + ":" + "-".join(words)
    w = "/home/masteradamo/academy/QueenMerrily/metamatic/taxotron/data/" + title + ".txt"
    x = open(w,'w')
    ins = []
    outs = []
    targ = dbase[comp]
    l = len(words)
    vecs = vecter(f,words)
    tal = grouper(vecs)
    tal = cutter(tal,l)
    tal = subnormer(tal,l)
    for dlen in ds:
        x.write("DIMS:" + str(dlen) + "\n")
        dims,nims = varier(tal,l,dlen)
        wd = textspacer(dims,wd,5.0)
        rank = resulter(wd,len(dims),5)
        rank = uncler5(dims,rank,5000)
        dturner(x,targ,nims)
        turner(x,targ,rank,vs)

def dturner(x,targ,nims):
    davov = []
    davin = []
    davout = []
    dins = []
    douts = []
    for tup in nims:
        davov.append(tup[0])
        dins,douts,davin,davout = pengparer(targ,tup[1],tup[0],dins,douts,davin,davout)
    sultwriter(x,dins,douts,np.mean(davov),np.mean(davin),np.mean(davout))
    print str(len(nims)) + " DIMS WRITTEN"

def turner(x,targ,rank,vs):
    for val in vs:
        x.write("VECS:" + str(val) + "\n")
        fields = ["CENTROID","NORM","ANGLE","SPARSENESS"]
        for n in range(0,len(fields)):
            vavov = []
            vavin = []
            vavout = []
            vins = []
            vouts = []
            x.write(fields[n] + "::")
            for thing in sorter(rank,n,n%2)[0:val]:
                vavov.append(thing[n])
                word = rt[wd.index(thing)]
                vins,vouts,vavin,vavout = pengparer(targ,word,thing[n],vins,vouts,vavin,vavout)
            sultwriter(x,vins,vouts,np.mean(vavov),np.mean(vavin),np.mean(vavout))
        print str(val) + " VECS WRITTEN"

def pengparer(targ,word,val,ins,outs,avin,avout):
#    print "STARTING PENG"
#    print word
    alt = peng.singular_noun(str(word))
    if word in targ or alt in targ:
        avin.append(val)
        if word not in ins and alt not in ins:
            ins.append(word)
    else:
        avout.append(val)
        if word not in outs and alt not in outs:
            outs.append(word)
#    print "FINISHING PENG"
    return ins,outs,avin,avout

def sultwriter(x,ins,outs,avov,avin,avout):
    x.write("IN:" + str(float(len(ins))/(len(ins)+len(outs))) + "," + "OUT:" + str(float(len(outs))/(len(ins)+len(outs))) + "," + "AVOV:" + str(avov) + "," + "AVIN:" + str(avin) + "," + "AVOUT:" + str(avout) + "\n")
    x.write("INS::")
    for thing in ins:
        x.write(str(thing) + ",")
    x.write("\n")
    x.write("OUTS::")
    for thing in outs:
        x.write(str(thing) + ",")
    x.write("\n")

def dbaser(y):
    base = {}
    z = open(y,'r')
    for line in z:
        line = line.split("::")
        pos = line[1].split(",")[:-1]
        for thing in pos:
            if thing not in base:
                base[thing] = []
            base[thing].append(line[0])
    return base

def wbaser():
    wd = []
    n = 0
    while n < 200000:
        wd.append([0.0,0.0,0.0,0.0])
        n += 1
    print "BASE DICTIONARY BUILT"
    return wd

tr = translater(g)
print "TRANSLATER BUILT"
rt = numberer(g,len(tr)+1)
print "REVERSE TRANSLATER BUILT"
'''cats = [[["language"],["english","chinese","farsi"]],[["disease"],["syphilis","cancer","leprosy"]],[["weapon"],["gun","sword","mace"]]]
ds = [2,5,10,25,50,100,200,500]
vs = [10,20,30,40,50]

dbase = dbaser(h)

for subcat in cats:
    wd = wbaser()
    inster(subcat[0],subcat[0][0],ds,vs,dbase,wd)
    wd = wbaser()
    inster(subcat[1],subcat[0][0],ds,vs,dbase,wd)'''

#d = dicter(g,200000)
def runner(words,z):
    x = []
    wd = []
    n = 0
    while n < 200000:
        wd.append([0.0,0.0,0.0,0.0])
        n += 1
    print "BASE DICTIONARY BUILT"
    l = len(words)
    vecs = vecter(f,words)
    tal = grouper(vecs)
    tal = cutter(tal,l)
    tal = subnormer(tal,l)
    dlen = raw_input("HOW MANY DIMENSIONS: ")
    dims,nims = varier(tal,l,int(dlen))
    wd = textspacer(dims,wd,5.0)
    rank = resulter(wd,len(dims),5)
#    rank = uncler5(dims,rank,5000)
    cents = []
    norms = []
    for thing in sorter(rank,0,0)[0:int(z)]:
        cents.append(rt[wd.index(thing)])
    for thing in sorter(rank,1,1)[0:int(z)]:
        norms.append(rt[wd.index(thing)])
    return cents,norms


'''            z = raw_input("HOW MANY VECTORS: ")
            print "BY DISTANCE FROM ANCHOR:"
            for thing in sorter(rank,0,0)[0:int(z)]:
                print rt[wd.index(thing)],thing
            print "BY NORM:"
            for thing in sorter(rank,1,1)[0:int(z)]:
                print rt[wd.index(thing)],thing
            print "BY ANGLE:"
            for thing in sorter(rank,2,0)[0:int(z)]:
                print rt[wd.index(thing)],thing
            print "BY SPARSENESS:"
            for thing in sorter(rank,3,1)[0:int(z)]:
                print rt[wd.index(thing)],thing
#            tword = raw_input("TARGET WORD FOR COMPARISON: ")
#            extracter(rank,nims,tword,z)
            break'''
