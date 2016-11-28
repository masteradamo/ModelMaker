import numpy as np

f = 'space/frequs.txt'
g = 'space/contextus.txt'
h = 'space/tallus.txt'

def cbuilder(y):
    z = open(y,'r')
    cd = {}
    for line in z:
        line = line[:-1].split("::")
        cd[line[0]] = float(line[1])
    return cd

def wcounter(y):
    z = open(y,'r')
    wd = {}
    tot = 0.0
    for line in z:
        line = line.split("::")
        sline = line[1].split(",")
        for pair in sline:
            pair = pair.split(":")
            if pair[0] == "0":
                tot += float(pair[1])
                wd[line[0]] = float(pair[1])
                break
    return tot,wd

def talyer(y1,y2,wc,cd,wd):
    z1 = open(y1,'r')
    z2 = open(y2,'w')
    n = 0
    for line in z1:
        if n%10==0:
            print n
        n += 1
        line = line[:-2].split("::")
        wt = wd[line[0]]
        z2.write(line[0] + "::")
        sline = line[1].split(",")
        for pair in sline:
            pair = pair.split(":")
            if pair[0] != "0":
                fr = float(pair[1])
                ct = cd[pair[0]]
                val = np.log2(((fr*wc)/(wt*(ct+10000)))+1)
                z2.write(pair[0] + ":" + "%.5f" % val + ",")
        z2.write("\n")

print "BUILDING CONTEXTS..."
cd = cbuilder(g)
print "CONTEXTS BUILT."
print "BUILDING WORDS..."
wc,wd = wcounter(f)
print "WORDS BUILT."
print "TOTAL WORD COUNT: " + str(wc)
print "TALLYING..."
talyer(f,h,wc,cd,wd)
