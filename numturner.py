g = 'space/contextus.txt'
h = 'space/tallus.txt'

def concounter(y1,y2,lim):
    z1 = open(y1,'r')
    cls = z1.readlines()
    l = len(cls)
    n = 0
    while n*lim < l:
        print "CONTEXTS " + str(n+1)
        z2 = open(y2,'r')
        foc = cls[n*lim:(n+1)*lim]
        cont = {}
        for line in foc:
            line = line.split("::")
            cont[line[0]] = {}
        m = 0
        for line in z2:
            if m%20000 == 0:
                print m/20000
            m += 1
            line = line[:-2].split("::")
            try:
                sline = line[1].split(",")
                for pair in sline:
                    pair = pair.split(":")
                    if pair[0] in cont:
                        cont[pair[0]][line[0]] = pair[1]
                    pair = None
            except IndexError:
                print "ERROR",line
            line = None
            sline = None
        writer(cont)
        cont = None
        n += 1
        z2.close()

def writer(cont):
    for thing in cont:
        y = "space/contexts/" + str(thing) + ".txt"
        z = open(y,'w')
        for word in cont[thing]:
            z.write(word + "::" + cont[thing][word] + "\n")
        z.close()

concounter(g,h,300000)
