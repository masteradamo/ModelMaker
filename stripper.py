import re
import string
import unicodedata

def runner(d):
    f = open(d,'r')
    g = open('space/linus.txt','w')
    n = 0
    for para in f:
        if n%10000 == 0:
            print n
        if re.match(".*\W$",para):
            para = para[:-1]
            para = re.split("\. |\? |! |; ",para)
    #        para = para.split(". ")
    #        para = para.split("? ")
    #        para = para.split("! ")
            for line in para:
    #            line = unicodedata.normalize('NFKD',line).encode('ascii','ignore')
                test = line.split()
    #            print line
                if len(test) > 4:
                    line = re.sub(" \([^(]*?\)","",line)
                    line = re.sub(" \([^(]*?\)","",line)
                    line = re.sub(" \([^(]*?\)","",line)
                    line = re.sub(",|;|:|!|\"|\'|\[|\]|\{|\}|\(|\)|\?|\.","",line)
                    line = line.lower()
                    line = re.sub("( |^)((the)|(a)|(an)) "," ",line)
                    line = re.sub("  +"," ",line)
    #                line = re.sub("\d+\.*\d*","#",line)
                    if re.match("\w",line):
                        g.write(line + "\n")
    #        print line
        n += 1
    f.close()
    g.close()

#total para count space1 = 123420000
