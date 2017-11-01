import time

f = 'space/numlus.txt'
g = 'space/frequs.txt'
h = 'space/contextus.txt'
j = 'space/numbus.txt'

def ranger(y1,y2,clim):
    ext = len(open(j,'r').readlines())
    cd = {}
    bound = [0,500,2000,4000,7000,13000,25000,50000,100000,200000]
    n = 0
    while n < len(bound)-1:
        lo = bound[n]
        hi = min(bound[n+1],ext)
        print "FROM " + str(lo) + " TO " + str(hi)
        wd,cd = liner(y1,cd,lo,hi,clim)
        if n == 0:
            wwriter(y2,wd,lo,hi)
        else:
            awriter(y2,wd,lo,hi)
        wd = None
        n += 1
        if bound[n] > ext:
            break
    return cd

def bowcounter(line,wd,cd,lo,hi,clim):
    for word in line:
        if word not in wd:
            wd[word] = {}
            wd[word]["0"] = 0
        for cont in line:
            wd[word]["0"] += 1
            if cont in cd:
                cd[cont] += 1
            else:
                cd[cont] = 1
            if cont in wd[word]:
                wd[word][cont] += 1
            else:
                wd[word][cont] = 1
    return wd,cd

def counter(line,wd,cd,lo,hi,clim):
    clim = min(clim,len(line))
    n = 0
    while n < len(line):
        if lo <= int(line[n]) < hi:
            if line[n] not in wd:
                wd[line[n]] = {}
                wd[line[n]]["0"] = 0
            m = 1
            while m < clim+1:
                if n+m < len(line):
                    wd[line[n]]["0"] += 1
                    if line[n+m] in cd:
                        cd[line[n+m]] += 1
                    else:
                        cd[line[n+m]] = 1
                    if line[n+m] in wd[line[n]]:
                        wd[line[n]][line[n+m]] += 1
                    else:
                        wd[line[n]][line[n+m]] = 1
                if n-m > -1:
                    wd[line[n]]["0"] += 1
                    if line[n-m] in cd:
                        cd[line[n-m]] += 1
                    else:
                        cd[line[n-m]] = 0
                    if line[n-m] in wd[line[n]]:
                        wd[line[n]][line[n-m]] += 1
                    else:
                        wd[line[n]][line[n-m]] = 1
                m += 1
        n += 1
    return wd,cd

def liner(y,cd,lo,hi,clim):
    wd = {}
    z = open(y,'r')
    n = 0
    for line in z:
        if n%100000 == 0:
            print lo,n
        n += 1
        line = line.split(",")
        if len(line) > 1:
#            wd,cd = bowcounter(line[:-1],wd,cd,lo,hi,clim)
            wd,cd = counter(line[:-1],wd,cd,lo,hi,clim)
    z.close()
    return wd,cd

def wwriter(y,d,lo,hi):
    z = open(y,'w')
    ra = range(1,hi)
    for thing in ra:
        z.write(str(thing) + "::")
        for item in d[str(thing)]:
            z.write(str(item) + ":" + str(d[str(thing)][item]) + ",")
        z.write("\n")

def awriter(y,d,lo,hi):
    z = open(y,'a')
    ra = range(lo,hi)
    for thing in ra:
        z.write(str(thing) + "::")
        for item in d[str(thing)]:
            z.write(str(item) + ":" + str(d[str(thing)][item]) + ",")
        z.write("\n")

def cwriter(y,cd):
    z = open(y,'w')
    for thing in cd:
        z.write(thing + "::" + str(cd[thing]) + "\n")

def runner(clim):
    cd = ranger(f,g,clim)
    cwriter(h,cd)

#n = 0
#wl = importer(h)
#ranger(wl,f,g,j,2)

#2breakdown 500/2500/6000/10000/20000/50000/100000/200000
#5breakdown 500/2000/5000/8000/15000/30000/50000/100000/200000
