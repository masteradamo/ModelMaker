f = 'space/linus.txt'
g = 'space/numbus.txt'
h = 'spcae/numlus.txt'

def dicter(y):
    z = open(y,'r')
    d = {}
    for line in z:
        line = line.split(",")
#        if line[1]== '\xe1\xbc\x80\xce\xbd-':
#            print "YES!"
        d[line[1]] = line[0]
    z.close()
    return d

def replacer(ys,d,yt):
    zs = open(ys,'r')
    zt = open(yt,'w')
    n = 0
    for line in zs:
        if n%10000 == 0:
            print n
        n += 1
        line = line.split()
        for thing in line:
            try:
                zt.write(d[str(thing)] + ",")
            except KeyError:
                print "ERROR ON " + str(thing) + " IN LINE " + str(n)
        zt.write("\n")
    zs.close()
    zt.close()

d = dicter(g)
print "DICTIONARY BUILT"
replacer(f,d,h)
