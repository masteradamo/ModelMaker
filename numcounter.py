import string
import time

f = open('space/linus.txt','r')
h = open('space/numbus.txt','w')

def counter(f):
    wl = {}
    tok = 0
    n = 0
    for para in f:
        if n%10000 == 0:
            print n
        para = para.split()
        for word in para:
            if word == str('\xe1\xbc\x80\xce\xbd-'):
                print "YES!"
            tok += 1
            if word in wl:
                wl[word] += 1
            else:
                wl[word] = 1
        n += 1
    return wl,tok

def writer(d,z):
    for thing in d:
        z.write(str(thing) + ": " + str(d[thing]) +"\n")

def writer2(d,g):
    for thing in d:
        g.write(str(thing) + "\n")

def writer3(l,z):
    for thing in l:
        for item in thing:
#            print item
            z.write(str(item) + ",")
            if item == str('\xe1\xbc\x80\xce\xbd-'):
                print "YES!"
        z.write("\n")

def orderer(wl):
    order = []
    for thing in wl:
        order.append((wl[thing],thing))
    return sorted(order,reverse=True)

def numberer(sl):
    enum = []
    n = 0
    while n < len(sl):
        enum.append((n+1,sl[n][1],sl[n][0]))
        n += 1
    return enum

def pointer(wl,tok):
    fc = []
    toco = 0
    tyto = len(wl)
    tyco = len(wl)
    order = orderer(wl)
    enum = numberer(order)
    for thing in order:
        if float(tyco)/tyto >= float(toco)/tok:
            fc.append(thing)
            tyco -= 1
            toco += thing[0]
    return fc,enum

wl,tok = counter(f)

print "TOKENS:",tok
print "TYPES:",len(wl)
#writer(wl,g)

fc,enum = pointer(wl,tok)
print "ACCEPTED WORDS:",len(fc)
#writer2(fc,j)
#writer2(enum,h)
writer3(enum,h)

#total para count = 61500000

#linus tokens = 1095238485
#linus types = 7485248
#words accepted = 207010

'''SPACE 1'''
#total para count = 59900000

#linus tokens = 1088317747
#linus types = 7421507
#words accepted = 205225

#brokus2 tokens = 15303573562
#brokus2 types = 13854145
#linus2 tokens = 1518905909
#linus2 types = 11970611
#linus2redux tokens = 1365458079
#linus2redux types = 10872326
